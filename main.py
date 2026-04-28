from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
import requests
import docker
import threading
import time
from datetime import datetime
import os
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

LOG_FILE = "logs.txt"

# ---------------------------
# Jenkins Config
# ---------------------------
JENKINS_URL = os.getenv("JENKINS_URL")
CONSOLE_URL = os.getenv("CONSOLE_URL")

JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")

# ---------------------------
# Docker Client
# ---------------------------
docker_client = docker.from_env()

# Prevent duplicate logs
last_console_log = ""
last_docker_logs = {}

# Create log file if missing
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()


# ---------------------------
# Write Logs
# ---------------------------
def write_log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")

    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


# ---------------------------
# GitHub Webhook
# ---------------------------
@app.post("/github-webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    repo = payload.get("repository", {}).get("name", "Unknown")
    pusher = payload.get("pusher", {}).get("name", "Unknown")

    commits = payload.get("commits", [])

    write_log(f"GitHub Push | Repo: {repo} | By: {pusher}")

    for commit in commits:
        msg = commit.get("message")
        author = commit.get("author", {}).get("name")

        write_log(f"Commit by {author}: {msg}")

    return {"status": "received"}


# ---------------------------
# Dashboard
# ---------------------------
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# ---------------------------
# Logs API
# ---------------------------
@app.get("/logs")
async def get_logs():
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()

        return PlainTextResponse("".join(lines[-150:]))

    except Exception:
        return PlainTextResponse("No logs yet")


# ---------------------------
# Jenkins Monitor
# ---------------------------
def monitor_jenkins():
    global last_console_log

    last_build = None

    while True:
        try:
            response = requests.get(
                JENKINS_URL,
                auth=(JENKINS_USER, JENKINS_TOKEN)
            )

            if response.status_code == 200:
                data = response.json()

                build_no = data.get("number")
                building = data.get("building")
                result = data.get("result")

                if build_no != last_build:
                    last_build = build_no

                    if building:
                        write_log(f"Jenkins Build #{build_no} Running")

                    elif result:
                        write_log(f"Jenkins Build #{build_no} Finished -> {result}")

                # Console Logs
                console_response = requests.get(
                    CONSOLE_URL,
                    auth=(JENKINS_USER, JENKINS_TOKEN)
                )

                if console_response.status_code == 200:
                    console_text = console_response.text.strip()

                    if console_text != last_console_log:
                        last_console_log = console_text

                        last_lines = console_text.splitlines()[-5:]

                        for line in last_lines:
                            write_log(f"Jenkins Console: {line}")

        except Exception as e:
            write_log(f"Jenkins Error: {str(e)}")

        time.sleep(5)


# ---------------------------
# Docker Monitor
# ---------------------------
def monitor_docker():
    global last_docker_logs

    while True:
        try:
            containers = docker_client.containers.list()

            for container in containers:
                logs = container.logs(tail=1).decode("utf-8").strip()

                if container.name not in last_docker_logs:
                    last_docker_logs[container.name] = ""

                if logs and logs != last_docker_logs[container.name]:
                    last_docker_logs[container.name] = logs

                    write_log(f"Docker [{container.name}] -> {logs}")

        except Exception as e:
            write_log(f"Docker Error: {str(e)}")

        time.sleep(8)


# ---------------------------
# Background Threads
# ---------------------------
threading.Thread(target=monitor_jenkins, daemon=True).start()
threading.Thread(target=monitor_docker, daemon=True).start()

@app.get("/health")
async def health():
    return {"status": "healthy"}