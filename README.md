# Dev Ops Group Project

This repository is designed to change an already existing system to be reformed into a service/microservice oriented architecture. 

This system is based off of: https://github.com/Matt25969/LAFB

# Contents
1. [Overview](https://github.com/hbuck95/DevOpsGroupProject#dev-ops-group-project)
2. [Original Architecture](https://github.com/hbuck95/DevOpsGroupProject#original-architecture)
3. [New Architecture](https://github.com/hbuck95/DevOpsGroupProject#new-architecture)
4. [CD/CI Pipeline](https://github.com/hbuck95/DevOpsGroupProject#cdci-pipeline)
5. [Jenkins Pipeline](https://github.com/hbuck95/DevOpsGroupProject#jenkins-pipeline)
6. [How to deploy with the Azure Kubernetes Service](https://github.com/hbuck95/DevOpsGroupProject#how-to-deploy-with-the-azure-kubernetes-service)\
6b. [How to swap images in a Kubernetes deployment](https://github.com/hbuck95/DevOpsGroupProject#how-to-swap-images-in-a-kubernetes-deployment)\
6c. [How to setup the Jenkins pipeline in a Kubernetes deployment](https://github.com/hbuck95/DevOpsGroupProject#how-to-setup-the-jenkins-pipeline-for-kubernetes-deployment)
7. [How to deploy using Docker Swarm](https://github.com/hbuck95/DevOpsGroupProject#how-to-deploy-using-docker-swarm)
8. [Known Issues](https://github.com/hbuck95/DevOpsGroupProject#known-issues)
9. [Contributors](https://github.com/hbuck95/DevOpsGroupProject#contributors)


# Original Architecture

The original architecture for the LAFB system is set out as such:

![Original Architecture](http://i.imgur.com/G4ghJRE.png)

The architecture consists of:
  * One database implemented with mLabs (A Mongo database-as-a-service)
  *	A database connector made in Node.js.
  *	A java-based server made using Spring Boot
  *	A notification server using Python
  *	A client (static website) made with Node.js

The reason that the original architecture has been changed is so that the server performs one service. In this architecture the server randomly generates the users account number, interacts with the notification server and serves the API to the static website.

# New Architecture

The current project architecture:
![Current Architecture](http://i.imgur.com/OKcuydy.png)

The new architecture consists of:
  *	A Mongo database
  *	A Node.js database connector
  *	A Java-based server made using Spring Boot
  *	A notification server microservice made with Python
  *	A prize generator microservice made with Python
  *	A number generate microservice made with Python
  *	A text generator microservice made with Python
  *	A client made using Node.js which interacts with the server
  *	A reverse-proxy using Nginx to route traffic
  
# CD/CI Pipeline
![CD/CI Pipeline](http://i.imgur.com/BY7lolH.png)
  
# Jenkins Pipeline
  
The Jenkins pipeline is split into two separate pipelines: initial deployment, and update.

With the initial deployment whenever a push to the current development branch is made, Jenkins, via a webhook, then clones down the project goes through the process of cleaning *(killing)* any active pods and deployments, building each image, pushing the new image to the organisations dockerhub, and finally redeploying all of the pods to the live environment within the Microsoft Azure Kubernetes Service *(az aks)*.

The update pipeline works mostly the same way, however pods are never killed and instead any new images are deployed into the live pods using the 'set image' command meaning that the user experience is never interrupted.

# How to deploy with the Azure Kubernetes Service

Using the Azure CLI ensure you are logged in *(enter credentials if prompted)*:
```
az login
```

Setup a resource a new resource group with a suitable name in the location of your choice, in this example uksouth is chosen:
```
az group create –n lafb-group –l uksouth
```

Setup the Azure Kubernetes Service *(AKS)* and retrieve the credentials:
```
az aks create –n lafb-aks –g lafb-group -l uksouth -–node-count 2
az aks get-credentials –n lafb-aks –g lafb-group
```

Clone down the project and move into its root directory:
```
git clone https://github.com/hbuck95/DevOpsGroupProject
cd DevOpsGroupProject/
```

Now deploy each service to the AKS cluster created previously:
```
kubectl apply –f mongo/

# Ensure that the pod is successfully running before continuing as issues may occur
# It would be good practice to do this each each pod deployment for the steps below.

kubectl get pods

# Please note that some services will take on average of 3-8 minutes to deploy
# Services such as Jenkins and Nginx can take in excess of 10-15 minutes

kubectl apply –f db_connector/
kubectl apply –f prizegen-big/
kubectl apply –f notification_server/
kubectl apply –f server/
kubectl apply –f textgen-upper/
kubectl apply –f numgen_big/
kubectl apply –f client/
kubectl apply –f Jenkins/ # Optional step (Only if you want to deploy Jenkins)
kubectl apply –f nginx/
```

Check that all the pods and services are running correctly:
```
kubectl get pods
kubectl get svc
```

If an error occurs with deployment or a pod fails to deploy (is stuck at 0/1) kill and restart it:
```
# Switch *mongo/* for the service which fails
kubectl delete -f mongo/ 
kubectl apply -f mongo/
```

Wait for the Azure Kubernetes Service to assign an IP to Nginx before continuing.
The IP address will appear in the **EXTERNAL-IP** column in the list of services.
```
kubectl get svc
```

Open ports 80 and 8084 on your node cluster:
```
az vm open-port -g lafb-group -n [NODE_NAME] --port 80
az vm open-port -g lafb-group -n [NODE_NAME] --port 8084
```

Interact with the system by navigating to your assigned URL.
You can also directly retrieve all data in the database and interact with Jenkins *(if installed)* as follows:
```
YOUR_ASSIGNED_IP/server/getAllAccounts
YOUR_ASSIGNED_IP/jenkins
```

## How to swap images in a Kubernetes deployment
Once your kubernetes containers are deployed image updates can be issued using the 'kubectl set image' command as follows:
```
kubectl set image deployment/[DEPLOYMENT] [CONTAINER]=[IMAGE]:[VERSION]
```

e.g:
```
kubectl set image deployment/prizegen prizegen=hazardd/prizegen:big
```


All of the microservice deployments in this project can be updated using the above format as follows:

Prizegen:
  ```
  kubectl set image deployment/prizegen prizegen=hazardd/prizegen:big
  kubectl set image deployment/prizegen prizegen=hazardd/prizegen:small
  ```
  
Textgen:
  ```
  kubectl set image deployment/textgen textgen=hazardd/textgen:upper
  kubectl set image deployment/textgen textgen=hazardd/textgen:lower
  ```
  
Numgen:
  ```
  kubectl set image deployment/numgen numgen=hazardd/numgen:big
  kubectl set image deployment/numgen numgen=hazardd/numgen:small
  ```

## How to setup the Jenkins pipeline for Kubernetes deployment

To setup an instance of Jenkins within Kubernetes you must create a custom Jenkins image with the Azure CLI, Kubernetes, Docker, and Docker-Compose preinstalled, or alternatively use an image which is already configured with these packages and then add a volume mount for the Jenkins home workspace.

Full instructions of how to do this are within the /jenkins .yaml files.

Run your jenkins kubernetes container *(if not already deployed in the above instructions)* with:
```
kubectl apply -f ./jenkins/.
```

Check if it has deployed:
```
kubectl get pods
kubectl get svc
```

This container can take 5-15 minutes to deploy, once deployed it can be accessed using the supplied configuration via:
```
https://[IP_ADDRESS]/jenkins
```

Install and setup Jenkins as normal, once setup then create a pipeline job as you would with any other jenkins job and add a webhook:

Example: ```http://admin:admin@19.96.141.205/jenkins/job/devops/build?token=kubes```\
Usage: ```http://[USER]:[PASS]@[IP][PATH]/job/[JOB]/build?token=[TOKEN]```

Fork this project and ensure that the Jenkins job is pointing the currect github url on the kubernetes or kubernetes-update branch as these branches support jenkins deployment.

Make sure to point the job to look in the project for the Jenkinsfile.

# How to deploy using Docker Swarm

Create a new resource group:
```
az group create -n lafb-swarm -l ukwest
```

Create at least two virtual machines in your new resource group:
```
az vm create -n swarm-manager-1 -g lafb-swarm -l ukwest --image UbuntuLTS
az vm create -n swarm-worker-1 -g lafb-swarm -l ukwest --image UbuntuLTS
```

SSH into one of your newly created machine which will be turned into the manager node:
```
ssh VM_IP_ADDRESS
```

In your VM you will need to install Docker and Docker-compose as follows:

Docker:
```
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker $(whoami)
sudo systemctl enable docker
sudo systemctl start docker
```

After doing the above exit the VM and ssh into it again to ensure the usermod applies:
```
exit
ssh VM_IP_ADDRESS
```

Docker-compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Initialise a swarm:
```
docker swarm init
```

The command printed to the console after completing the above will allow other VMs to join your swarm as a worker node, copy this command because it will be used shortly. If you forget this token it can be retrived by executing the following:
```
docker swarm join-token worker
```

Open ports 80 and 8084:
```
az vm open-port -g lafb-group -n [NODE_NAME] --port 80
az vm open-port -g lafb-group -n [NODE_NAME] --port 8084
```

SSH into the other virtual machine created and execute your join-token created previously.
e.g:
```
  docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377
```

Open ports 80 and 8084 once again before SSHing back into your manager node.

Clone this repository and move into its root directory:
```
git clone https://github.com/hbuck95/DevOpsGroupProject.git
cd DevOpsGroupProject/
```

Deploy this system as a stack:
```
docker stack deploy --compose-file docker-compose.yaml stack-lafb
```

Ensure all the services are running before continuing:
```
docker service ps stack-lafb
```

When each service is running navigate to your assigned IP address to interact with the system:
```
YOUR_ASSIGNED_IP
YOUR_ASSIGNED_IP/server/getAllAccounts
```

In addition, you can update services and issue replicas as follows:
```
docker service update --replicas 2 stack-lafb_nginx
```

# Known Issues
* When initially deploying the project with Jenkins the Jenkins user will successfully deploy the mongo database and db- connector images, however they do not connect and instead these may have to be deleted and then redeployed manually.
We cannot determine how or why this happens but can reproduce  this issue each time.

* The jenkins image used in this project for Kubernetes deployment has been configured incorrectly and has not had the jenkins user added to the docker group, due to this each docker command must be executed with sudo.

  e.g:
  ```sudo docker images```

* With Jenkins deployed in Kubernetes you are required to login to your Dockhub to push to your organisations repository, this login can sometimes timeout and must be recompleted as follows:

  Enter the bash shell within the Jenkins container:
  ```kubectl exec -it jenkins /bin/bash```

  Log back in to your docker account:
  ```sudo docker login``` 

# Contributors
[Harry Buck](https://github.com/hbuck95)\
[Karishma Patel](https://github.com/patelkarishma10)
