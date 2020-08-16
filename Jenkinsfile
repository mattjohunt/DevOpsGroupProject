pipeline{
	agent any
	environment {
		ORG = "hazardd"
		CUR_PRIZE_VER = "big"
		NEW_PRIZE_VER = "big"
		CUR_NUM_VER = "big"
		NEW_NUM_VER = "big"
		CUR_TEXT_VER = "upper"
		NEW_TEXT_VER = "upper"		
	}
	stages{	
		stage('Build Client'){
                        steps{
				sh 'sudo docker build ./client/. -t $ORG/client:v1'
                        }
                }
                stage('Build Server'){
                        steps{
				sh 'sudo docker build ./server/. -t $ORG/server:v1'				
                        }
                }
		stage('Build Textgens'){
			steps{
				sh 'sudo docker build ./textgen-lower/. -t $ORG/textgen:lower'
				sh 'sudo docker build ./textgen-upper/. -t $ORG/textgen:upper'
			}
		}
		stage('Build Numgens'){
                        steps{
                                sh 'sudo docker build ./numgen_small/. -t $ORG/numgen:small'
                                sh 'sudo docker build ./numgen_big/. -t $ORG/numgen:big'
                        }
                }
		stage('Build Prizegens'){
                        steps{
                                sh 'sudo docker build ./prizegen-small/. -t $ORG/prizegen:small'
                                sh 'sudo docker build ./prizegen-big/. -t $ORG/prizegen:big'
                        }
                }
		stage('Build Notification Server'){
			steps{
				sh 'sudo docker build ./notification_server/. -t $ORG/notification_server:v2'
			}
		}
		stage('Build DB Connector'){
                        steps{
                                sh 'sudo docker build ./db_connector/. -t $ORG/db-connector:v1'
                        }
                }
                stage('Push'){
                        steps{
                                sh 'sudo docker push $ORG/client:v1'
				sh 'sudo docker push $ORG/server:v1'
				sh 'sudo docker push $ORG/textgen:lower'
				sh 'sudo docker push $ORG/textgen:upper'
				sh 'sudo docker push $ORG/numgen:small'
				sh 'sudo docker push $ORG/numgen:big'
				sh 'sudo docker push $ORG/prizegen:small'
				sh 'sudo docker push $ORG/prizegen:big'
				sh 'sudo docker push $ORG/notification_server:v2'
				sh 'sudo docker push $ORG/db-connector:v1'
                        }
                }
		stage('Clean Nginx'){
			steps{
				sh "kubectl delete -f ./nginx/config-map.yaml"
				sh "kubectl delete -f ./nginx/deployment.yaml"
			}
		}
		stage('Clean Prize Gen'){
			steps{
				sh "kubectl delete -f ./prizegen-$CUR_PRIZE_VER/. --all"
			}
		}
		stage('Clean Notification Server'){
			steps{
				sh "kubectl delete -f ./notification_server/. --all"
			}
		}
		stage('Clean Textgen'){
                        steps{
                                sh "kubectl delete -f ./textgen-$CUR_TEXT_VER/. --all"
                        }
                }
		stage('Clean Numgen'){
                        steps{
                                sh "kubectl delete -f ./numgen_$CUR_NUM_VER/. --all"
                        }
                }
		stage('Clean Server'){
			steps {
				sh "kubectl delete -f ./server/. --all"
			}
		}
		stage('Clean Client'){
			steps {
				sh "kubectl delete -f ./client/service.yaml --all"
				sh "kubectl delete -f ./client/deployment.yaml --all"
			}
		}
		stage('Run Mongo'){
			steps{
				sh "kubectl apply -f mongo/pod.yaml -f mongo/service.yaml"
			}
		}
		stage('Run DB Connector'){
			steps{
				 sh "kubectl apply -f db_connector/pod.yaml -f db_connector/service.yaml"
			}
		}
		stage('Run Prize Gen'){
                        steps{
                                sh "kubectl apply -f ./prizegen-$NEW_PRIZE_VER/."
                        }
                }
                stage('Run Notification Server'){
                        steps{
                                sh "kubectl apply -f ./notification_server/."
                        }
                }
                stage('Run Server'){
                        steps{
                                sh "kubectl apply -f ./server/."
                        }
                }
                stage('Run Textgen'){
                        steps{
                                sh "kubectl apply -f ./textgen-$NEW_TEXT_VER/."
                        }
                }
                stage('Run Numgen'){
                        steps{
                                sh "kubectl apply -f ./numgen_$NEW_NUM_VER/."
                        }
                }
		stage('Run Client'){
			steps{
				sh "kubectl apply -f ./client/service.yaml"
				sh "kubectl apply -f ./client/deployment.yaml"
			}
		}
		stage('Run Nginx'){
			steps{
				sh "kubectl apply -f ./nginx/."
			}
		}		
	}
}
