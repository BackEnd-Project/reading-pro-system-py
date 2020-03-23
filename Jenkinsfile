pipeline {
  agent any

  environment {
      docker_tag= "dev"
      docker_release_tag= "1.0.0"
      docker_images= "social-sp-api"
      docker_registry= "registry.cn-shenzhen.aliyuncs.com"
      docker_registry_release= "registry-intl.cn-shanghai.aliyuncs.com"
      docker_registry_library= "smkj"
      docker_registry_library_release= "doo-release"
      docker_registry_user= "szsongmaokeji"
      docker_registry_pass= "8lvDGNpl4h"
      docker_registry_user_release= "dooholding@gmail.com"
      docker_registry_pass_release= "y3rqDcSsShp76QeC"
  }

  stages {
    stage('Input') {
      steps {
        script {
          myStage = input message: 'What stage do you want to run now?', parameters: [choice(choices: 'Prepare\nDev\nRelease', description: '', name: 'Stage')]
        }

        echo myStage
      }
    }
    stage('Prepare') {
      when {
        expression {
          myStage == 'Prepare'
        }

      }
      steps {
        echo "Currently in branch ${env.BRANCH_NAME}"
      }
    }
    stage('Dev') {
      when {
        expression {
          myStage == 'Dev'
        }

      }
      steps {
        echo 'Test Stage'
        sh "docker login $docker_registry -u $docker_registry_user -p $docker_registry_pass"
        sh "docker build -t $docker_images:$docker_tag . --no-cache"
        sh "docker tag $docker_images:$docker_tag $docker_registry/$docker_registry_library/$docker_images:$docker_tag"
        sh "docker push $docker_registry/$docker_registry_library/$docker_images:$docker_tag"
      }
    }
    stage('Release') {
      when {
        expression {
          myStage == 'Release'
        }

      }
      steps {
        echo 'Release Stage'
        sh "docker login $docker_registry_release -u $docker_registry_user_release -p $docker_registry_pass_release"
        sh "docker build -t $docker_images:$docker_release_tag . --no-cache"
        sh "docker tag $docker_images:$docker_release_tag $docker_registry_release/$docker_registry_library_release/$docker_images:$docker_release_tag"
        sh "docker push $docker_registry_release/$docker_registry_library_release/$docker_images:$docker_release_tag"
      }
    }
  }

}
