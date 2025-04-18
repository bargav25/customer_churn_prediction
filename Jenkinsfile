pipeline{

    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT="robust-cycle-453405-b2"
        GCLOUD_PATH="/var/jenkins_home/google-cloud-sdk/bin"
    }
    
    stages {
        stage('Cloning Github repo to Jenkins'){

            steps{
                script{

                    echo "Cloning Github repo to Jenkins"
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/bargav25/customer_churn_prediction.git']])
                }
            }
        }

       stage('Setup Python Virtual Environment'){

            steps{
                script{

                    echo "Setting up Python Virtual Environment and Installing dependencies"
                    sh '''
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

       stage('Building and Pushing Docker Image to GCR'){

            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo "Building and Pushing Docker Image to GCR"
                        sh '''

                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/customer_churn_prediction:latest .
                        docker push gcr.io/${GCP_PROJECT}/customer_churn_prediction:latest
                        
                        '''

                    }
                }
       
            }
        }

       stage('Deploy to Google Cloud Run'){

            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo "Deploying to Google Cloud Run"
                        sh '''

                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy customer-churn-prediction \
                            --image gcr.io/${GCP_PROJECT}/customer_churn_prediction:latest \
                            --platform managed \
                            --region us-central1 \
                            --allow-unauthenticated \
            
                        '''

                    }
                }
       
            }
        }

    }
}