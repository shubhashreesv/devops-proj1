pipeline {
    agent any

    environment {
        IMAGE_NAME = "shubhashreesv/docker-ci"
        CONTAINER_NAME = "test-container"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Run Container Test') {
            steps {
                sh '''
                docker rm -f test-container || true

                docker run -d \
                --name test-container \
                -p 8001:8000 \
                $IMAGE_NAME

                docker logs test-container || true
                echo "Waiting for FastAPI startup..."

                for i in {1..20}
                do
                    sleep 3

                    if curl -f http://localhost:8001/health; then
                        echo "Health check passed"
                        exit 0
                    fi

                    echo "Retrying health check..."
                done

                echo "Health check failed"
                exit 1
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'USER',
                        passwordVariable: 'PASS'
                    )
                ]) {

                    sh '''
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push $IMAGE_NAME
                    '''
                }
            }
        }
    }

    post {

        always {
            sh '''
            docker stop $CONTAINER_NAME || true
            docker rm $CONTAINER_NAME || true
            '''
        }

        success {
            sh '''
            docker rm -f prod-container || true

            docker run -d \
            -p 8002:8000 \
            --name prod-container \
            $IMAGE_NAME
            '''
        }
    }
}