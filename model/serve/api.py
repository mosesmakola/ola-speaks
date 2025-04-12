from fastapi import FastAPI

app = FastAPI()

def translator(text: str, targetLanguage: str) -> str:
    return f"{text} in {targetLanguage}: {text.upper()}"

@app.get("/test")
async def root():
    return {"message": "hello world"}

@app.get("/translate")
async def translation(originalText, targetLanguage):
    return {"translation": translator(originalText, targetLanguage)}