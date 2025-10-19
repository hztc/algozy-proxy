from flask import Flask, Response
import requests

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
    token = auth.json()["result"]["token"]

    csv_data = ""
    for exch in ["NSECM", "BSECM"]:
        headers = {"AuthorizationToken": token, "x-source": "WEBAPI"}
        r = requests.get(f"{BASE}/instruments-master?exchangeSegmentList={exch}", headers=headers)
        if r.status_code == 200:
            csv_data += r.text
        else:
            print(f"⚠️ Failed {exch}: {r.status_code}")
    return Response(csv_data, mimetype="text/csv")

@app.route('/')
def home():
    return "✅ Algozy XTS Proxy is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
