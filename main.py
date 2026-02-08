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

import random

def pick_reply(mood: str, text: str) -> str:
    t = text.strip().lower()

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

    greetings = [
        "Szia 😘 jó, hogy írtál!",
        "Helló 💕 már vártalak.",
        "Sziaaa 😊 mesélj, mi újság?",
    ]

    questions = [
        "Ez érdekes… mesélnél róla kicsit bővebben? 😌",
        "És te mit gondolsz erről igazán?",
        "Miért fontos ez most neked? 💭",
    ]

    pool = base.get(mood, base["Cuki"]).copy()

    if any(x in t for x in ["szia", "hello", "cső", "csá"]):
        pool += greetings

    if "?" in t:
        pool += questions

    return f"({mood}) {random.choice(pool)}"
