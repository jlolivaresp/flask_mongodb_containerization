# Kubernetes Containerization: Python + MongoDB

A basic project to deploy locally two containers to Kubernetes as micro-services:

* A Python/Flask app, with a web API, that queries 3 "ways" from the Open Street Map Overpass API and stores their associated
nodes to a MongoDB database.

* A MongoDB database.

The configuration files for deployment of both services on Docker are included. Be aware that Docker requires making the 
node ports available to each other for them to communicate.

## Project Structure

The project structure is the following:

```console
osm/
├── app/
│   ├── __init__.py
│   ├── docker-compose.yaml
│   ├── Dockerfile
│   ├── kubernetes/
│   │   ├── flask-deployment.yaml
│   │   └── flask-service.yaml
│   ├── main.py
│   ├── model/
│   │   ├── __init__.py
│   │   └── way.py
│   ├── requirements.txt
│   └── services/
│       ├── __init__.py
│       ├── mongodb.py
│       └── overpass.py
├── database/
│   ├── docker/
│   │   └── docker-compose.yaml
│   └── kubernetes/
│       ├── mongodb-data-persistentvolume.yaml
│       ├── mongodb-data-persistentvolumeclaim.yaml
│       ├── mongodb-data-secrets.yaml
│       ├── mongodb-service-deployment.yaml
│       └── mongodb-service-service.yaml
├── kubernetes/
│   └── osm-ingress.yaml
└── README.md
```

## Requirements

* [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Kubectl]((https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-linux/))
* [Minkube](https://kubernetes.io/docs/tasks/tools/install-minikube/)
* Conntrack

For this last one, run the following commands in a terminal window:
```console
$ sudo apt-get update -y
$ sudo apt-get install -y conntrack
```


## Installation

Once you have installed the required software, proceed with the following steps:

### General

#### Start minikube

   In a terminal window, run the following command:

   ```console
   $ minikube start --driver=<driver_name>
   ```
   
   If using driver=none, the above command must be ran as root user.

### MongoDB micro-service

#### Deploy to Kubernetes
   Run the following commands in a terminal:

   ```console
   $ mkdir -p $HOME/.kube
   $ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   $ sudo chown $(id -u):$(id -g) $HOME/.kube/config
   $ cd <YOUR_PATH>/osm/database/kubernetes
   $ kubectl apply -f mongodb-data-persistentvolume.yaml
   $ kubectl apply -f mongodb-data-persistentvolumeclaim.yaml
   $ kubectl apply -f mongodb-data-secrets.yaml
   $ kubectl apply -f mongodb-service-service.yaml
   $ kubectl apply -f mongodb-service-deployment.yaml
   ```

   You should see the following messages printed:

   ```console
   persistentvolume/mongodb-data configured
   persistentvolumeclaim/mongodb-data configured
   secret/mongodb-credentials created
   deployment.apps/mongodb-service created
   service/mongodb-service configured
   ```

   To check that your micro-service is running, run the following command:

   ```console
   $ kubectl get pods
   ```

   After this, you should see:

   ```console
   NAME                              READY   STATUS    RESTARTS   AGE
   mongodb-service-c898b6bb4-5dv5k   1/1     Running   1          2s
   ```

### Python-Flask micro-service
   
#### Build the image for the python app

   Run the following commands:

   ```console
   $ cd <YOUR_PATH>/osm/app/
   $ sudo docker build -f Dockerfile -t python:latest .
   ```

#### Deploy to Kubernetes

   ```console
   $ cd <YOUR_PATH>/osm/app/kubernetes
   $ for file in flask*; do kubectl apply -f $file; done
   ```
   You should see the following messages printed:

   ```console
   deployment.apps/flask created
   service/flask configured
   ```

   To check that your micro-service is running, run the following command:

   ```console
   $ kubectl get pods
   ```

   After this, you should see:

   ```console
   NAME                               READY   STATUS    RESTARTS   AGE
   mongodb-service-c898b6bb4-79xsj     1/1     Running   0          2m
   flask-7d7894dc77-bfl8p              1/1     Running   0          3s
   ```

### Ingress configuration

   Execute the following commands:
   
   ```console
   # Enable the Ingress addon:
   $ minikube addons enable ingress
   
   $ cd <YOUR_PATH>/osm/kubernetes
   
   # Add an entry to /etc/hosts:
   $ echo "$(minikube ip) osm.project" | sudo tee -a /etc/hosts

   # Create the Ingress object:
   $ kubectl apply -f osm-ingress.yaml
   ```
   
## Usage

Now that both pods are running, you can hit the web service at the following endpoint from your browser:

[htttp://osm.project](htttp://osm.project)

If it doesn't work, try copying: htttp://osm.project in your browser.

If everything works, you should see a JSON response like:

```json
{
  "2388248": "{'_id': ObjectId('5eec5705af5b31dc7aa221d2'), 'nodes': []}",
  "253408665": "{'_id': ObjectId('5eec5705af5b31dc7aa221d3'), 'nodes': [2593331116, 2593331150, 2593331151, 2593331117, 2593331116]}",
  "4848900793": "{'_id': ObjectId('5eec5705af5b31dc7aa221d1'), 'nodes': [5346360238, 5346398330, 5346482962, 5346379327, 5346360238]}"
}
```

The keys are the "ways" queried and they are composed of the _id (unique identifiers with which the ways and their nodes 
where stored in the DB) and their associated nodes.

## Clean

To stop the minikube server run:

```console
$ minikube stop
```

## Credits

Made by Jorge Luis Olivares.