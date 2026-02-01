import requests
import os

HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HF_TOKEN = os.getenv("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

LABELS = {
    "Produtivo": "email que solicita ação, suporte, status, resposta ou resolução de problema",
    "Improdutivo": "email apenas informativo, agradecimento, felicitação ou sem necessidade de ação"
}

def classify_and_generate_response(email_text: str) -> dict:
    payload = {
        "inputs": email_text,
        "parameters": {
            "candidate_labels": list(LABELS.values())
        }
    }

    response = requests.post(
        HF_API_URL,
        headers=HEADERS,
        json=payload,
        timeout=30
    )

    result = response.json()

    # 🔁 Mapeia descrição → rótulo final
    label_descricao = result["labels"][0]
    classificacao = next(
        k for k, v in LABELS.items() if v == label_descricao
    )

    if classificacao == "Produtivo":
        resposta = (
            "Prezado(a),\n\n"
            "Recebemos sua mensagem e ela foi encaminhada para análise. "
            "Em breve retornaremos com uma atualização.\n\n"
            "Atenciosamente,\nEquipe de Atendimento"
        )
    else:
        resposta = (
            "Olá,\n\n"
            "Agradecemos sua mensagem e o contato. "
            "Desejamos um excelente dia!\n\n"
            "Atenciosamente,\nEquipe de Atendimento"
        )

    return {
        "classificacao": classificacao,
        "resposta_sugerida": resposta
    }
