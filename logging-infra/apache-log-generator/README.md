# Apache log generator (Generates dummy logs based on configuration files)

### Introduction
Dockerfile to build an [log-generator](https://pypi.org/project/log-generator/).

Run in docker
~~~~~~~~~~~~~
    $ mkdir workdir
    $ cd workdir
    $ git clone https://github.com/prabhatmaurya/plabs-sre-admin.git
    $ cd apache-log-generator
    $ docker-compose up [--build] -d
~~~~~~~~~~~~~

Run in minikube
~~~~~~~~~~~~~~~
    $ mkdir workdir
    $ cd workdir
    $ git clone https://github.com/prabhatmaurya/plabs-sre-admin.git
    $ cd apache-log-generator
    $ minikube start
    $ eval $(minikube docker-env)
    $ docker-compose build
    $ kubectl create -f pod.yaml
    $ kubectl get pods
