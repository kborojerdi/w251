# Homework 3 - Katayoun Borojerdi

For this homework I have split up the ta

In the cloud, you need to provision a lightweight virtual machine (1-2 CPUs and 2-4 G of RAM should suffice) and run an MQTT broker. As discussed above, the faces will need to be sent here as binary messages. Another component will need to be created here to receive these binary files and save them to SoftLayer's Object storage (note that the Swift-compatible object storage is being deprecated in favor of s3-compatible object storage).

# Cloud VM

## Provision VM
I setup up a lightweight VM from my jumpbox using the CLI 

The following command creates the new virutal machine:
```
ibmcloud sl vs create --hostname=faces --domain=storage.cloud --cpu=1 --memory=2048 --datacenter=sjc04 --os=UBUNTU_18_64 --san --disk=100 --key=1689110
```
Once the vm is up and running I find the ip address to ssh in using ``` ibmcloud sl vs list ``` and then I followed the instructions from hw2 in order to harden the VSI and ensure the password login is disabled.  

## Install Docker and Docker-Compose

I followed the instruction from week2 lab2 to install Docker and verify that is working properly
```apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
	
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"	

apt-get update

apt-get install -y docker-ce
```
verify ```docker run hello-world```


### Set IBM Object Storage
Create Object Storage through IBM Cloud service

Add storage

name      value
ID        95633556
FQDN      faces.storage.cloud
created   2020-01-20T13:55:57Z
guid      fdf0fb88-788a-4f2e-93e4-3086443a71acfollowing
IP Addr   169.62.93.58

### Starting the MQTT Broker and Image Processor/Saver on the Cloud VSI
I started with the Mosquitto Broker running on Alipne Linux. I created a Dockerfile.alpine-mqtt and built the docker image with the following command.
```
docker build -t mosquitto -f Dockerfile.alpine-mqtt
```

In order to get the incoming images from the MQTT broker and and save them to the Object Storage. I used a python file to subscribe to the broker and convert the mesages back to an image from bytes and save it to the object storage. I created a Dockerfile based on Ubuntu and added the neccesary apps and build the docker image.
```
docker build -t client -f Dockerfile.opencv-mqtt
```

To make it easy to run all containers I used a docker-compose.yml file to spin up both services at once with the follwoing command.
```
docker-compose up
```

## Starting the MQTT Broker, Forwarder and Image Capture on the jetson TX2
I re-used the Dockerfile from the previous broker. Also the Processor/Saver image can be used for the Image Capture. For the Forwader I found a alpine linux image that included python, and used that as my base image and added Mosquitto as we had done before with the broker. 

Again to make networking and other settings easier, I used a docker-compose.yml file.


[link to sample face](https://s3.us-south.cloud-object-storage.appdomain.cloud/cloud-object-storage-w251-hw3-faces/myface.png)


Submission
Please point us to the repository of your code and provide an http link to the location of your faces in the object storage. Also, explan the naming of the MQTT topics and the QoS that you used.


