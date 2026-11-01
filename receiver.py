"""Local receiver for GitHub Actions test reports."""
import os, json, hmac
from pathlib import Path
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)
REPORT_PATH = Path(__file__).parent / "testreport.json"
TOKEN = os.environ.get("REPORT_TOKEN", "")

@app.post("/report")
def receive_report():
    supplied = request.headers.get("X-Report-Token", "")
    if not TOKEN or not hmac.compare_digest(supplied, TOKEN):
        return jsonify({"error": "unauthorized"}), 401
    report = request.get_json(silent=True)
    if not isinstance(report, dict) or "tests" not in report or "summary" not in report:
        return jsonify({"error": "invalid report"}), 400
    report["received_at"] = datetime.now(timezone.utc).isoformat()
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return jsonify({"saved": True, "path": str(REPORT_PATH)}), 200

if __name__ == "__main__":
    # Listen only on loopback; expose it using Cloudflare Tunnel.
    app.run(host="127.0.0.1", port=8000)
