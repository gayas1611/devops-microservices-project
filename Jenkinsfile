pipeline {
    agent any
    environment {
        DOCKER_USERNAME = 'shaikgayas'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build and Test') {
            steps {
                sh 'docker-compose build'
                sh 'docker-compose up -d'
                sh 'sleep 10'  // Wait for services to start
                sh 'curl http://localhost:5000/health || exit 1'
                sh 'curl http://localhost:5001/health || exit 1'
                sh 'curl http://localhost:5002/health || exit 1'
                sh 'docker-compose down'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    sh 'docker-compose push'
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/'
                sh 'kubectl get pods'
            }
        }
    }
    post {
        always {
            sh 'docker-compose down'
            sh 'docker logout'
        }
    }
}