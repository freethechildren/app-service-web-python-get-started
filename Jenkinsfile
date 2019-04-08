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
    DOCKER_REPO_NAME='rbc-devops/sample-django'
    BUILD_TAG='latest'
    DOCKER_REGISTRY_CREDS = credentials('platform-docker-registry')
    DNS_NAME_LABEL = "rbc-devops-sample-dev"
    JENKINS_SP_PW = credentials('platform-docker-registry')
    JENKINS_SP_NAME = 'jenkins_sp'
    RESOURCE_GROUP = 'weorg-dev'
    APP_NAME = "rbc-devops-sample-dev"
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
    stage('Build the container') {
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
            // sh 'flake8 .'
            // sh 'pytest --tb=short --cov=./ tests/'
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
    stage("Deploy container to chosen deploy") {
      agent {
        docker {
          image 'microsoft/azure-cli'
          args '-v $HOME/.jenkins/:/tmp'
        }
      }
    //   environment {

        // env.MQ_HOST = "wetl-main-queue-dev.redis.cache.windows.net"
        // env.MQ_PORT = '6380'
        // env.MQ_DATABASE = '0'
        // env.MQ_CREDS_ID = "wetl-main-queue-dev"
        // SF_URL = 'https://we--danbox.cs62.my.salesforce.com'
        // env.SF_CREDS_ID = "pyth_sf_danbox_creds"
        // env.SF_TOKEN_ID = "pyth_sf_danbox_token"
        // env.SF_DOMAIN = 'test'
        // env.SENTRY_DSN = 'https://3d8842518bc74291840d42a501825f26@sentry.io/1404060'


        // MQ_CREDS = credentials("${MQ_CREDS_ID}")
        // SF_CREDS = credentials("${SF_CREDS_ID}")
        // SF_TOKEN = credentials("${SF_TOKEN_ID}")
    //   }
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
          sh """
          az container create  \
            -g ${RESOURCE_GROUP} \
            --name ${APP_NAME} \
            --image ${DOCKER_REGISTRY}/${DOCKER_REPO_NAME}:${BUILD_TAG} \
            --registry-username ${DOCKER_REGISTRY_CREDS_USR} \
            --registry-password "${DOCKER_REGISTRY_CREDS_PSW}" \
            --ip-address public \
            --dns-name-label ${DNS_NAME_LABEL} \
            --verbose
          """
          sh """
          az container restart \
            --verbose \
            -g ${RESOURCE_GROUP} \
            --name ${APP_NAME}
          """
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