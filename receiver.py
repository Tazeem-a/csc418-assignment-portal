import os
import json
import hmac
from pathlib import Path
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)

REPORT_PATH = Path(__file__).parent / "testreport.json"


@app.post("/report")
def receive_report():

    # Check authentication
    token = os.environ.get("REPORT_TOKEN", "")
    supplied = request.headers.get("X-Report-Token", "")

    if not token or not hmac.compare_digest(supplied, token):
        return jsonify({"error": "unauthorized"}), 401

    # Read incoming data
    raw_data = request.get_data(as_text=True)

    print("Content-Type:", request.content_type)
    print("Received body length:", len(raw_data))
    print("Received body preview:", repr(raw_data[:300]))

    # Remove extra header text if present
    if raw_data.startswith("Content-Length:"):
        parts = raw_data.split("\r\n\r\n", 1)
        if len(parts) == 2:
            raw_data = parts[1]

    # Parse JSON
    try:
        report = json.loads(raw_data)
    except (json.JSONDecodeError, TypeError) as e:
        print("JSON parsing error:", e)
        return jsonify({"error": "invalid JSON"}), 400

    print("Received data type:", type(report).__name__)

    if isinstance(report, dict):
        print("Received keys:", list(report.keys()))

    # Validate report
    if not isinstance(report, dict):
        return jsonify({"error": "report is not a JSON object"}), 400

    if "tests" not in report or "summary" not in report:
        return jsonify({
            "error": "required fields missing",
            "received_keys": list(report.keys())
        }), 400

    # Save report
    report["received_at"] = datetime.now(timezone.utc).isoformat()

    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print("Report successfully saved!")

    return jsonify({"saved": True}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
