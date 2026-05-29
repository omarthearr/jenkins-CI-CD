pipeline {
    agent any
    environment {
        REGISTRY = '172.31.29.90:5000'
        IMAGE_NAME = 'cargasdeployment2025'
        VERSION = "v${BUILD_NUMBER}"
        USER_PROD = 'ubuntu'
        SERVER_PROD = '172.31.29.90'
        DEPLOY_PATH = '/home/ubuntu/cargasdeployment2025'
    }
    triggers {
        githubPush()
    }
    stages {
        stage('Inicializando...') {
            steps {
                echo 'Asignando workspace y validando entorno.'
            }
        }
        stage('Construir imagen produccion') {
            steps {
                sh "docker build -t ${REGISTRY}/${IMAGE_NAME}:${VERSION} -f Dockerfile-prod ."
                sh "docker tag ${REGISTRY}/${IMAGE_NAME}:${VERSION} ${REGISTRY}/${IMAGE_NAME}:latest"
            }
        }
        stage('Push de imagen a registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'registry-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin ${REGISTRY}
                        docker push ${REGISTRY}/${IMAGE_NAME}:${VERSION}
                        docker push ${REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }
        stage('Desplegar en produccion') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'registry-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${USER_PROD}@${SERVER_PROD} "
                            cd ${DEPLOY_PATH} &&
                            echo \\"\$DOCKER_PASS\\" | docker login -u \\"\$DOCKER_USER\\" --password-stdin ${REGISTRY} &&
                            docker compose -f docker-compose.prod.yml pull &&
                            docker compose -f docker-compose.prod.yml up -d
                        "
                    """
                }
            }
        }
    }
    post {
        always {
            sh "docker rmi ${REGISTRY}/${IMAGE_NAME}:${VERSION} || true"
            sh "docker rmi ${REGISTRY}/${IMAGE_NAME}:latest || true"
            sh 'docker system prune -f || true'
        }
        success {
            echo "Pipeline completado exitosamente con version ${VERSION}"
        }
        failure {
            echo "El pipeline fallo en algun paso."
        }
    }
}
