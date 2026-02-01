from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

LABELS = {
    "Produtivo": "email que solicita ação, suporte, status, resposta ou resolução de problema",
    "Improdutivo": "email apenas informativo, agradecimento, felicitação ou sem necessidade de ação"
}

def classify_and_generate_response(email_text: str) -> dict:
    result = classifier(
        email_text,
        list(LABELS.values()),
        hypothesis_template="Este email é {}."
    )

    # Mapeia de volta para o rótulo humano
    label_description = result["labels"][0]
    classificacao = next(
        key for key, value in LABELS.items() if value == label_description
    )

    if classificacao == "Produtivo":
        resposta = gerar_resposta_produtiva(email_text)
    else:
        resposta = gerar_resposta_improdutiva()

    return {
        "classificacao": classificacao,
        "resposta_sugerida": resposta
    }

def gerar_resposta_produtiva(texto: str) -> str:
    if "status" in texto.lower():
        return (
            "Prezado(a),\n\n"
            "Recebemos sua solicitação de status e ela já está em análise. "
            "Em breve retornaremos com uma atualização.\n\n"
            "Atenciosamente,\n"
            "Equipe de Atendimento"
        )

    if "erro" in texto.lower() or "problema" in texto.lower():
        return (
            "Prezado(a),\n\n"
            "Identificamos sua solicitação relacionada a um problema técnico. "
            "Nossa equipe já está analisando.\n\n"
            "Atenciosamente,\n"
            "Equipe de Atendimento"
        )

    return (
        "Prezado(a),\n\n"
        "Recebemos sua mensagem e ela foi encaminhada para análise. "
        "Em breve retornaremos.\n\n"
        "Atenciosamente,\n"
        "Equipe de Atendimento"
    )

def gerar_resposta_improdutiva() -> str:
    return (
        "Olá,\n\n"
        "Agradecemos sua mensagem e o contato. "
        "Desejamos um excelente dia!\n\n"
        "Atenciosamente,\n"
        "Equipe de Atendimento"
    )