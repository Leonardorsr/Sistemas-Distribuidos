Sistema de Gerenciamento de Presença Escolar
<div align="center">
PythonFlaskVue.jsLicense

Sistema web completo para gerenciamento de presenças e faltas de alunos

Demonstração • Instalação • Uso • API • Estrutura

</div>
📋 Índice
Sobre o Projeto
Funcionalidades
Tecnologias
Arquitetura
Instalação
Uso
Documentação da API
Estrutura do Projeto
Contribuindo
Licença
🎯 Sobre o Projeto
Sistema desenvolvido para facilitar o controle de presença em ambientes educacionais. Permite que professores e coordenadores registrem presenças/faltas de forma rápida e intuitiva, com persistência de dados em CSV (estado atual) e JSON (histórico completo).

🌟 Diferenciais
✅ Dupla persistência: CSV para estado atual + JSON para histórico completo
✅ Interface moderna: Design responsivo com Vue.js 3
✅ API RESTful: Backend Flask bem estruturado e documentado
✅ Estatísticas em tempo real: Taxas de presença e análises por aluno
✅ Ações em lote: Marcar todos presentes/ausentes com um clique
✅ Validação robusta: Tratamento de erros em todas as camadas
🚀 Funcionalidades
📊 Gestão de Turmas
Listagem de turmas disponíveis
Visualização de quantidade de alunos por turma
Seleção intuitiva de turma
👥 Controle de Alunos
Lista completa de alunos por turma
Status visual de presença (verde) e ausência (vermelho)
Matrícula e nome do aluno organizados
✅ Registro de Presença
Marcação individual de presença/falta
Ações em lote (todos presentes/ausentes)
Seleção de data customizada
Salvamento automático com feedback visual
📈 Estatísticas
Total de alunos, presentes e ausentes
Taxa de presença média por turma
Estatísticas individuais por aluno
Histórico completo de presenças
🔍 Busca
Busca de alunos por nome
Filtros por turma e data
Resultados em tempo real
🛠 Tecnologias Utilizadas
Backend

Flask 3.0.0          # Framework web minimalista
Flask-CORS 4.0.0     # Habilitação de CORS
Pandas 2.1.4         # Manipulação de dados CSV
Python-dotenv 1.0.0  # Gestão de variáveis de ambiente
Frontend

Vue.js 3             # Framework JavaScript progressivo
Axios                # Cliente HTTP
CSS3                 # Estilização customizada
Armazenamento

CSV                  # Estado atual das presenças
JSON                 # Histórico completo de registros
🏗 Arquitetura

┌─────────────────┐
│   Frontend      │
│   (Vue.js 3)    │
│                 │
│  - Interface    │
│  - Validação    │
│  - Feedback     │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│   Backend       │
│   (Flask API)   │
│                 │
│  - Rotas        │
│  - Validação    │
│  - Lógica       │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼──┐  ┌───▼────┐
│ CSV  │  │  JSON  │
│      │  │        │
│Estado│  │Histórico│
└──────┘  └────────┘
Fluxo de Dados
Leitura inicial: Frontend busca turmas → Backend lê CSV
Seleção de turma: Frontend carrega alunos com status atual do CSV
Marcação: Usuário marca presenças na interface (estado local)
Salvamento:
CSV é atualizado com estado atual (presente/ausente)
JSON recebe novo registro timestampado no histórico
Reload: Frontend recarrega dados atualizados do CSV
📦 Instalação
Pré-requisitos
Python 3.8 ou superior
pip (gerenciador de pacotes Python)
Navegador web moderno
Passo a Passo
Clone o repositório
bash

git clone https://github.com/seu-usuario/sistema-presenca.git
cd sistema-presenca
Crie um ambiente virtual
bash

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
Instale as dependências
bash

pip install -r backend/requirements.txt
Estrutura de diretórios

sistema-presenca/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── utils.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── js/
│   │   └── app.js
│   └── css/
│       └── style.css
└── data/
    ├── alunos.csv
    └── presencas.json
Inicie o backend
bash

cd backend
python app.py
Você verá:


==================================================
🚀 Iniciando API de Sistema de Presença
==================================================
📊 Alunos carregados: 14
📚 Turmas disponíveis: 3
==================================================
✅ Servidor rodando em: http://localhost:5000
📖 Rotas disponíveis:
   GET  /api/health
   GET  /api/turmas
   GET  /api/turmas/{id}/alunos
   POST /api/presencas
   GET  /api/presencas
   GET  /api/turmas/{id}/estatisticas
   GET  /api/alunos/buscar?q=nome
==================================================
Abra o frontend
Abra frontend/index.html diretamente no navegador ou use um servidor local:

bash

# Opção 1: Python
cd frontend
python -m http.server 8080

# Opção 2: Node.js (se tiver instalado)
npx serve .

