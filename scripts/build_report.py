import json, os, sys
from datetime import datetime, timezone
from pathlib import Path

source = Path("pytest-report.json")
data = json.loads(source.read_text(encoding="utf-8")) if source.exists() else {}
tests = []
for item in data.get("tests", []):
    outcome = item.get("outcome", "unknown")
    call = item.get("call", {}) or {}
    longrepr = call.get("longrepr") or item.get("longrepr") or ""
    tests.append({
        "name": item.get("nodeid", item.get("name", "unnamed test")),
        "result": "passed" if outcome == "passed" else ("failed" if outcome == "failed" else outcome),
        "failure_message": str(longrepr) if outcome == "failed" else None
    })
summary = data.get("summary", {})
passed = int(summary.get("passed", sum(t["result"] == "passed" for t in tests)))
failed = int(summary.get("failed", sum(t["result"] == "failed" for t in tests)))
total = int(summary.get("total", len(tests)))
status = "passed" if failed == 0 and total > 0 else "failed"
report = {
    "repository": os.environ.get("GITHUB_REPOSITORY", "local"),
    "branch": os.environ.get("GITHUB_REF_NAME", "local"),
    "commit_sha": os.environ.get("GITHUB_SHA", "local"),
    "pipeline_run_id": os.environ.get("GITHUB_RUN_ID", "local"),
    "execution_timestamp": datetime.now(timezone.utc).isoformat(),
    "tests": tests,
    "summary": {"total": total, "passed": passed, "failed": failed, "status": status}
}
Path("testreport.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
sys.exit(0 if status == "passed" else 1)
