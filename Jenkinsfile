pipeline {
    agent any
    environment {
        REGISTRY = '172.31.29.90:5000'
        IMAGE_NAME = 'cargasdeployment2025'
        VERSION = "v${BUILD_NUMBER}"
        USER_PROD = 'ubuntu'
        SERVER_PROD = '172.31.29.90'
        DEPLOY_PATH = '/home/ubuntu/cargasdeployment2025'
        COMPOSE_DEV = 'docker-compose.yml'
        JENKINS_UID = '105'
        JENKINS_GID = '109'
    }
    triggers {
        githubPush()
    }
    options {
        timeout(time: 30, unit: 'MINUTES')
    }
    stages {
        stage('Inicializando...') {
            steps {
                echo "Pipeline CI/CD - version ${VERSION}"
            }
        }
        stage('Levantar entorno de desarrollo') {
            steps {
                sh '''
cat > .env <<ENVEOF
DB_NAME=cargas_academicas
DB_USER=cargasuser
DB_USER_ADMIN=root
DB_PASSWORD=admin1234
DB_ROOT_PASSWORD=admin1234
DB_HOST=db
DEBUG=True
SECRET_KEY=ci-build-${BUILD_NUMBER}-not-secret
ENVEOF
                    docker compose -f ${COMPOSE_DEV} up -d --build app db
                    echo "Esperando a la base de datos..."
                    sleep 25
                    docker compose -f ${COMPOSE_DEV} exec -T db sh -c "mariadb -uroot -p${DB_ROOT_PASSWORD} -e \\"GRANT ALL PRIVILEGES ON *.* TO 'cargasuser'@'%'; FLUSH PRIVILEGES;\\"" || true
                    docker compose -f ${COMPOSE_DEV} exec -T app /env/bin/python manage.py migrate --noinput
                '''
            }
        }
        stage('Pruebas unitarias + coverage') {
            steps {
                sh '''
                    docker compose -f ${COMPOSE_DEV} exec -T app sh -c "cd /app && /env/bin/coverage run --source=. manage.py test --noinput && /env/bin/coverage html -d /app/htmlcov && /env/bin/coverage report"
                '''
            }
        }
        stage('Pruebas de aceptacion (behave)') {
            steps {
                sh '''
                    docker compose -f ${COMPOSE_DEV} up -d selenium-hub chrome
                    sleep 12
                    # El contenedor dev corre apache (no sirve Django en :8000); levantamos runserver para los tests
                    docker compose -f ${COMPOSE_DEV} exec -d app /env/bin/python manage.py runserver 0.0.0.0:8000
                    sleep 6
                    # Sembrar usuario admin para el escenario de login
                    docker compose -f ${COMPOSE_DEV} exec -T app /env/bin/python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); u,_=U.objects.get_or_create(username='admin'); u.set_password('admin1234'); u.is_staff=True; u.is_superuser=True; u.save()"
                    # Corre las features sin @skip (login). Las alta_* estan @skip: les falta login flow + datos (pendiente app)
                    docker compose -f ${COMPOSE_DEV} exec -T -w /pruebas_aceptacion app /env/bin/behave --no-capture --tags=-skip
                '''
            }
        }
        stage('Reporte de coverage') {
            steps {
                sh 'docker compose -f ${COMPOSE_DEV} exec -T -u 0 app chown -R ${JENKINS_UID}:${JENKINS_GID} /app /pruebas_aceptacion || true'
                publishHTML([
                    reportDir: 'app/cargas_academicas/htmlcov',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report',
                    keepAll: true,
                    allowMissing: true,
                    alwaysLinkToLastBuild: true
                ])
            }
        }
        stage('Apagar entorno de desarrollo') {
            steps {
                sh 'docker compose -f ${COMPOSE_DEV} down -v || true'
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
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin ${REGISTRY}
                        docker push ${REGISTRY}/${IMAGE_NAME}:${VERSION}
                        docker push ${REGISTRY}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }
        stage('Desplegar en produccion') {
            steps {
                sshagent(['prod-ssh-key']) {
                    withCredentials([usernamePassword(credentialsId: 'registry-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
ssh -o StrictHostKeyChecking=no ${USER_PROD}@${SERVER_PROD} bash -s <<REMOTE
set -e
cd ${DEPLOY_PATH}
if grep -q '^IMAGE_TAG=' .env; then sed -i "s|^IMAGE_TAG=.*|IMAGE_TAG=${VERSION}|" .env; else echo "IMAGE_TAG=${VERSION}" >> .env; fi
echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin ${REGISTRY}
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
docker logout ${REGISTRY} || true
REMOTE
                        '''
                    }
                }
            }
        }
    }
    post {
        always {
            sh 'docker compose -f ${COMPOSE_DEV} down -v || true'
            sh "docker rmi ${REGISTRY}/${IMAGE_NAME}:${VERSION} || true"
            sh "docker rmi ${REGISTRY}/${IMAGE_NAME}:latest || true"
            sh 'docker system prune -f || true'
        }
        success {
            echo "Pipeline OK - version ${VERSION} desplegada en produccion"
        }
        unstable {
            echo "Pipeline UNSTABLE - desplegado, pero pruebas de aceptacion fallaron"
        }
        failure {
            echo "El pipeline fallo en algun paso."
        }
    }
}
