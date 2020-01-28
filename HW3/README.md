# Homework 3 - Katayoun Borojerdi

For this homework I have split up the ta

In the cloud, you need to provision a lightweight virtual machine (1-2 CPUs and 2-4 G of RAM should suffice) and run an MQTT broker. As discussed above, the faces will need to be sent here as binary messages. Another component will need to be created here to receive these binary files and save them to SoftLayer's Object storage (note that the Swift-compatible object storage is being deprecated in favor of s3-compatible object storage).

# Part 1: Cloud VM

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

Next to install Docker Compose I ran the following

```sudo curl -L "https://github.com/docker/compose/releases/download/1.25.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose```

## Setup IBM Object Storage

I created the Object Storage through IBM Cloud service website. https://cloud.ibm.com
I did this by going to resource list menu and clicking on the "create resource" blue button on the top right. 
Next, by clicking the storage menu I selected "Object Storage" and select the default "Lite Plan".

Next I mounted the cloud object VSI using the following
```
#Biuld and install package
sudo apt-get update
sudo apt-get install automake autotools-dev g++ git libcurl4-openssl-dev libfuse-dev libssl-dev libxml2-dev make pkg-config
git clone https://github.com/s3fs-fuse/s3fs-fuse.git
Add storage

#Build and install library
cd s3fs-fuse
./autogen.sh
./configure
make
sudo make install
```
Next I went to my object storage and from the service credentials viewed my credentials:

{
  "apikey": "CXTYf2wsfzVXUW1bLnJhSxWn3ko-YczE0MYFqABkN_Fx",
  "cos_hmac_keys": {
    "access_key_id": "b8714174da0e4d6688d7c9534cd06d98",
    "secret_access_key": "7d0354fa191c04c2df7ce86768f72ad35a36f37cc019bc52"
  },


```
echo "<b8714174da0e4d6688d7c9534cd06d98>:<7d0354fa191c04c2df7ce86768f72ad35a36f37cc019bc52>" > $HOME/.cos_creds
chmod 600 $HOME/.cos_creds
```
Finally I created a directory to mount my bucket using the following

```
sudo mkdir -m 777 /mnt/mybucket
sudo s3fs bucketname /mnt/mybucket -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.us-east.objectstorage.softlayer.net
```

## Starting the MQTT Broker and Image Processor/Saver on the Cloud VSI
I started with the Mosquitto Broker running on Alipne Linux. I created a Dockerfile.alpine-mqtt and built the docker image with the following command.
```
docker build -t mqtt-broker -f Dockerfile.mqtt-broker .
```
In order to get the incoming images from the MQTT broker and and save them to the Object Storage. I used a python file to subscribe to the broker and convert the mesages back to an image from bytes and save it to the object storage. I created a Dockerfile based on Ubuntu and added the neccesary apps and build the docker image.
```
docker build -t image-saver -f Dockerfile.opencv-mqtt-image-save .
```

To make it easy to run all containers I used a docker-compose.yml file to spin up both services at once with the follwoing command.
```
docker-compose up
```
# Part 2: Jetson TX2

## Starting the MQTT Broker, Forwarder and Image Capture on the jetson TX2
The same dockerfile use to build the broker on the VM can be re-used on the Jetson. Also the Processor/Saver dockerfile can be used to build the container for face detection. I only had to swap out the python file that subscribes and saves the image, to the file that turns on video from the webcam and detects faces. For the Forwader I found a alpine linux image that included python, and used that as my base image, then added Mosquitto, paho-mqtt and a python file. The python file subscribes to both the local Jetson broker and the remote VM broker. The file then sucribes to a local topic and forwards all messages to the remote broker. 

To build the MQTT Broker on the Jestson I used the following:
```
docker build -t mqtt-broker -f Dockerfile.mqtt-broker .
```

To build the MQTT Forwarder on the Jestson I used the following command:
```
docker build -t mqtt-forwarder -f Dockerfile.mqtt-forwarder .
```

To build the container that turns on the video capture and runs face detection:
```
docker build -t face-detect -f Dockerfile.opencv-mqtt-face-detect .
```

Again to make it easy to run all containers I used a docker-compose.yml file to spin up all three services at once with the follwoing command. I did not start the face detection script to make it easeier to start and stop.
```
docker-compose up
```

To star the video and face detection I used the following command:
```
# need to run xhost only once
xhost + 
docker-compose exec face-detect python video_face_detect.py
```

https://s3.us-south.cloud-object-storage.appdomain.cloud/cloud-object-storage-w251-hw3-faces/face_04e447f4-318f-4686-9446-97ac9bcdde6b.png

[link to sample face](https://s3.us-south.cloud-object-storage.appdomain.cloud/cloud-object-storage-w251-hw3-faces/myface.png)


Submission
Please point us to the repository of your code and provide an http link to the location of your faces in the object storage. Also, explan the naming of the MQTT topics and the QoS that you used.


