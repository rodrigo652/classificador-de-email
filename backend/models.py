from pydantic import BaseModel

class EmailRequest(BaseModel):
    content: str

class EmailResponse(BaseModel):
    classificacao: str
    resposta_sugerida: str
    tempo_processamento: float