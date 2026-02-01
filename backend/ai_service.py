from transformers import pipeline

classifier = None
LABELS = ["Produtivo", "Improdutivo"]

def get_classifier():
    global classifier
    if classifier is None:
        classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
    return classifier


def classify_and_generate_response(email_text: str) -> dict:
    clf = get_classifier()
    result = clf(email_text, LABELS)
    classificacao = result["labels"][0]

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
