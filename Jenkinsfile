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
        timeout(time: 15, unit: 'MINUTES')
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

        stage('Esperar imagen en ACR') {
            steps {
                powershell '''
                    $ErrorActionPreference = 'Stop'
                    $maxAttempts = 30

                    for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
                        & docker manifest inspect $env:DEPLOY_IMAGE *> $null

                        if ($LASTEXITCODE -eq 0) {
                            Write-Host "Imagen disponible en ACR: $env:DEPLOY_IMAGE"
                            exit 0
                        }

                        Write-Host "Imagen aun no disponible. Intento $attempt de $maxAttempts."
                        Start-Sleep -Seconds 10
                    }

                    throw "La imagen $env:DEPLOY_IMAGE no aparecio en ACR dentro del tiempo esperado."
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
                    Invoke-KubectlCommand apply -f k8s/service.yaml

                    $deploymentManifest = & kubectl set image -f k8s/deployment.yaml devops-app=$env:DEPLOY_IMAGE --local -o yaml
                    if ($LASTEXITCODE -ne 0) {
                        throw "No fue posible preparar el Deployment con la imagen $env:DEPLOY_IMAGE"
                    }

                    $deploymentManifest | & kubectl apply -f -
                    if ($LASTEXITCODE -ne 0) {
                        throw "No fue posible aplicar el Deployment"
                    }
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
