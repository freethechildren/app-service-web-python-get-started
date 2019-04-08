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
    JENKINS_SP_PW = credentials('jenkins_sp_pw')
    JENKINS_SP_NAME = 'jenkins_sp'
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
          docker.withRegistry("$DOCKER_REGISTRY_ADDR", 'we-docker-registry-staging') {
            app = docker.build(env.DOCKER_REPO_NAME, '-f Dockerfile.production .')
            app.push("${env.BUILD_TAG}")
          }
        }
      }
    }
    // stage('Kick off deploy to dev') {
    //   when { expression { env.BRANCH_NAME == env.DEPLOY_BRANCH } }
    //   steps {
    //     build (
    //       job: 'wetl-core-deploy-2',
    //       parameters: [
    //         [$class: 'StringParameterValue', name: 'target', value: "dev"],
    //         [$class: 'StringParameterValue', name: 'image_tag', value: "$BUILD_TAG"]
    //       ],
    //       wait: false,
    //       propagate: false
    //     )
    //   }
    // }
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