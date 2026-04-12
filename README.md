# Continuous Integration for Dockerized Application 

## Scenario: 
- Developers want automated builds whenever code is pushed to GitHub. 

## Objective: 
- Implement CI pipeline using Jenkins

## Requirements 
- Jenkins pipeline triggered via webhook 
- Build application 
- Build Docker image d
- Run container tests 
- Push image to Docker registry 

## Deliverables: 
- Jenkinsfile, 
- Dockerfile, 
- Build logs


Whenever code is pushed to GitHub → Jenkins automatically:
- Builds the app
- Creates Docker image
- Tests it
- Pushes to Docker Hub

# Developer → GitHub → Webhook → Jenkins Pipeline → Docker Build → Test → Push to DockerHub


### INSTALLATION COMMANDS:
sudo apt install python3-pip
sudo apt install uvicorn
pip3 install fastapi uvicorn


### RUN:
uvicorn main:app --host 0.0.0.0 --port 8000

### OPEN IN BROWSER:
http://<your-vm-ip>:8000
- You will see {"message":"DevOps CI Pipeline Running"}

### DOCKERFILE SETUP:
touch Dockerfile

<Refere Dockerfile content in the project directory>

docker build -t docker-ci .
docker run -d -p 8000:8000 docker-ci

### INITIALIZE GIT REPO:
git init
git add .
git commit -m "Initial commit - FastAPI Docker CI project"

Go to GitHub > Click New Repository > Setup

git remote add origin https://github.com/<your-username>/devops-ci-project.git
git branch -M main
git push -u origin main

### JENKINS SETUP:
- Install Jenkins on your VM
- Install necessary plugins (Git, Docker, etc.)
- Open http://<your-vm-ip>:8080 and set up Jenkins

Click New Item > Pipeline > OK
Pipeline section > Pipeline script from SCM:
- SCM: Git
- Repository URL: https://github.com/<your-username>/devops-proj1
- Branch: */main

Triggers Section > GitHub hook trigger for GITScm polling 
Save

Note: To Test BUILD Manually: Click Build Now (It will fail if you dont have Jenkins File in the repo)


### GITHUB WEB HOOK SETUP
Go to GitHub Repo > Settings > Webhooks > Add webhook
- Payload URL: http://<your-vm-ip>:8080/github-webhook/


In Jenkins
Open your pipeline job:
Configure → Build Triggers
Enable:GitHub hook trigger for GITScm polling

### ISSUE WITH YOUR IP IN WEBHOOK AND SOLUTION: 
http://192.168.72.129:8080/github-webhook/ -> This IP is not accessible from GitHub servers, so you need to use a public IP 

Solution: Use ngrok to expose your local Jenkins server to the internet

sudo apt install unzip -y

Download: wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip
Unzip: unzip ngrok-v3-stable-linux-amd64.zip

Then RUN: ./ngrok http 8080
You will get a public URL like https://<random-id>.ngrok-free.app

Use this URL in your GitHub webhook setup

NOTE: Have an account in ngrok before this step, and login using ./ngrok authtoken <your-ngrok-auth-token>