# Acesse: http://localhost:8080
💻 Uso
Interface Principal
Selecione uma turma no dropdown superior
Escolha a data (padrão: hoje)
Marque presenças/faltas clicando nos botões de cada aluno
Use ações rápidas para marcar todos de uma vez (opcional)
Clique em "Salvar Presenças" para persistir os dados
Atalhos Úteis
Marcar Todos Presente: Útil no início da aula (depois ajusta exceções)
Marcar Todos Ausente: Útil para situações especiais (feriados, etc.)
Indicadores Visuais
🟢 Verde: Aluno presente
🔴 Vermelho: Aluno ausente
Números grandes: Estatísticas em tempo real
📡 Documentação da API
Base URL

http://localhost:5000/api
Endpoints
1. Health Check
http

GET /api/health
Resposta:

json

{
  "success": true,
  "message": "API funcionando corretamente",
  "data": {
    "status": "online",
    "timestamp": "2024-01-15T10:30:00"
  }
}
2. Listar Turmas
http

GET /api/turmas
Resposta:

json

{
  "success": true,
  "message": "3 turma(s) encontrada(s)",
  "data": [
    {
      "id": 1,
      "nome": "1º Ano A - Matemática",
      "quantidade_alunos": 5
    }
  ]
}
3. Listar Alunos por Turma
http

GET /api/turmas/{turma_id}/alunos
Parâmetros:

turma_id (path): ID da turma
Resposta:

json

{
  "success": true,
  "message": "5 aluno(s) encontrado(s)",
  "data": [
    {
      "id": "2024001",
      "matricula": "2024001",
      "nome": "Ana Silva",
      "turma_id": 1,
      "presente": true
    }
  ]
}
4. Salvar Presenças
http

POST /api/presencas
Body:

json

{
  "turma_id": 1,
  "data": "2024-01-15",
  "presencas": [
    {
      "aluno_id": "2024001",
      "presente": true
    },
    {
      "aluno_id": "2024002",
      "presente": false
    }
  ]
}
Resposta:

json

{
  "success": true,
  "message": "Presenças salvas com sucesso (CSV atualizado + histórico salvo)"
}
Comportamento:

✅ Atualiza coluna presenca_aluno no CSV
✅ Adiciona registro timestampado no JSON
✅ Remove duplicatas (mesma turma + data)
5. Consultar Histórico de Presenças
http

GET /api/presencas?turma_id=1&data=2024-01-15
Query Params:

turma_id (opcional): Filtrar por turma
data (opcional): Filtrar por data (YYYY-MM-DD)
Resposta:

json

{
  "success": true,
  "message": "2 registro(s) encontrado(s)",
  "data": [
    {
      "turma_id": 1,
      "data": "2024-01-15",
      "timestamp": "2024-01-15T14:30:00",
      "presencas": [...],
      "total_alunos": 5,
      "presentes": 4,
      "ausentes": 1
    }
  ]
}
6. Estatísticas da Turma
http

GET /api/turmas/{turma_id}/estatisticas
Resposta:

json

{
  "success": true,
  "message": "Estatísticas calculadas com sucesso",
  "data": {
    "turma_id": 1,
    "total_alunos": 5,
    "total_aulas": 10,
    "taxa_presenca_media": 87.5,
    "alunos_estatisticas": [
      {
        "nome": "Ana Silva",
        "matricula": "2024001",
        "presencas": 9,
        "faltas": 1,
        "taxa_presenca": 90.0
      }
    ]
  }
}
7. Buscar Alunos
http

GET /api/alunos/buscar?q=Ana
Query Params:

q (obrigatório): Termo de busca (case-insensitive)
Resposta:

json

{
  "success": true,
  "message": "2 aluno(s) encontrado(s)",
  "data": [
    {
      "id": "2024001",
      "nome": "Ana Silva",
      "turma_id": 1,
      "presente": true
    }
  ]
}
Tratamento de Erros
Todos os endpoints retornam erros no formato padrão:

json

{
  "success": false,
  "message": "Descrição do erro"
}
Códigos HTTP:

200: Sucesso
201: Criado com sucesso
400: Erro de validação
404: Não encontrado
405: Método não permitido
500: Erro interno do servidor
📁 Estrutura do Projeto

sistema-presenca/
│
├── backend/
│   ├── app.py              # API Flask (rotas e inicialização)
│   ├── models.py           # Modelos de dados e lógica de negócio
│   ├── utils.py            # Funções utilitárias (decorators, validação)
│   └── requirements.txt    # Dependências Python
│
├── frontend/
│   ├── index.html          # Página principal (estrutura HTML)
│   ├── js/
│   │   └── app.js          # Lógica Vue.js (componente principal)
│   └── css/
│       └── style.css       # Estilos customizados
│
├── data/
│   ├── alunos.csv          # Base de dados de alunos (estado atual)
│   └── presencas.json      # Histórico de presenças
│
└── README.md               # Este arquivo
Descrição dos Arquivos
Backend
app.py

