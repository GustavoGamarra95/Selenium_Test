pipeline {
    agent any

    environment {
        REPORTS_DIR = 'reports'
        ALLURE_RESULTS = "${REPORTS_DIR}/allure-results"
        ALLURE_REPORT = "${REPORTS_DIR}/allure-report"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t qa-tests .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm -v $(pwd)/reports:/app/reports qa-tests ./generate_html_report.sh'
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh '''
                    docker run --rm \
                        -v "$PWD/${ALLURE_RESULTS}:/allure-results" \
                        -v "$PWD/${ALLURE_REPORT}:/allure-report" \
                        frankescobar/allure \
                        generate /allure-results -o /allure-report
                '''
                archiveArtifacts artifacts: "${ALLURE_REPORT}/**", allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: "${REPORTS_DIR}/**", allowEmptyArchive: true
        }
    }
}
