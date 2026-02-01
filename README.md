# Classificador Inteligente de Emails

Aplicação full stack para **classificação automática de emails corporativos**
utilizando **IA generativa**, com sugestão de resposta, histórico persistente
e coleta de feedback humano.

---

## Funcionalidades

-  Classificação de emails (texto ou arquivo `.txt` / `.pdf`)
-  Sugestão automática de resposta
-  Classificação: Produtivo / Improdutivo
-  Histórico persistente no backend
-  Feedback humano para melhoria futura do modelo
-  Estatísticas reais vindas da API
-  Resposta editável antes do envio

---

## Tecnologias Utilizadas

### Backend
- Python
- FastAPI
- Pydantic
- Hugging Face Transformers

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript (Fetch API)

---

## Endpoints Principais

### Classificação
- `POST /classify`
- `POST /classify-file`

### Histórico
- `GET /history`

### Estatísticas
- `GET /stats`

### Feedback
- `POST /feedback`

---

## Como executar o projeto

### Backend
```bash
pip install -r requirements.txt
uvicorn main:app --reload