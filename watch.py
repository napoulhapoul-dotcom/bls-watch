import os, re, requests

URL = "https://www.blsinternational.com/portugal/morocco/"
CHAT = "@fatherNabil99"
TOKEN = os.environ["TG_TOKEN"]

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT, "text": msg}, timeout=30)

try:
    html = requests.get(URL, timeout=30,
        headers={"User-Agent": "Mozilla/5.0"}).text
except Exception as e:
    print("Erreur:", e); raise SystemExit

text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))
m = re.search(r"La prochaine de ces journées aura lieu(.{0,200})", text)
snippet = m.group(1).strip() if m else "INTROUVABLE"

last = open("last.txt").read() if os.path.exists("last.txt") else ""
if snippet != last:
    if snippet == "INTROUVABLE":
        send("BLS Portugal : l'avis a changé ou disparu, vérifie la page : " + URL)
    else:
        send("BLS Portugal Rabat, portes ouvertes : " + snippet + "\n" + URL)
    open("last.txt", "w").write(snippet)
