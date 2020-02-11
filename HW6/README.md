# Homework 6 - Katayoun Borojerdi   

## BERT model - Jigsaw Unintended Bias in Toxicity Classification  
For this homework we will train a BERT NLP model in pytorch on the Jigsaw Toxicity classification dataset.

### Start VMs  
Start an ibmcloud VM with the follwoing commands

#### V100  
```
ibmcloud sl vs create --datacenter=dal10 --hostname=v100a --domain=kborojerdi.cloud --image=2263543 --billing=hourly  --network 1000 --key=1689110 --flavor AC2_8X60X100 --san
```

#### P100  
```
ibmcloud sl vs create --datacenter=dal13 --hostname=p100a --domain=kborojerdi.cloud --image=2263543 --billing=hourly  --network 1000 --key=1689110 --flavor AC1_8X60X100 --san
```

### Start and run the Notebook
Once we have a VM running, ssh into the machine and run the below.
```
nvidia-docker run --rm --name hw06 -p 8888:8888 -d w251/hw06:x86-64
```
Useing the docker logs and the IP address of the VM, we can go to the url of our Notebook.  

After filling the missing code cells with help from the *Toxic BERT plain vanila* Kernal, we run the notebooks on each of the VMs created above.

### Comparing GPU performance of P100 vs V100
Run times for P100  
Bert Tokenizer  34 mins  
Training        365 mins  
Prediction      61 mins  
Total           460 mins  

Run times for V100  
Bert Tokenizer  34 mins  
Training        112 mins  
Prediction      16 mins  
Total           162 mins  

Nvidia advertizes speed increase of "2.05x for V100 compared to the P100 in training mode and 1.72x in inference mode."
From our results we are seeing an increase of 3.26x for training and 3.81x for predictions.

### Section 8C - Submit to Kaggle
I Copied the notebook at https://www.kaggle.com/abhishek/pytorch-bert-inference, uploaded and used the "bert_pytorch.bin" created from the V100 notebook.
Submited the output file with the following result

![Kaggle Score](https://github.com/kborojerdi/w251/blob/master/HW6/Kaggle%20Score%20-%20Kborojerdi.png)
