pipeline {
    agent any
    environment {
        REGISTRY = '34.238.238.115:5000'
        IMAGE_NAME = 'cargasdeployment2025'
        VERSION = "v${BUILD_NUMBER}"
        USER_PROD = 'ubuntu'
        SERVER_PROD = '34.238.238.115'
        DEPLOY_PATH = '/home/ubuntu/cargasdeployment2025'
    }
    stages {
        stage('Inicializando...') {
            steps {
                echo 'Asignando workspace y validando entorno.'
            }
        }
        stage('Entorno de desarrollo') {
            steps {
                sh 'docker compose up -d --build'
            }
        }
        stage('Analisis de codigo') {
            steps {
                sh 'docker exec cargas_academicas_app flake8 --max-complexity=10 --max-line-length=200 --ignore=F811,E402 .'
            }
        }
        stage('Pruebas unitarias') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    sleep time: 20, unit: 'SECONDS'
                    sh 'docker exec cargas_academicas_app python3 manage.py test'
                    sh """docker exec cargas_academicas_app bash -c "coverage run --branch --source='.' --omit=*test*,*migrations*,*__init*,*settings*,*apps*,*wsgi*,*admin.py,*asgi.py,manage.py,*urls.py manage.py test" """
                    sh 'docker exec cargas_academicas_app coverage html'
                    sh 'docker cp cargas_academicas_app:/app/htmlcov .'

                    publishHTML target:[
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: './htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Reporte de cobertura Cargas académicas',
                        reportTitles: 'Cobertura de código'
                    ]
                }
            }
        }

        stage('Pruebas de aceptacion') {
            steps {
                sh 'docker exec cargas_academicas_app python manage.py migrate'
                sh 'docker exec cargas_academicas_app python create_superuser.py'
                sh 'docker exec cargas_academicas_app bash -c "python manage.py runserver 0:8000 &"'
                sh 'docker exec -w /pruebas_aceptacion cargas_academicas_app behave features/login.feature'
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
                sh """
                    ssh -o StrictHostKeyChecking=no ${USER_PROD}@${SERVER_PROD} '
                        cd ${DEPLOY_PATH}
                        docker login -u admin -p admin123 ${REGISTRY}
                        docker compose -f docker-compose.prod.yml pull
                        docker compose -f docker-compose.prod.yml up -d
                    '
                """
            }
        }
        stage('Revision por QA') {
            steps {
                input "Desplegar en produccion?"
            }
        }
    }
    post {
        always {
            sh 'docker compose down -v'
        }
        success {
            echo "Pipeline completado exitosamente con version ${VERSION}"
        }
        failure {
            echo "El pipeline fallo en algun paso."
        }
    }
}
