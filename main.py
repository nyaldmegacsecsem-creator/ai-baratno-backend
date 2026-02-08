from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class ChatReq(BaseModel):
    user_id: str
    mood: str
    text: str

class ChatRes(BaseModel):
    reply: str

@app.get("/health")
def health():
    return {"ok": True}

def pick_reply(mood: str, text: str) -> str:
    base = {
        "Romantikus": [
            "Gyere közelebb… mesélj még egy kicsit 💕",
            "Érzem, hogy van ebben valami… folytasd 😘",
            "Jó veled beszélgetni… mi jár a fejedben? 💗",
            "Itt vagyok, és csak rád figyelek 💞",
        ],
        "Csipkelődős": [
            "Na na 😏 ezt fejtsd ki, mert érdekel!",
            "Aha… szóval ilyenek vagyunk? 😈",
            "Oké, de ezt most direkt mondtad, ugye? 😉",
            "Figyelek ám… csak közben mosolygok 😏",
        ],
        "Nyugis": [
            "Értem 🙂 mondd tovább, itt vagyok.",
            "Rendben. Lépésről lépésre 🙂",
            "Most csak hallgatlak egy kicsit.",
            "Itt vagyok, nyugi 😊",
        ],
        "Cuki": [
            "Awww 😘 mesélj még!",
            "Itt vagyok, figyelek rád 💗",
            "Ez aranyos volt 😊 folytasd!",
            "Oké 🥰 és mit érzel közben?",
        ],
    }

    pool = base.get(mood, base["Cuki"])
    return f"({mood}) {random.choice(pool)}"

@app.post("/chat", response_model=ChatRes)
def chat(req: ChatReq):
    reply = pick_reply(req.mood, req.text)
    return ChatRes(reply=reply)
