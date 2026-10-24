import os, re, requests

URL = "https://www.blsinternational.com/portugal/morocco/"
CHAT = "@nabil_visa_alerts"
TOKEN = os.environ.get("TG_TOKEN", "").strip()
print("Token length:", len(TOKEN))

def send(msg):
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT, "text": msg}, timeout=30)
        print("Telegram:", r.status_code, r.text)
        return r.ok
    except Exception as e:
        print("Telegram error:", e)
        return False

manual = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"
if manual:
    send("Test: the BLS watcher is working")

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

last = open("last.txt").read() if os.path.exists("last.txt") else ""
if snippet != last:
    if snippet == "INTROUVABLE":
        ok = send("BLS Portugal : l'avis a changé ou disparu : " + URL)
    else:
        ok = send("BLS Portugal Rabat, portes ouvertes : " + snippet + "\n" + URL)
    if ok:
        open("last.txt", "w").write(snippet)
