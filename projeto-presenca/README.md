# 📘 API Flask -- Sistema de Presença

Esta é uma API desenvolvida em **Flask** para gerenciar turmas, alunos e
registros de presença.\
Ela lê e atualiza arquivos **CSV** e **JSON**, permitindo que um
frontend (ou outro sistema) consuma os dados via HTTP.

## 🚀 Pré-requisitos

-   Python 3.9+
-   pip instalado
-   (Opcional) Virtualenv

## 📦 Instalação

``` bash
pip install flask flask-cors
```

Ou:

``` bash
pip install -r requirements.txt
```

## ▶️ Como rodar

``` bash
python app.py
```

A API ficará disponível em:

    http://localhost:5000

## 🌐 Rotas

-   GET /api/health\
-   GET /api/turmas\
-   GET /api/turmas/{id}/alunos\
-   POST /api/presencas\
-   GET /api/presencas\
-   GET /api/turmas/{id}/estatisticas\
-   GET /api/alunos/buscar?q=nome

## 📝 Exemplo de body (POST /api/presencas)

``` json
{
  "turma_id": 1,
  "data": "2024-01-15",
  "presencas": [
    {"aluno_id": "2024001", "presente": true},
    {"aluno_id": "2024002", "presente": false}
  ]
}
```

## ⚠️ Erros

A API trata: - 404 (rota não encontrada) - 405 (método não permitido)

Todas as respostas seguem o padrão:

``` json
{
  "success": true/false,
  "message": "Descrição",
  "data": {...}
}
```

## 🛠️ Modo produção opcional

``` bash
pip install gunicorn
gunicorn -b 0.0.0.0:5000 app:app
```
