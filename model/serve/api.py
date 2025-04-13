from fastapi import FastAPI
import random
from openai import OpenAI
import os
from dotenv import load_dotenv
from google import genai

app = FastAPI()

load_dotenv()

client = genai.Client(api_key=os.environ["GOOGLE_AI_KEY"])

# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust this in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# introductionTranslations = {
#     "english": "Hi I'm Ola, can I speak in your language?",
#     "french": "Salut, je suis Ola, puis-je parler dans votre langue ?",
#     "spanish": "Hola, soy Ola, ¿puedo hablar en tu idioma?",
#     "german": "Hallo, ich bin Ola. Kann ich in deiner Sprache sprechen?",
#     "swahili": "Hujambo, mimi ni Ola, naweza kuzungumza kwa lugha yako?",
#     "lingala": "Mbote, nazali Ola, nakoki koloba na lokota na yo?",
#     "yoruba": "Báwo, èmi ni Ola, ṣé mo lè sọ̀rọ̀ ní èdè rẹ?",
#     "zulu": "Sawubona, ngingu Ola, ngingakhuluma ngolimi lwakho?",
#     "portuguese": "Oi, eu sou Ola, posso falar na sua língua?",
#     "arabic": "مرحبًا، أنا أولا، هل يمكنني التحدث بلغتك؟",
#     "russian": "Привет, я Ола, могу ли я говорить на твоём языке?",
#     "chinese": "嗨，我是Ola，我可以说你的语言吗？",
#     "japanese": "こんにちは、私はオラです。あなたの言語で話してもいいですか？",
#     "hindi": "नमस्ते, मैं ओला हूँ, क्या मैं आपकी भाषा में बात कर सकता हूँ?",
#     "turkish": "Merhaba, ben Ola, senin dilinde konuşabilir miyim?",
#     "italian": "Ciao, sono Ola, posso parlare nella tua lingua?",
#     "dutch": "Hoi, ik ben Ola, mag ik in jouw taal spreken?",
#     "korean": "안녕하세요, 저는 Ola입니다. 당신의 언어로 말해도 될까요?",
#     "amharic": "ሰላም፣ እኔ ኦላ ነኝ፣ በቋንቋዎ መናገር እችላለሁ?",
#     "filipino": "Hi, ako si Ola, pwede ba akong magsalita sa iyong wika?"
# }

# def introductionSentence():
#     return random.choice(list(introductionTranslations.values()))

# def translator(text: str, targetLanguage: str) -> str:
#     return f"{text} in {targetLanguage}: {text.upper()}"

# @app.get("/test")
# async def root():
#     return {"message": "hello world"}

# @app.get("/translate")
# async def translation(originalText, targetLanguage):
#     return {"translation": translator(originalText, targetLanguage)}

# @app.get("/randomTranslation")
# async def randomTranslation():
#     sentence = introductionSentence()
#     return {"introductionSentence": sentence}

# @app.get("/openaisentence")
# async def openaisentence():


#     return 

response = client.models.generate_content(
    model="gemini-2.0-flash-lite-001",
    contents="""
        Generate a short but semantically rich English sentence. 
        It should be clear, meaningful, and natural — not generic or templated. 
        Avoid clichés. Make it sound like something a human might say in everyday or unique conversation.

        The sentence will be used to validate a machine translation model in a human-in-the-loop RLHF setup, so ensure the vocabulary is diverse and not always literal or common.

        Only return the sentence — no explanation or additional text.
    """
)

print(response.text)