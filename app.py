from flask import Flask, render_template, request, redirect, url_for, flash
from urllib.parse import urlparse
import json
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-for-production"
DATA_FILE = Path(__file__).parent / "submissions.json"

def valid_http_url(value):
    try:
        parsed = urlparse(value)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc) and "." in parsed.netloc
    except Exception:
        return False

def load_submissions():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

def save_submissions(items):
    DATA_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        reg_no = request.form.get("reg_no", "").strip()
        title = request.form.get("title", "").strip()
        submission_url = request.form.get("submission_url", "").strip()

        if not all([name, reg_no, title, submission_url]):
            flash("All fields are required.", "error")
        elif not valid_http_url(submission_url):
            flash("Please enter a valid http:// or https:// submission URL.", "error")
        else:
            items = load_submissions()
            items.append({
                "name": name,
                "reg_no": reg_no,
                "title": title,
                "submission_url": submission_url
            })
            save_submissions(items)
            flash("Submission saved successfully.", "success")
            return redirect(url_for("index"))
    return render_template("index.html", submissions=load_submissions())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
