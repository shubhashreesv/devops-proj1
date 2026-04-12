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
