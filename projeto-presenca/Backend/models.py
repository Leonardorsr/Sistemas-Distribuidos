"""
Modelos de dados e lógica de negócio
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
import json
import os


@dataclass
class Aluno:
    """Representa um aluno"""
    cod_aluno: str
    cod_turma: int
    nome_aluno: str
    presenca_aluno: str = "presente"  # ← NOVO CAMPO
    
    def to_dict(self) -> Dict:
        return {
            'id': self.cod_aluno,
            'matricula': self.cod_aluno,
            'nome': self.nome_aluno,
            'turma_id': self.cod_turma,
            'presente': self.presenca_aluno == 'presente'  # ← Converte para boolean
        }


@dataclass
class Turma:
    """Representa uma turma"""
    cod_turma: int
    nome: str
    quantidade_alunos: int
    
    def to_dict(self) -> Dict:
        return {
            'id': self.cod_turma,
            'nome': self.nome,
            'quantidade_alunos': self.quantidade_alunos
        }


class GerenciadorDados:
    """Gerencia leitura/escrita de dados"""
    
    def __init__(self, csv_path: str = 'data/alunos.csv', 
                 presencas_path: str = 'data/presencas.json'):
        self.csv_path = csv_path
        self.presencas_path = presencas_path
        self._alunos_cache: Optional[List[Aluno]] = None
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Garante que os arquivos de dados existem"""
        # Criar diretório data se não existir
        os.makedirs('data', exist_ok=True)
        
        # Criar CSV de exemplo se não existir
        if not os.path.exists(self.csv_path):
            df = pd.DataFrame({
                'cod_aluno': ['2024001', '2024002', '2024003', '2024004', 
                              '2024005', '2024006', '2024007', '2024008'],
                'cod_turma': [1, 1, 1, 1, 2, 2, 2, 2],
                'nome_aluno': ['Ana Silva', 'Bruno Costa', 'Carlos Santos', 
                               'Diana Oliveira', 'Eduardo Lima', 'Fernanda Souza',
                               'Gabriel Pereira', 'Helena Rodrigues'],
                'presenca_aluno': ['presente'] * 8  # ← NOVO: todos iniciam como presente
            })
            df.to_csv(self.csv_path, index=False)
        
        # Criar arquivo de presenças se não existir
        if not os.path.exists(self.presencas_path):
            with open(self.presencas_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def carregar_alunos(self, force_reload: bool = False) -> List[Aluno]:
        """Carrega alunos do CSV"""
        if self._alunos_cache is not None and not force_reload:
            return self._alunos_cache
        
        try:
            df = pd.read_csv(self.csv_path, dtype={
                'cod_aluno': str, 
                'cod_turma': int,
                'nome_aluno': str,
                'presenca_aluno': str  # ← NOVO
            })
            
            # Garantir que a coluna presenca_aluno existe
            if 'presenca_aluno' not in df.columns:
                df['presenca_aluno'] = 'presente'
                df.to_csv(self.csv_path, index=False)
            
            self._alunos_cache = [
                Aluno(
                    cod_aluno=str(row['cod_aluno']),
                    cod_turma=int(row['cod_turma']),
                    nome_aluno=str(row['nome_aluno']),
                    presenca_aluno=str(row['presenca_aluno'])  # ← NOVO
                )
                for _, row in df.iterrows()
            ]
            
            return self._alunos_cache
        except Exception as e:
            print(f"Erro ao carregar alunos: {e}")
            return []
    
    def salvar_presencas(self, turma_id: int, data: str, presencas: List[Dict]) -> bool:
        """
        Salva registro de presenças (JSON para histórico + CSV para status atual)
        
        Args:
            turma_id: ID da turma
            data: Data no formato YYYY-MM-DD
            presencas: Lista de dicts com 'aluno_id' e 'presente'
        
        Returns:
            bool: True se pelo menos CSV foi atualizado, False se erro total
        """
        csv_sucesso = False
        json_sucesso = False
        
        # ========== PARTE 1: ATUALIZAR CSV ==========
        try:
            csv_sucesso = self.atualizar_presencas_lote_csv(presencas)
            if csv_sucesso:
                print(f"✅ CSV atualizado com sucesso")
            else:
                print(f"⚠️ Falha ao atualizar CSV")
        except Exception as e:
            print(f"❌ Erro crítico ao atualizar CSV: {e}")
            csv_sucesso = False
        
        # ========== PARTE 2: SALVAR HISTÓRICO JSON ==========
        try:
            todas_presencas = []
            
            # Ler JSON existente (com múltiplas camadas de proteção)
            if os.path.exists(self.presencas_path):
                try:
                    # Verificar tamanho do arquivo
                    tamanho = os.path.getsize(self.presencas_path)
                    
                    if tamanho == 0:
                        print("ℹ️ Arquivo JSON vazio, inicializando lista vazia")
                        todas_presencas = []
                    else:
                        with open(self.presencas_path, 'r', encoding='utf-8') as f:
                            conteudo = f.read().strip()
                            
                            if conteudo:
                                todas_presencas = json.loads(conteudo)
                                print(f"ℹ️ JSON carregado: {len(todas_presencas)} registro(s) existente(s)")
                            else:
                                todas_presencas = []
                                
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON corrompido ({e}), resetando arquivo...")
                    todas_presencas = []
                    # Fazer backup do arquivo corrompido
                    backup_path = f"{self.presencas_path}.backup"
                    try:
                        import shutil
                        shutil.copy(self.presencas_path, backup_path)
                        print(f"   Backup salvo em: {backup_path}")
                    except:
                        pass
                        
                except Exception as e:
                    print(f"⚠️ Erro ao ler JSON: {e}, usando lista vazia")
                    todas_presencas = []
            else:
                print("ℹ️ Criando novo arquivo de histórico JSON")
                todas_presencas = []
            
            # Criar novo registro
            novo_registro = {
                'turma_id': turma_id,
                'data': data,
                'timestamp': datetime.now().isoformat(),
                'presencas': presencas,
                'total_alunos': len(presencas),
                'presentes': sum(1 for p in presencas if p.get('presente', False)),
                'ausentes': sum(1 for p in presencas if not p.get('presente', False))
            }
            
            # Remover registro duplicado (mesma turma + data)
            todas_presencas = [
                registro for registro in todas_presencas 
                if not (registro.get('turma_id') == turma_id and registro.get('data') == data)
            ]
            
            # Adicionar novo registro
            todas_presencas.append(novo_registro)
            
            # Salvar JSON
            with open(self.presencas_path, 'w', encoding='utf-8') as f:
                json.dump(todas_presencas, f, indent=2, ensure_ascii=False)
            
            print(f"✅ JSON salvo: {len(todas_presencas)} registro(s) total")
            json_sucesso = True
            
        except Exception as e:
            print(f"❌ Erro ao salvar histórico JSON: {e}")
            print(f"   Tipo do erro: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            json_sucesso = False
        
        # ========== RESULTADO FINAL ==========
        if csv_sucesso and json_sucesso:
            print("✅ Salvamento completo: CSV + JSON")
            return True
        elif csv_sucesso:
            print("⚠️ Salvamento parcial: CSV OK, JSON falhou")
            return True  # Retorna True porque principal (CSV) funcionou
        else:
            print("❌ Salvamento falhou completamente")
            return False

    
    def atualizar_presencas_lote_csv(self, presencas: List[Dict]) -> bool:
        """
        Atualiza múltiplas presenças de uma vez no CSV
        
        Args:
            presencas: Lista de dicts com 'aluno_id' e 'presente' (boolean)
        
        Returns:
            bool: True se sucesso, False se erro
        """
        try:
            df = pd.read_csv(self.csv_path, dtype={'cod_aluno': str})
            
            # Garantir que presenca_aluno existe
            if 'presenca_aluno' not in df.columns:
                df['presenca_aluno'] = 'presente'
            
            # Atualizar cada aluno
            for presenca in presencas:
                aluno_id = presenca['aluno_id']
                status = 'presente' if presenca['presente'] else 'ausente'
                df.loc[df['cod_aluno'] == aluno_id, 'presenca_aluno'] = status
            
            # Salvar CSV
            df.to_csv(self.csv_path, index=False)
            
            # Limpar cache
            self._alunos_cache = None
            
            print(f"✅ {len(presencas)} presença(s) atualizada(s) no CSV")
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar presenças no CSV: {e}")
            return False
    
    def obter_turmas(self) -> List[Turma]:
        """Retorna lista de turmas únicas do CSV"""
        alunos = self.carregar_alunos()
        
        # Agrupar por turma
        turmas_dict: Dict[int, List[Aluno]] = {}
        for aluno in alunos:
            if aluno.cod_turma not in turmas_dict:
                turmas_dict[aluno.cod_turma] = []
            turmas_dict[aluno.cod_turma].append(aluno)
        
        # Criar objetos Turma
        turmas = []
        nomes_turmas = {
            1: '1º Ano A - Matemática',
            2: '1º Ano B - Matemática',
            3: '2º Ano A - Física',
            4: '2º Ano B - Física',
            5: '3º Ano A - Química'
        }
        
        for cod_turma, alunos_turma in sorted(turmas_dict.items()):
            turmas.append(Turma(
                cod_turma=cod_turma,
                nome=nomes_turmas.get(cod_turma, f'Turma {cod_turma}'),
                quantidade_alunos=len(alunos_turma)
            ))
        
        return turmas
    
    def obter_alunos_por_turma(self, cod_turma: int) -> List[Aluno]:
        """Retorna alunos de uma turma específica"""
        alunos = self.carregar_alunos(force_reload=True)  # ← Force reload para pegar status atual
        return [a for a in alunos if a.cod_turma == cod_turma]
    
    def salvar_presencas(self, turma_id: int, data: str, presencas: List[Dict]) -> bool:
        """
        Salva registro de presenças (JSON para histórico + CSV para status atual)
        
        Args:
            turma_id: ID da turma
            data: Data no formato YYYY-MM-DD
            presencas: Lista de dicts com 'aluno_id' e 'presente'
        """
        try:
            # 1. Atualizar CSV com status atual
            sucesso_csv = self.atualizar_presencas_lote_csv(presencas)
            
            if not sucesso_csv:
                print("⚠️ Aviso: Erro ao atualizar CSV, mas continuando...")
            
            # 2. Salvar histórico no JSON
            if os.path.exists(self.presencas_path):
                with open(self.presencas_path, 'r', encoding='utf-8') as f:
                    todas_presencas = json.load(f)
            else:
                todas_presencas = []
            
            # Criar novo registro
            novo_registro = {
                'turma_id': turma_id,
                'data': data,
                'timestamp': datetime.now().isoformat(),
                'presencas': presencas
            }
            
            # Remover registro anterior da mesma turma/data se existir
            todas_presencas = [
                p for p in todas_presencas 
                if not (p['turma_id'] == turma_id and p['data'] == data)
            ]
            
            # Adicionar novo registro
            todas_presencas.append(novo_registro)
            
            # Salvar JSON
            with open(self.presencas_path, 'w', encoding='utf-8') as f:
                json.dump(todas_presencas, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Presenças salvas: CSV + JSON (histórico)")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar presenças: {e}")
            return False
    
    def obter_presencas(self, turma_id: Optional[int] = None, 
                       data: Optional[str] = None) -> List[Dict]:
        """Recupera presenças salvas com filtros opcionais"""
        try:
            if not os.path.exists(self.presencas_path):
                return []
            
            with open(self.presencas_path, 'r', encoding='utf-8') as f:
                todas_presencas = json.load(f)
            
            # Aplicar filtros
            resultado = todas_presencas
            if turma_id is not None:
                resultado = [p for p in resultado if p['turma_id'] == turma_id]
            if data is not None:
                resultado = [p for p in resultado if p['data'] == data]
            
            return resultado
        except Exception as e:
            print(f"Erro ao carregar presenças: {e}")
            return []
    
    def obter_estatisticas(self, turma_id: int) -> Dict:
        """Calcula estatísticas de presença de uma turma"""
        presencas = self.obter_presencas(turma_id=turma_id)
        alunos = self.obter_alunos_por_turma(turma_id)
        
        total_alunos = len(alunos)
        total_aulas = len(presencas)
        
        if total_aulas == 0:
            return {
                'turma_id': turma_id,
                'total_alunos': total_alunos,
                'total_aulas': 0,
                'taxa_presenca_media': 0,
                'alunos_estatisticas': []
            }
        
        # Calcular estatísticas por aluno
        estatisticas_alunos = {}
        for aluno in alunos:
            estatisticas_alunos[aluno.cod_aluno] = {
                'nome': aluno.nome_aluno,
                'matricula': aluno.cod_aluno,
                'presencas': 0,
                'faltas': 0
            }
        
        # Contar presenças e faltas
        for registro in presencas:
            for presenca in registro['presencas']:
                aluno_id = presenca['aluno_id']
                if aluno_id in estatisticas_alunos:
                    if presenca['presente']:
                        estatisticas_alunos[aluno_id]['presencas'] += 1
                    else:
                        estatisticas_alunos[aluno_id]['faltas'] += 1
        
        # Calcular taxas
        for stats in estatisticas_alunos.values():
            total = stats['presencas'] + stats['faltas']
            stats['taxa_presenca'] = (stats['presencas'] / total * 100) if total > 0 else 0
        
        taxa_media = sum(s['taxa_presenca'] for s in estatisticas_alunos.values()) / total_alunos
        
        return {
            'turma_id': turma_id,
            'total_alunos': total_alunos,
            'total_aulas': total_aulas,
            'taxa_presenca_media': round(taxa_media, 2),
            'alunos_estatisticas': list(estatisticas_alunos.values())
        }
