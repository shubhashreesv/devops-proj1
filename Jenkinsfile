pipeline {
    agent any

    environment {
        IMAGE_NAME = "shubhashreesv/docker-ci"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Container Test') {
            steps {
                sh 'docker run -d --name test-container $IMAGE_NAME'
                sh 'sleep 5'
                sh 'docker exec test-container curl -f http://localhost:8000/health'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push $IMAGE_NAME'
                }
            }
        }
    }

    post {
        always {
            sh 'docker stop test-container || true'
            sh 'docker rm test-container || true'
        }
        success {
            sh 'docker run -d -p 8000:8000 --name prod-container $IMAGE_NAME'
        }
    }
}