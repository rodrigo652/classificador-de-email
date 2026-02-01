from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
import time
import os

from schemas import FeedbackRequest
from models import EmailRequest, EmailResponse
from nlp import preprocess_text
from ai_service import classify_and_generate_response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI(title="Email Classifier API")

@app.get("/")
async def main_index():
    return RedirectResponse(url="/static/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

historico_emails = []
historico = []

@app.post("/classify", response_model=EmailResponse)
def classify_email(request: EmailRequest):
    start_time = time.time()

    processed_text = preprocess_text(request.content)

    ai_result = classify_and_generate_response(processed_text)

    elapsed_time = round(time.time() - start_time, 2)

    historico_emails.insert(0, {
        "classificacao": ai_result["classificacao"],
        "timestamp": time.time()
    })

    historico_emails[:] = historico_emails[:5]

    return EmailResponse(
        classificacao=ai_result["classificacao"],
        resposta_sugerida=ai_result["resposta_sugerida"],
        tempo_processamento=elapsed_time
    )



@app.post("/classify-file", response_model=EmailResponse)
def classify_file(file: UploadFile = File(...)):
    start_time = time.time()

    if file.filename.endswith(".txt"):
        content = file.file.read().decode("utf-8")

    elif file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        content = ""
        for page in reader.pages:
            content += page.extract_text() or ""

    else:
        raise HTTPException(status_code=400, detail="Formato não suportado")

    processed_text = preprocess_text(content)
    ai_result = classify_and_generate_response(processed_text)

    elapsed_time = round(time.time() - start_time, 2)

    historico_emails.insert(0, {
        "classificacao": ai_result["classificacao"],
        "timestamp": time.time()
    })

    historico_emails[:] = historico_emails[:5]

    return EmailResponse(
        classificacao=ai_result["classificacao"],
        resposta_sugerida=ai_result["resposta_sugerida"],
        tempo_processamento=elapsed_time
    )

@app.get("/history")
def get_history():
    return historico_emails

feedbacks = []

@app.post("/feedback")
def salvar_feedback(request: FeedbackRequest):
    feedbacks.append({
        "classificacao": request.classificacao,
        "feedback": request.feedback,
        "motivo": request.motivo
    })
    return {"status": "ok"}

@app.get("/stats")
def get_status():
    return {
        "total_emails": len(historico),
        "produtivos": len([h for h in historico if h["classificacao"] == "Produtivo"]),
        "improdutivos": len([h for h in historico if h["classificacao"] == "Improdutivo"])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
