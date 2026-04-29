# Continuous Integration for Dockerized Application

## Scenario

Developers want automated builds whenever code is pushed to GitHub.

## Objective

Implement a Continuous Integration (CI) pipeline using Jenkins.

## Requirements

- Jenkins pipeline triggered via webhook
- Build application
- Build Docker image
- Run container tests
- Push image to Docker registry

## Workflow

```
Developer → GitHub → Webhook → Jenkins → Docker Build → Test → Push to Docker Hub
```

## Application Setup

### Install Dependencies

```bash
sudo apt install python3-pip -y
pip3 install fastapi uvicorn
```

### Run Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Access Output

```
http://<your-vm-ip>:8000
```

Output:

```json
{"message": "DevOps CI Pipeline Running"}
```

## Docker Setup

### Build Image

```bash
docker build -t docker-ci .
```

### Run Container

```bash
docker run -d -p 8000:8000 docker-ci
```

## GitHub Setup

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<your-username>/devops-proj1.git
git branch -M main
git push -u origin main
```

## Jenkins Setup

* Install Jenkins
* Install plugins: Git, Pipeline, Docker

### Configure Pipeline

* SCM: Git
* Repository: your GitHub repo
* Branch: main

### Enable Trigger

GitHub hook trigger for GITScm polling

## Jenkinsfile

The Jenkinsfile defines the CI pipeline stages:

* Build Docker image
* Run container test
* Push image to Docker Hub

## Webhook Setup 
- purpose of webhook: to notify Jenkins of code changes in GitHub, triggering the CI pipeline automatically.
- how ngrok is linked via webhook: ngrok provides a public URL that forwards requests to the local Jenkins server, allowing GitHub to trigger the Jenkins pipeline even if it's running on a local machine.
- how ngrok connects with Jenkins: ngrok creates a secure tunnel to the local Jenkins server, enabling it to receive webhook events from GitHub and trigger the CI pipeline accordingly.
- how local url is connected to jenkins: Jenkins is configured to listen for incoming webhook requests on a specific endpoint (e.g., /github-webhook/). Ngrok forwards the requests from the public URL to this local Jenkins endpoint, allowing Jenkins to process the webhook events and execute the CI pipeline.

In GitHub:

* Go to Settings → Webhooks → Add Webhook

Payload URL:

```
https://<ngrok-url>/github-webhook/
```

Note: Local IP (192.168.x.x) will not work. Use ngrok for public access.

## Ngrok Setup (for local Jenkins)

```bash
sudo apt install unzip -y
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip
unzip ngrok-v3-stable-linux-amd64.zip

./ngrok config add-authtoken <your-token>
./ngrok http 8080
```

## Final Output

* Jenkins pipeline execution logs
* Docker image available in Docker Hub
* Running application via Docker container


### FINAL FLOW:
Whenever code is pushed to GitHub:

* Jenkins is triggered via webhook
* Application is built
* Docker image is created
* Container is tested
* Image is pushed to Docker Hub


git add .
git commit -m "Test Commit"
git push -u origin main



# Incase of Disk Space issue:

## Issue: 
Your Jenkins server stores:

Build workspaces
Docker images
Containers
Build logs
Git clones
Cache files

Over time these fill disk space.

Your node becomes: offline until storage is cleaned.

Thus RUN: 

docker system prune -a -f
sudo rm -rf /var/lib/jenkins/workspace/*
sudo systemctl restart jenkins

Check space: df -h 

TEST