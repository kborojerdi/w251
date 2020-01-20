# HW3 - Katayoun Borojerdi

In the cloud, you need to provision a lightweight virtual machine (1-2 CPUs and 2-4 G of RAM should suffice) and run an MQTT broker. As discussed above, the faces will need to be sent here as binary messages. Another component will need to be created here to receive these binary files and save them to SoftLayer's Object storage (note that the Swift-compatible object storage is being deprecated in favor of s3-compatible object storage).

## Cloud VSI
Setting up a lightweight VM from my jumpbox useing CSI
```
ibmcloud sl vs create --hostname=faces --domain=storage.cloud --cpu=1 --memory=2048 --datacenter=sjc04 --os=UBUNTU_18_64 --san --disk=100 --key=1689110
```

name      value
ID        95633556
FQDN      faces.storage.cloud
created   2020-01-20T13:55:57Z
guid      fdf0fb88-788a-4f2e-93e4-3086443a71acfollowing
IP Addr   169.62.93.58

Add storage

Run Docker image alpine-mqtt broker
Run Docker image Ubuntu-python message subscriber + save files to folder


