from flask import Flask, Response
import requests
import os

app = Flask(__name__)

API_KEY = "989f5e96ebc9a4c13a0196"
SECRET = "Raee546#RF"
BASE = "https://algozy.rathi.com/apimarketdata"

@app.route('/getInstruments')
def get_instruments():
    auth = requests.post(f"{BASE}/auth/login", json={
        "appKey": API_KEY,
        "secretKey": SECRET,
        "source": "WEBAPI"
    })
    if auth.status_code != 200:
        return f"Login failed: {auth.text}", 500

    token = auth.json()["result"]["token"]
    csv_data = ""

    for exch in ["NSECM", "BSECM"]:
        headers = {
            "AuthorizationToken": token,
            "x-source": "WEBAPI"
        }
        r = requests.get(f"{BASE}/instruments-master?exchangeSegmentList={exch}", headers=headers)
        if r.status_code == 200:
            csv_data += r.text
        else:
            csv_data += f"⚠️ {exch} fetch failed ({r.status_code})\n"
    return Response(csv_data, mimetype="text/plain")

@app.route('/')
def home():
    return "✅ Algozy Proxy is alive!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
