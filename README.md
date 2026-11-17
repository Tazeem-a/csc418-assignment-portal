# CSC418 DevOps Lab Mid — Assignment Submission Portal

A Flask assignment portal with pytest automated tests, GitHub Actions CI, authenticated JSON report delivery to a local receiver, optional email reporting, and a GitHub Pages static demo.

## Requirements

- Python 3.10 or newer
- Git
- A GitHub account and repository
- For local report delivery: Cloudflare Tunnel (`cloudflared`)
- Optional email bonus: Gmail app password and GitHub Actions secrets

## 1. Run in VS Code

Open this folder in VS Code. In the VS Code terminal:

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies and start the portal:

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

Submissions are stored in `submissions.json` beside `app.py`.

## 2. Run automated tests locally

```bash
pytest -v
```

The three required tests cover a valid submission, a missing registration number, and an invalid URL.

## 3. Start the local report receiver

Open a second terminal in the project folder and set a long random token.

**Windows PowerShell**
```powershell
$env:REPORT_TOKEN="replace-with-a-long-random-secret"
python receiver.py
```

**macOS/Linux**
```bash
export REPORT_TOKEN="replace-with-a-long-random-secret"
python receiver.py
```

The receiver listens on `127.0.0.1:8000` and writes received reports to `testreport.json`.

## 4. Expose the receiver to GitHub Actions

Install `cloudflared`, then keep this running in a third terminal:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

Cloudflare prints a temporary `https://....trycloudflare.com` URL. Your receiver endpoint is that URL plus `/report`, for example:

`https://random-name.trycloudflare.com/report`

Do not use `localhost` in GitHub Actions: it would refer to GitHub's runner, not your computer. Keep both `receiver.py` and `cloudflared` running throughout the demonstration. Quick Tunnel URLs can change; update the GitHub secret if yours changes.

## 5. Create GitHub repository and configure secrets

Create an empty GitHub repository, e.g. `csc418-assignment-portal`. In the repository, open **Settings → Secrets and variables → Actions**.

Add these **repository secrets**:

- `LOCAL_REPORT_URL` = your complete Cloudflare URL ending in `/report`
- `REPORT_TOKEN` = exactly the same token used by `receiver.py`

For the optional email bonus, add:

- `MAIL_USERNAME` = your Gmail address
- `MAIL_PASSWORD` = a Gmail App Password (not your normal account password)

Add this **repository variable** for email:

- `REPORT_EMAIL` = recipient email address

The workflow uses Gmail SMTP. App-password availability depends on your Google account security configuration. Never commit credentials into source code.

## 6. Push project to GitHub

```bash
git init
git add .
git commit -m "Initial CSC418 assignment portal"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/csc418-assignment-portal.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Open **Actions** on GitHub to see the workflow.

Every push runs pytest. The workflow creates a report from pytest's JSON output and attempts local delivery even when tests fail. It then marks the job failed if tests failed. Pages deployment is a separate dependent job, so it runs only after the test-and-report job succeeds and only on `main`.

## 7. Demonstrate pass → fail → fix

1. **Passing run:** push the working code. Show the green Actions run and the new `testreport.json` on your computer.
2. **Failing run:** temporarily introduce a defect, e.g. in `app.py` change the URL validation condition so valid URLs are rejected. Commit and push. Show the red Actions run and the received JSON with failed test details.
3. **Fix:** restore the original validation code, commit, and push. Show the green run and updated local JSON.

Do not fake report data. The JSON is generated from the actual pytest execution.

## 8. GitHub Pages bonus

In GitHub repository **Settings → Pages**, choose **GitHub Actions** as the build/deployment source. Push to `main` after enabling Pages. The workflow publishes the `docs/` folder only when tests pass. The Pages site is a static demonstration and stores demo submissions in the visitor's browser; the full Flask app remains the server-backed portal.

The deployed URL normally looks like:

`https://YOUR-USERNAME.github.io/csc418-assignment-portal/`

## Report structure

`testreport.json` contains repository, branch, commit SHA, workflow run ID, execution timestamp, each test's name/result/failure message, and total/passed/failed/overall status. The receiver also adds `received_at`.

## Troubleshooting

- **No local report:** check that receiver and tunnel are both running; verify the secret URL ends in `/report`; ensure `REPORT_TOKEN` matches exactly.
- **Tunnel URL changed:** restart `cloudflared` and update `LOCAL_REPORT_URL` in GitHub Secrets.
- **401 Unauthorized:** receiver token and GitHub secret differ.
- **Pages not deploying:** enable GitHub Pages with GitHub Actions as source and confirm the workflow ran on `main` with passing tests.
- **Email not sent:** check the Gmail app password, recipient variable, and Actions log. Email is optional; local JSON delivery is a core requirement.

## Security note

This is a teaching project. Use a strong random report token, keep secrets in GitHub Actions settings, and do not expose the Flask student portal publicly without production security controls.
155c0228bc34c0e4120a80da616657ed8b4ef34d527c1454933016e258a21119$env:REPORT_TOKEN="YAHAN_APNA_NAYA_TOKEN_PASTE_KARO"

cloudflared tunnel --url http://localhost:8000
https://vocal-specialist-curious-train.trycloudflare.com   