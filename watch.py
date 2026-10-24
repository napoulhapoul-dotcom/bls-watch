import os, re, requests

URL = "https://www.blsinternational.com/portugal/morocco/"
CHAT = "@fatherNabil99"
TOKEN = os.environ["TG_TOKEN"].strip()

def send(msg):
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT, "text": msg}, timeout=30)
    print("Telegram:", r.status_code, r.text)
    return r.ok

try:
    resp = requests.get(URL, timeout=30,
        headers={"User-Agent": "Mozilla/5.0"})
    print("Site status:", resp.status_code)
    html = resp.text
except Exception as e:
    print("Site error:", e)
    raise SystemExit

text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))
m = re.search(r"La prochaine de ces journées aura lieu(.{0,200})", text)
snippet = m.group(1).strip() if m else "INTROUVABLE"
print("Snippet:", snippet[:100])
