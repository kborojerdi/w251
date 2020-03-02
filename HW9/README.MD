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
  
  
nohup mpirun --allow-run-as-root -n 4 -H 150.238.57.24:2, 150.238.57.28:2 -bind-to none -map-by slot --mca btl_tcp_if_include eth0 -x NCCL_SOCKET_IFNAME=eth0 -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH python run.py --config_file=/data/transformer-base.py --use_horovod=True --mode=train_eval &


