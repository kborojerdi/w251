# Homework 9 - Katayoun Borojerdi

## Distributed Training and Neural Machine Translation

Distributed Training and Neural Machine Translation.

### Start VMs

Start an ibmcloud VM with the follwoing commands

Setup a pair of two V-100 VMs in Softlayer.

Commands:

v100a
```
ibmcloud sl vs create --datacenter=dal10 --hostname=v100a --domain=kborojerdi.cloud --image=2263543 --billing=hourly  --network 1000 --key=1689110 --flavor AC2_16X120X100 --san
```
v100b
```
ibmcloud sl vs create --datacenter=dal10 --hostname=v100b --domain=kborojerdi.cloud --image=2263543 --billing=hourly  --network 1000 --key=1689110 --flavor AC2_16X120X100 --san
```

log into the Softlayer Portal, find your instances under "devices" and "upgrade" them by adding a second 2 TB SAN drive to each VM, then format the 2TB disk and mount it to /data

### Prepare the second disk

### What is it called?

fdisk -l
You should see your large disk, something like this

Disk /dev/xvdc: 2 TiB, 2147483648000 bytes, 4194304000 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
In this case, our disk is called /dev/xvdc. Your disk may be named differently. Format it:

# first
mkdir -m 777 /data
mkfs.ext4 /dev/xvdc
Add to /etc/fstab

# edit /etc/fstab and all this line:
/dev/xvdc /data                   ext4    defaults,noatime        0 0
Mount the disk

mount /data
Move the working Docker directory

By default, docker stores its images under /var/lib/docker , which will quickly fill up. So,

service docker stop
cd /var/lib
cp -r docker /data
rm -fr docker
ln -s /data/docker ./docker
service docker start


Nvidia API key
MmI0b2NzYmNpNDAxNnRyMzc4amdwa2dudmE6NjM5OGE4OGYtN2FlNS00NjdhLWJjMDUtNDQ5NzI0ZjU2YTM2



mpirun -n 2 -H 150.238.57.24, 150.238.57.28 --allow-run-as-root hostname
  
  
nohup mpirun --allow-run-as-root -n 4 -H 150.238.57.24:2,150.238.57.28:2 -bind-to none -map-by slot --mca btl_tcp_if_include eth0 -x NCCL_SOCKET_IFNAME=eth0 -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH python run.py --config_file=/data/transformer-base.py --use_horovod=True --mode=train_eval &

Started ~1:00 am


time per step = 0:00:1.723


### Submission
Please submit the nohup.out file along with screenshots of your Tensorboard indicating training progress (Blue score, eval loss) over time. Also, answer the following (simple) questions:

1. How long does it take to complete the training run? (hint: this session is on distributed training, so it will take a while)
It took about 24 hours to complete 50,000 steps.

2. Do you think your model is fully trained? How can you tell?

3. Were you overfitting?

4. Were your GPUs fully utilized?
Yes, the GPUs on both machines seemed to be near 100%, at least while I monitored them.

Usage v100a
![v100a](https://github.com/kborojerdi/w251/blob/master/HW9/Distributed%20Learning%20v100a.png)

Usage v100b
![v100b](https://github.com/kborojerdi/w251/blob/master/HW9/Distributed%20Learning%20v100b.png)



5. Did you monitor network traffic (hint: apt install nmon ) ? Was network the bottleneck?
It seems that the network must be somewhat the bottelneck since it is fastener to run this on a single machine with 2 GPUs

Network traffic from nmon
![Network](https://github.com/kborojerdi/w251/blob/master/HW9/Distributed%20Learning%20Network.png)

6. Take a look at the plot of the learning rate and then check the config file. Can you explan this setting?
The model is using the learning rate policy, transformer policy, which uses an equation to decay the learning rate as steps increase. For later steps, we use smaller learning rate which resuls in better model more quickly.

7. How big was your training set (mb)? How many training lines did it contain?
```
du -sm wmt16_de_en/
13351mb
```



8. What are the files that a TF checkpoint is comprised of?
The TF checkpoint contains three file types that store the data about the model and model weights, along with a couple other files.
* The checkpoint file is a bookkeeping file that can be used for loading different time saved chkp files.
* The .meta file holds the graph of the model and all the metadata associated like learning rate, etc.
* The .index file holds the key-value table linking the tensor names and the data in the chkp.data files.
* The .data files hold the weights. There can be many data files because they can be created at multiple timesteps while training.
* The events file stores information needed to visualise the model along with all the data measured while training. This does not affec saving or restoring the model itself.

9. How big is your resulting model checkpoint (mb)?
The data file is 813mb and the meta file is 15mb

10. Remember the definition of a "step". How long did an average step take?
Average time per step was 1.713 seconds
Average objects per second 36437.740

11. How does that correlate with the observed network utilization between nodes?
