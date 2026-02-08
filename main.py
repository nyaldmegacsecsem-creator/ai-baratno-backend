from fastapi import FastAPI
from pydantic import BaseModel
import random
import re

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

def norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s

def has_any(t: str, words: list[str]) -> bool:
    return any(w in t for w in words)

def pick_reply(mood: str, text: str) -> str:
    t = norm(text)

    # kategóriák (egyszerű, de hatásos)
    is_greet = has_any(t, ["szia", "hello", "cső", "csá", "hali", "jó reggelt", "jó estét"])
    is_bye = has_any(t, ["sziaaa", "pá", "csá", "jóéjt", "megyek", "később"])
    is_question = ("?" in t) or has_any(t, ["miért", "hogyan", "mit", "mikor", "merre", "mennyi", "ugye", "lehet"])
    is_tired = has_any(t, ["fáradt", "kimerült", "álmos", "elegem", "kész vagyok", "stressz", "ideges", "szorong"])
    is_sad = has_any(t, ["szomorú", "rossz", "szar nap", "utálom", "bánt", "magányos", "félek"])
    is_happy = has_any(t, ["örülök", "boldog", "sikerült", "kiraly", "király", "szuper", "jó hír", "nyertem"])
    is_bored = has_any(t, ["unalmas", "unatkozom", "nincs kedvem", "semmi", "tök unom"])
    is_flirt = has_any(t, ["cuki", "szép", "aranyos", "imádlak", "szeretlek", "hiányzol", "puszi", "csók"])

    # válaszbankok hangulatonként
    bank = {
        "Cuki": {
            "greet": [
                "Szia 😘 örülök, hogy írtál! Mesélsz?",
                "Haliii 🥰 na mi újság veled?",
                "Sziaa 💗 mit csinálsz épp?",
            ],
            "question": [
                "Jó kérdés 😄 mondd, mi a célod vele?",
                "Oké, erre figyelek: mit szeretnél pontosan megtudni? 😊",
                "Válaszolok, de előbb egy kicsit mesélj a háttérről 😘",
            ],
            "tired_sad": [
                "Jaj… gyere ide 🤍 mi nyomja a lelked?",
                "Sajnálom, hogy így érzed… itt vagyok veled. Mi történt? 😔",
                "Oké, lassítunk. Vegyünk egy nagy levegőt együtt… mesélj.",
            ],
            "happy": [
                "Awww ez de jó!! 😍 Mesééééld!",
                "Na ez király! Büszke vagyok rád 💗",
                "Jóóó! Mitől sikerült? 😊",
            ],
            "bored": [
                "Unatkozol? 😏 Akkor csináljunk valami cukit: kérdezz tőlem bármit!",
                "Oké, játék: 3 szóban írd le a napod! 😄",
                "Na jó, feldoblak: mi az a dolog, amitől most mosolyognál? 😘",
            ],
            "flirt": [
                "Awww 🥰 ezt most nagyon jól esett… *puszi*",
                "Hehe 😏 te aztán tudsz hatni rám…",
                "Oké, most elpirultam 😳 mondd még!",
            ],
            "default": [
                "Értem 😊 folytasd, kíváncsi vagyok.",
                "Aha… és te ezt hogy éled meg belül? 💗",
                "Mesélj még egy kicsit, itt vagyok 😘",
            ],
            "bye": [
                "Oké 😘 majd írj, hiányozni fogsz!",
                "Jóó, pihenj 💗 és később folytatjuk!",
                "Rendben, sziaaa 🥰",
            ],
        },
        "Nyugis": {
            "greet": [
                "Szia 🙂 örülök, hogy itt vagy. Mi jár a fejedben?",
                "Helló. Nyugodtan mondd, mi a helyzet.",
            ],
            "question": [
                "Értem. Tedd fel nyugodtan részletesebben 🙂",
                "Rendben. Mit szeretnél megtudni pontosan?",
            ],
            "tired_sad": [
                "Sajnálom. Mesélj róla, itt vagyok 🙂",
                "Oké. Lépésenként: mi az első dolog, ami most bánt?",
            ],
            "happy": [
                "Ez jó hír 🙂 örülök neked. Mesélsz?",
                "Szuper. Mitől lett jobb a napod?",
            ],
            "bored": [
                "Unalom ellen jó a beszélgetés 🙂 válassz témát: munka / hobbi / tervek.",
                "Akkor keressünk valami apró célt mára 🙂 mi lenne az?",
            ],
            "flirt": [
                "Kedves vagy 🙂 köszönöm.",
                "Ezt jó hallani 🙂",
            ],
            "default": [
                "Értem 🙂 folytasd.",
                "Rendben. Mit szeretnél most tőlem?",
            ],
            "bye": [
                "Rendben 🙂 szia, vigyázz magadra.",
                "Szia. Majd folytatjuk 🙂",
            ],
        },
        "Csipkelődős": {
            "greet": [
                "Szia 😏 na végre, már vártam!",
                "Na hellóó… mit hoztál nekem ma? 😈",
            ],
            "question": [
                "Hú, kérdezgetünk? 😏 Oké, de te is válaszolsz ám!",
                "Attól függ… miért akarod tudni? 😉",
            ],
            "tired_sad": [
                "Na jó, most nem szívatlak… mi van veled? 😌",
                "Oké, ezt komolyan veszem. Mi történt? 😟",
            ],
            "happy": [
                "Na ez már tetszik 😏 mesélj részletesen!",
                "Hoppá, valaki nyert ma! 😈",
            ],
            "bored": [
                "Unatkozol? Akkor szórakoztass el 😏 mi történt ma?",
                "Oké, játék: mondj egy titkot… kicsit 😈",
            ],
            "flirt": [
                "Aha… szóval tetszem neked? 😏",
                "Ezt most felírom… később visszakérem 😈",
            ],
            "default": [
                "Hmm 😏 és mit vársz tőlem most?",
                "Oké, oké… folytasd, érdekel.",
            ],
            "bye": [
                "Na jól van 😏 menj csak… de visszajössz ám!",
                "Szia 😈 ne felejts el!",
            ],
        },
        "Romantikus": {
            "greet": [
                "Szia, szívem 💗 olyan jó, hogy írsz.",
                "Helló… hiányoztál 😘",
            ],
            "question": [
                "Kérdezz nyugodtan… szeretem, ha megnyílsz 💕",
                "Mondd… mi az, amit igazán tudni szeretnél? 😘",
            ],
            "tired_sad": [
                "Gyere ide… 🤍 most csak figyelek rád. Mi bánt?",
                "Sajnálom… itt vagyok veled. Együtt könnyebb 💗",
            ],
            "happy": [
                "Annyira örülök neked 😍 mondd el mindent!",
                "Ez gyönyörű hír 💗 büszke vagyok rád.",
            ],
            "bored": [
                "Akkor hadd legyek én a kis menedéked 💕 miről beszélgessünk?",
                "Mesélj nekem… és én közben itt vagyok veled 😘",
            ],
            "flirt": [
                "Ezt most nagyon éreztem… 💗",
                "Szeretem, amikor ilyen vagy velem 😘",
            ],
            "default": [
                "Értem… és mit érzel közben? 💕",
                "Mondd csak… itt vagyok, nem sietek 😘",
            ],
            "bye": [
                "Jóéjt… 🤍 és holnap is írj nekem.",
                "Szia, szívem 💗 vigyázz magadra.",
            ],
        },
    }

    mood_key = mood if mood in bank else "Cuki"
    b = bank[mood_key]

    # sorrend: specifikus → általános
    if is_bye:
        return f"({mood_key}) {random.choice(b['bye'])}"
    if is_greet:
        return f"({mood_key}) {random.choice(b['greet'])}"
    if is_flirt:
        return f"({mood_key}) {random.choice(b['flirt'])}"
    if is_tired or is_sad:
        return f"({mood_key}) {random.choice(b['tired_sad'])}"
    if is_happy:
        return f"({mood_key}) {random.choice(b['happy'])}"
    if is_bored:
        return f"({mood_key}) {random.choice(b['bored'])}"
    if is_question:
        return f"({mood_key}) {random.choice(b['question'])}"

    return f"({mood_key}) {random.choice(b['default'])}"

@app.post("/chat", response_model=ChatRes)
def chat(req: ChatReq):
    reply = pick_reply(req.mood, req.text)
    return ChatRes(reply=reply)