Inicialização do Flask com CORS
Definição de todas as rotas REST
Handlers de erro personalizados
Mensagens de startup informativas
models.py

Aluno: Dataclass com informações do aluno
Turma: Dataclass com informações da turma
GerenciadorDados: Classe principal de lógica de negócio
Carregamento de CSV
Salvamento duplo (CSV + JSON)
Cálculo de estatísticas
Gestão de cache
utils.py

json_response(): Padroniza respostas JSON
@handle_errors: Decorator para tratamento automático de exceções
validate_required_fields(): Validação de campos obrigatórios
Frontend
index.html

Estrutura semântica com Vue.js 3
CDN para Vue e Axios
Componentes reativos (turmas, alunos, toast)
app.js

Aplicação Vue.js com Composition API
Métodos para comunicação com API
Gerenciamento de estado local
Computed properties para estatísticas em tempo real
style.css

Design system com variáveis CSS
Layout responsivo (mobile-first)
Animações e transições suaves
Estados visuais (presente/ausente)
Data
alunos.csv

csv

cod_aluno,cod_turma,nome_aluno,presenca_aluno
2024001,1,Ana Silva,presente
presencas.json

json

[
  {
    "turma_id": 1,
    "data": "2024-01-15",
    "timestamp": "2024-01-15T14:30:00",
    "presencas": [...],
    "total_alunos": 5,
    "presentes": 4,
    "ausentes": 1
  }
]
🧪 Testando a API
Com cURL
bash

# Health check
curl http://localhost:5000/api/health

# Listar turmas
curl http://localhost:5000/api/turmas

# Salvar presenças
curl -X POST http://localhost:5000/api/presencas \
  -H "Content-Type: application/json" \
  -d '{
    "turma_id": 1,
    "data": "2024-01-15",
    "presencas": [
      {"aluno_id": "2024001", "presente": true}
    ]
  }'
Com Python
python

import requests

# Listar turmas
response = requests.get('http://localhost:5000/api/turmas')
print(response.json())

# Salvar presenças
dados = {
    'turma_id': 1,
    'data': '2024-01-15',
    'presencas': [
        {'aluno_id': '2024001', 'presente': True}
    ]
}
response = requests.post('http://localhost:5000/api/presencas', json=dados)
print(response.json())
🔧 Configuração Avançada
Variáveis de Ambiente
Crie um arquivo .env no diretório backend/:

env

FLASK_ENV=development
FLASK_DEBUG=True
CSV_PATH=../data/alunos.csv
JSON_PATH=../data/presencas.json
Personalizar Nomes de Turmas
Edite models.py, método obter_turmas():

python

nomes_turmas = {
    1: 'Sua Turma Personalizada',
    2: 'Outra Turma',
    # ...
}
Mudar Porta do Backend
Em app.py:

python

app.run(debug=True, host='0.0.0.0', port=8000)  # Altere 5000 para 8000
Atualize frontend/js/app.js:

javascript

apiUrl: 'http://localhost:8000/api'
🚨 Troubleshooting
Problema: "CORS error" no frontend
Solução: Verifique se Flask-CORS está instalado:

bash

pip install Flask-CORS
Problema: Dados não salvam
Solução:

Verifique permissões da pasta data/
Confira logs no terminal do backend
Valide formato dos dados enviados
Problema: CSV corrompido
Solução: O sistema cria backup automático. Restaure:

bash

cp data/alunos.csv.backup data/alunos.csv
Problema: JSON vazio
Solução: O sistema reseta automaticamente arquivos corrompidos e cria backup.

🤝 Contribuindo
Contribuições são bem-vindas! Siga os passos:

Fork o projeto
Crie uma branch para sua feature (git checkout -b feature/MinhaFeature)
Commit suas mudanças (git commit -m 'Adiciona MinhaFeature')
Push para a branch (git push origin feature/MinhaFeature)
Abra um Pull Request
Boas Práticas
✅ Mantenha tipagem forte (type hints em Python)
✅ Escreva código idiomático
✅ Adicione tratamento de erros
✅ Documente funções complexas
✅ Teste antes de enviar
📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

👨‍💻 Autor
Desenvolvido com ❤️ por [Seu Nome]

GitHub: @seu-usuario
LinkedIn: Seu Perfil
🎓 Melhorias Futuras
 Autenticação de usuários (JWT)
 Exportação de relatórios em PDF
 Gráficos de presença com Chart.js
 Notificações push
 Deploy com Docker
 Testes automatizados (pytest + Jest)
 CI/CD com GitHub Actions
 Dashboard administrativo
 Integração com Google Classroom
<div align="center">
⭐ Se este projeto foi útil, considere dar uma estrela!

Made with 🐍 Flask + ⚡ Vue.js

</div>
