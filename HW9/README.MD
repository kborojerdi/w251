# Homework 9 - Katayoun Borojerdi

## Distributed Training and Neural Machine Translation

In this HW, we'll are training a Transformer-based Machine Translation network on an English to German WMT corpus. We will use Nvidia OpenSeq2Seq framework good for Automatic Speech Recognition (ASR) and Natural Language Processing (NLP). It is  written in Python and TensorFlow. These tasks can take a very long time to train, so we will train on more than one machine. 

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

### Added Docker Containers and Pulled Training Data

Followed the steps outlined in the HW description to the Docker Nvidia Containers running on both VMs.

### Running the mpi command

Ran the following command on the v100a machine to start training.
```
nohup mpirun --allow-run-as-root -n 4 -H 150.238.57.24:2,150.238.57.28:2 -bind-to none -map-by slot --mca btl_tcp_if_include eth0 -x NCCL_SOCKET_IFNAME=eth0 -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH python run.py --config_file=/data/transformer-base.py --use_horovod=True --mode=train_eval &
```

### Submission
The nohup.out file from the training is in the github repo.

screenshots of your Tensorboard 

* BLUE Score
![BLUE_SCORE](https://github.com/kborojerdi/w251/blob/master/HW9/BLUE_Score.png)

* Eval Loss
![Eval_Loss](https://github.com/kborojerdi/w251/blob/master/HW9/eval_loss.png)

* Training Loss
![train_loss](https://github.com/kborojerdi/w251/blob/master/HW9/train_loss.png)

#### 1. How long does it take to complete the training run?  
   It took about 24 hours to complete 50,000 steps.

#### 2. Do you think your model is fully trained? How can you tell?  
   At 50,000 steps I do not think the model is fully trained. However at 300,000 steps, I think the model looks like it is proabably fully trained.
   
#### 3. Were you overfitting?  
   At 50,000 steps I do think the model is overfitting, however at 300,000 steps looking at the sample eval loss it is possible the model is overfitting.

#### 4. Were your GPUs fully utilized?  
   Yes, the GPUs on both machines seemed to be near 100%, at least while I monitored them.

* Usage v100a
![v100a](https://github.com/kborojerdi/w251/blob/master/HW9/Distributed%20Learning%20v100a.png)

* Usage v100b
![v100b](https://github.com/kborojerdi/w251/blob/master/HW9/Distributed%20Learning%20v100b.png)

#### 5. Did you monitor network traffic (hint: apt install nmon ) ? Was network the bottleneck?
It seems that the network must be somewhat the bottelneck since it is fastener to run this on a single machine with 2 GPUs

* Network traffic from nmon  
![Network](https://github.com/kborojerdi/w251/blob/master/HW9/Distributed%20Learning%20Network.png)

#### 6. Take a look at the plot of the learning rate and then check the config file. Can you explan this setting?  
The model is using the learning rate policy, transformer policy, which uses an equation to decay the learning rate as steps increase. For later steps, we use smaller learning rate which resuls in better model more quickly.

#### 7. How big was your training set (mb)? How many training lines did it contain?  

* Training set size (mb)  
![Training_Size](https://github.com/kborojerdi/w251/blob/master/HW9/Training_Size.png)

* Number of lines in the training set  
![Training_Lines](https://github.com/kborojerdi/w251/blob/master/HW9/Training_Lines.png)

#### 8. What are the files that a TF checkpoint is comprised of?  
The TF checkpoint contains three file types that store the data about the model and model weights, along with a couple other files.
* The checkpoint file is a bookkeeping file that can be used for loading different time saved chkp files.
* The .meta file holds the graph of the model and all the metadata associated like learning rate, etc.
* The .index file holds the key-value table linking the tensor names and the data in the chkp.data files.
* The .data files hold the weights. There can be many data files because they can be created at multiple timesteps while training.
* The events file stores information needed to visualise the model along with all the data measured while training. This does not affec saving or restoring the model itself.

#### 9. How big is your resulting model checkpoint (mb)?  
   The data file is 813mb and the meta file is 15mb

#### 10. Remember the definition of a "step". How long did an average step take?  

* Model Finished  
![Finished_Training](https://github.com/kborojerdi/w251/blob/master/HW9/Finished_Training.png)

#### 11. How does that correlate with the observed network utilization between nodes?  
    Faster Network will result in shorter average step time
