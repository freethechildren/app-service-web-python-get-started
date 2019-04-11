def app

pipeline {
  agent {
    node {
      label 'master'
      customWorkspace "${env.HOME}/.jenkins/:/tmp"
    }
  }

  environment {
    DEPLOY_BRANCH = 'debug/poulad'
    DOCKER_REGISTRY = 'wedockerregistrydev.azurecr.io'
    DOCKER_REGISTRY_NAME = 'WeDockerRegistryDev'
    DOCKER_REGISTRY_ADDR= "https://${DOCKER_REGISTRY}"
    DOCKER_REPO_NAME='rbc-devops/rbc-flask'
    BUILD_TAG='latest'
    DOCKER_REGISTRY_CREDS = credentials('platform-docker-registry')
    DNS_NAME_LABEL = "rbc-devops-sample-dev"
    JENKINS_SP_NAME = 'jenkins_sp'
    JENKINS_SP_PW = credentials('jenkins_sp_pw')
    RESOURCE_GROUP = 'weorg-dev'
    WEBAPP_NAME = "rbc-devops-sample-dev"
  }

  stages {
    stage('Info and setup') {
      steps {
        // Prints out helpful diagnostics on the build environment
        sh 'printenv'
        sh 'ls -la'
        sh 'pwd'
      }
    }
    stage('Build Docker Image') {
      steps {
        script {
          app = docker.build(env.DOCKER_REPO_NAME)
        }
      }
    }
    stage('Test the container') {
      steps {
        script {
          app.inside {
            sh 'echo TESTS HERE...'
          }
        }
      }
    }
    stage('Push image to Registry & Deploy to dev') {
      when { expression { env.BRANCH_NAME == env.DEPLOY_BRANCH } }
      steps {
        script {
          echo "Recording commit ref"
          sh "echo ${GIT_COMMIT} > .ref"
          docker.withRegistry("$DOCKER_REGISTRY_ADDR", 'platform-docker-registry') {
            app = docker.build(env.DOCKER_REPO_NAME, '-f Dockerfile .')
            app.push("${env.BUILD_TAG}")
          }
        }
      }
    }
    stage('Deploy Docker Image (Development)') {
      agent {
        docker {
          image 'microsoft/azure-cli'
          args '-v $HOME/.jenkins/:/tmp'
        }
      }
      steps {
        script {
            sh """
            az login \
                --service-principal \
                -u http://$JENKINS_SP_NAME \
                -p \"$JENKINS_SP_PW\" \
                --verbose \
                --tenant we.org
            """
            azureWebAppPublish([
                appName: env.WEBAPP_NAME,
                azureCredentialsId: env.JENKINS_SP_NAME,
                dockerImageName: "${env.DOCKER_REGISTRY}/${env.DOCKER_REPO_NAME}",
                dockerImageTag: env.BUILD_TAG,
                dockerRegistryEndpoint: [
                    credentialsId: 'platform-docker-registry',
                    url: "https://${DOCKER_REGISTRY}"
                ],
                publishType: 'docker',
                resourceGroup: env.RESOURCE_GROUP,
                // slotName: env.SLOT,
            ])
        }
      }
    }
    stage('Deploy Docker Image (Development3)') {
      agent {
        docker {
          image 'microsoft/azure-cli'
          args '-v $HOME/.jenkins/:/tmp'
        }
      }
      steps {
        script {
            sh """
            az login \
                --service-principal \
                -u http://$JENKINS_SP_NAME \
                -p \"$JENKINS_SP_PW\" \
                --verbose \
                --tenant we.org
            """
            azureWebAppPublish([
                appName: "${env.WEBAPP_NAME}3",
                azureCredentialsId: env.JENKINS_SP_NAME,
                dockerImageName: "${env.DOCKER_REGISTRY}/${env.DOCKER_REPO_NAME}",
                dockerImageTag: env.BUILD_TAG,
                dockerRegistryEndpoint: [
                    credentialsId: 'platform-docker-registry',
                    url: "https://${DOCKER_REGISTRY}"
                ],
                publishType: 'docker',
                resourceGroup: env.RESOURCE_GROUP,
                // slotName: env.SLOT,
            ])
        }
      }
    }
  }

  post {
    success {
      office365ConnectorSend(
        message: "Sample Django app is Built Successfully",
        status: "SUCCESS",
        webhookUrl: "$PYTH_TEAMS_WEBHOOK",
        color: "6ef449"
      )
    }
    failure {
      office365ConnectorSend(
        message: "Error while building Sample Django app",
        status: "FAILURE",
        webhookUrl: "$PYTH_TEAMS_WEBHOOK",
        color: "d10815"
      )
    }
  }
}