import requests
import threading
import time
from flask import Flask

app = Flask(__name__)


REQUEST_INTERVAL = 0        # Time between Requests

# Session für Keep-Alive
session = requests.Session()

last_status = "Noch keine Anfrage gesendet."


def github_polling():
    global last_status
    url = "https://camo.githubusercontent.com/26041170d8f942d7876d6eccb0c9d1fbfe9ddc832cc3a9bf86fbcf9319c7b939/68747470733a2f2f6b6f6d617265762e636f6d2f67687076632f3f757365726e616d653d4e756d6277617265" # your link here

    while True:
        try:
            response = session.get(url)
            last_status = f"{time.ctime()}: Status {response.status_code}"
            print(last_status)

        except Exception as e:
            last_status = f"{time.ctime()}: Fehler: {e}"
            print(last_status)

        time.sleep(REQUEST_INTERVAL)  # künstliche Pause


# Hintergrundthread starten
thread = threading.Thread(target=github_polling, daemon=True)
thread.start()


@app.route("/")
def home():
    return f"""
    <h2>GitHub Monitor läuft</h2>
    <p>Letzter Status: {last_status}</p>
    <p>Polling-Intervall: {REQUEST_INTERVAL} Sekunden</p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
