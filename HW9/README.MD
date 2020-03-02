# Homework 6 - Katayoun Borojerdi

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

