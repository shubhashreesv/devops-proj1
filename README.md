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
git commit -m "Initial commit"
git push -u origin main
