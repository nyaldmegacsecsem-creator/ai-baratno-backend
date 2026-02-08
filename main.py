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

def pick_reply(mood: str, text: str) -> str:
    t = text.strip().lower()
    if any(x in t for x in ["szia", "hello", "cső", "csá"]):
        if mood == "Romantikus":
            return "Szia, szívem… örülök, hogy itt vagy velem 💗"
        if mood == "Csipkelődős":
            return "Szia 😏 na végre, már vártalak!"
        if mood == "Nyugis":
            return "Szia 🙂 nyugi, itt vagyok. Mi újság?"
        return "Szia 😘 hogy vagy most?"

    if "?" in text:
        if mood == "Romantikus":
            return "Imádom, hogy kérdezel… mondd, mit szeretnél tudni? 💕"
        if mood == "Csipkelődős":
            return "Hmm, kérdezgetünk? 😏 Oké, de te is mesélsz!"
        if mood == "Nyugis":
            return "Persze 🙂 kérdezz nyugodtan."
        return "Kérdezz csak 😄 figyelek rád."

    base = {
        "Romantikus": [
            "Gyere közelebb… mesélj még egy kicsit 💕",
            "Érzem, hogy van ebben valami… folytasd 😘",
            "Jó veled beszélgetni… mi jár a fejedben? 💗",
        ],
        "Csipkelődős": [
            "Na na 😏 ezt fejtsd ki, mert érdekel!",
            "Oké, ezt felírom… de mit akarsz ezzel mondani? 😉",
            "Aha… szóval ilyenek vagyunk? 😈",
        ],
        "Nyugis": [
            "Értem 🙂 mondd tovább, itt vagyok.",
            "Oké, és most mire lenne szükséged?",
            "Rendben. Lépésről lépésre 🙂",
        ],
        "Cuki": [
            "Awww 😘 mesélj még!",
            "Itt vagyok, figyelek rád 💗",
            "Oké 😊 és hogyan érzed magad ettől?",
        ],
    }
    arr = base.get(mood, base["Cuki"])
    return f"({mood}) {random.choice(arr)}"

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/chat", response_model=ChatRes)
def chat(req: ChatReq):
    reply = pick_reply(req.mood, req.text)
    return ChatRes(reply=reply)
