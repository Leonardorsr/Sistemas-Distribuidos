"""
API Flask para Sistema de Presença
"""
from flask import Flask, request
from flask_cors import CORS
from models import GerenciadorDados
from utils import json_response, handle_errors, validate_required_fields
from datetime import datetime

# Inicialização
app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

# Gerenciador de dados
db = GerenciadorDados()


# ==================== ROTAS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica se a API está funcionando"""
    return json_response(
        data={'status': 'online', 'timestamp': datetime.now().isoformat()},
        message='API funcionando corretamente'
    )


@app.route('/api/turmas', methods=['GET'])
@handle_errors
def listar_turmas():
    """
    GET /api/turmas
    Retorna lista de todas as turmas
    """
    turmas = db.obter_turmas()
    return json_response(
        data=[t.to_dict() for t in turmas],
        message=f'{len(turmas)} turma(s) encontrada(s)'
    )


@app.route('/api/turmas/<int:turma_id>/alunos', methods=['GET'])
@handle_errors
def listar_alunos_turma(turma_id: int):
    """
    GET /api/turmas/{turma_id}/alunos
    Retorna alunos de uma turma específica
    """
    alunos = db.obter_alunos_por_turma(turma_id)
    
    if not alunos:
        return json_response(
            data=[],
            message=f'Nenhum aluno encontrado na turma {turma_id}',
            status_code=404
        )
    
    # Adicionar status de presença (padrão: presente)
    alunos_com_status = []
    for aluno in alunos:
        aluno_dict = aluno.to_dict()
        aluno_dict['presente'] = True  # Default
        alunos_com_status.append(aluno_dict)
    
    return json_response(
        data=alunos_com_status,
        message=f'{len(alunos)} aluno(s) encontrado(s)'
    )


@app.route('/api/presencas', methods=['POST'])
@handle_errors
def salvar_presencas():
    """
    POST /api/presencas
    Salva registro de presenças
    
    Body: {
        "turma_id": 1,
        "data": "2024-01-15",
        "presencas": [
            {"aluno_id": "2024001", "presente": true},
            {"aluno_id": "2024002", "presente": false}
        ]
    }
    """
    data = request.get_json()
    
    # Validar campos obrigatórios
    validate_required_fields(data, ['turma_id', 'data', 'presencas'])
    
    # Validar formato da data
    try:
        datetime.strptime(data['data'], '%Y-%m-%d')
    except ValueError:
        raise ValueError('Data deve estar no formato YYYY-MM-DD')
    
    # Salvar
    sucesso = db.salvar_presencas(
        turma_id=data['turma_id'],
        data=data['data'],
        presencas=data['presencas']
    )
    
    if sucesso:
        return json_response(
            message='Presenças salvas com sucesso',
            status_code=201
        )
    else:
        return json_response(
            success=False,
            message='Erro ao salvar presenças',
            status_code=500
        )


@app.route('/api/presencas', methods=['GET'])
@handle_errors
def listar_presencas():
    """
    GET /api/presencas?turma_id=1&data=2024-01-15
    Retorna presenças com filtros opcionais
    """
    turma_id = request.args.get('turma_id', type=int)
    data = request.args.get('data', type=str)
    
    presencas = db.obter_presencas(turma_id=turma_id, data=data)
    
    return json_response(
        data=presencas,
        message=f'{len(presencas)} registro(s) encontrado(s)'
    )


@app.route('/api/turmas/<int:turma_id>/estatisticas', methods=['GET'])
@handle_errors
def obter_estatisticas(turma_id: int):
    """
    GET /api/turmas/{turma_id}/estatisticas
    Retorna estatísticas de presença da turma
    """
    stats = db.obter_estatisticas(turma_id)
    
    return json_response(
        data=stats,
        message='Estatísticas calculadas com sucesso'
    )


@app.route('/api/alunos/buscar', methods=['GET'])
@handle_errors
def buscar_aluno():
    """
    GET /api/alunos/buscar?q=Ana
    Busca alunos por nome
    """
    query = request.args.get('q', '').lower()
    
    if not query:
        raise ValueError('Parâmetro "q" é obrigatório')
    
    todos_alunos = db.carregar_alunos()
    resultados = [
        a.to_dict() for a in todos_alunos 
        if query in a.nome_aluno.lower()
    ]
    
    return json_response(
        data=resultados,
        message=f'{len(resultados)} aluno(s) encontrado(s)'
    )


# ==================== ERRO HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return json_response(
        success=False,
        message='Rota não encontrada',
        status_code=404
    )


@app.errorhandler(405)
def method_not_allowed(error):
    return json_response(
        success=False,
        message='Método não permitido',
        status_code=405
    )


# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Iniciando API de Sistema de Presença")
    print("=" * 50)
    print(f"📊 Alunos carregados: {len(db.carregar_alunos())}")
    print(f"📚 Turmas disponíveis: {len(db.obter_turmas())}")
    print("=" * 50)
    print("✅ Servidor rodando em: http://localhost:5000")
    print("📖 Rotas disponíveis:")
    print("   GET  /api/health")
    print("   GET  /api/turmas")
    print("   GET  /api/turmas/{id}/alunos")
    print("   POST /api/presencas")
    print("   GET  /api/presencas")
    print("   GET  /api/turmas/{id}/estatisticas")
    print("   GET  /api/alunos/buscar?q=nome")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
