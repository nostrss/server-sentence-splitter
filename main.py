from fastapi import FastAPI
from pydantic import BaseModel
from wtpsplit import SaT

app = FastAPI()
model = SaT("sat-3l-sm")


class SplitRequest(BaseModel):
    text: str
    language: str = ""


class SplitResponse(BaseModel):
    sentences: list[str]


@app.post("/split")
def split_sentences(req: SplitRequest) -> SplitResponse:
    sentences = model.split(req.text)
    return SplitResponse(sentences=[s.strip() for s in sentences if s.strip()])


@app.get("/health")
def health():
    return {"status": "ok"}
