pipeline {
    agent any

    environment {
        KUBE_CONTEXT = 'docker-desktop'
        KUBE_NAMESPACE = 'devops-app'
        DEPLOYMENT_NAME = 'devops-app'
        ACR_IMAGE = 'acrfundev.azurecr.io/app-cicdfundev'
    }

    triggers {
        pollSCM('* * * * *')
    }

    options {
        timeout(time: 10, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.IMAGE_TAG = powershell(
                        returnStdout: true,
                        script: '(git rev-parse HEAD).Trim()'
                    ).trim()
                    env.DEPLOY_IMAGE = "${env.ACR_IMAGE}:${env.IMAGE_TAG}"
                    echo "Imagen a desplegar: ${env.DEPLOY_IMAGE}"
                }
            }
        }

        stage('Validar Kubernetes') {
            steps {
                powershell '''
                    $ErrorActionPreference = 'Stop'
                    function Invoke-KubectlCommand {
                        & kubectl @args
                        if ($LASTEXITCODE -ne 0) {
                            throw "kubectl finalizo con codigo $LASTEXITCODE"
                        }
                    }

                    Invoke-KubectlCommand config use-context $env:KUBE_CONTEXT
                    Invoke-KubectlCommand get namespace $env:KUBE_NAMESPACE
                    Invoke-KubectlCommand get secret acr-secret --namespace $env:KUBE_NAMESPACE
                '''
            }
        }

        stage('Desplegar') {
            steps {
                powershell '''
                    $ErrorActionPreference = 'Stop'
                    function Invoke-KubectlCommand {
                        & kubectl @args
                        if ($LASTEXITCODE -ne 0) {
                            throw "kubectl finalizo con codigo $LASTEXITCODE"
                        }
                    }

                    Invoke-KubectlCommand apply -f k8s/namespace.yaml
                    Invoke-KubectlCommand apply -f k8s/deployment.yaml
                    Invoke-KubectlCommand apply -f k8s/service.yaml
                    Invoke-KubectlCommand set image deployment/$env:DEPLOYMENT_NAME devops-app=$env:DEPLOY_IMAGE --namespace $env:KUBE_NAMESPACE
                '''
            }
        }

        stage('Validar rollout') {
            steps {
                powershell '''
                    $ErrorActionPreference = 'Stop'
                    function Invoke-KubectlCommand {
                        & kubectl @args
                        if ($LASTEXITCODE -ne 0) {
                            throw "kubectl finalizo con codigo $LASTEXITCODE"
                        }
                    }

                    Invoke-KubectlCommand rollout status deployment/$env:DEPLOYMENT_NAME --namespace $env:KUBE_NAMESPACE --timeout=5m
                    Invoke-KubectlCommand wait deployment/$env:DEPLOYMENT_NAME --namespace $env:KUBE_NAMESPACE --for=condition=Available --timeout=60s
                    Invoke-KubectlCommand get deployment $env:DEPLOYMENT_NAME --namespace $env:KUBE_NAMESPACE
                '''
            }
        }
    }
}
