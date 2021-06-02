# Rpository Info
this is respository of DAIG (Distributed A.I Grid) project client program.
it is based on PyQT5 because we use tensorflow for model training and others.

# What is DAIG?
DAIG (Distributed A.I Grid) is distributed deep learning based machine learning system.
Usually, deep learning based machine learning methods require more training time than other methods.
One way to solve this long training time problem is using multiple GPUs. However, it is pretty expensive.
So, we tried to use other people's left pc resources instead of multiple GPUs

# How DAIG works?
DAIG system consists of Learning requestor, Resource provider and Management server.
Learning requestor makes project and upload train data to Management server.
Then, Management server distribute train data shards and model information to registered Resource providers
When all train data shards are used for leatning, Management server save final model and weight result at object storage.
Learning requestor can download trained model at anytime.

# How DAIG's distribution works?
We constructed DAIG distribution and result gathering system based on K-batch sync SGD.
And it gathers trained gradients based on all-reduce method.
K-batch size can be controlled by Learning requestor.
So, its final result is also contorlled by Learning requestor.

# How to use DAIG?
Make account and then log in.
Then, you can choose between two modes, Learning requestor(left) and Resource provider(right)

## Learning requestor
As learning requestor, you can create distributed learning porject by clicking + button on top menu bar.
Then, you will see project setting UI. first, upload your model file and data files.
Model file should be .h5 format file supported by tensorflow as model.save() and it must also contain compile information
Data files must be uploaded as two files. One is for train data and another is for label of train data.
Also these Data files should be stored as numpy file containing train data as numpy array ('dtype = object' is recommended)
(instruction will be written later).
After attach files, you can set hyper parameters for learning. each item will be directly put into tensorflow model.fit().
If you choose epoch = 20, batch_size =32, then it will perform tensorflow based trainging as model.fit(epoch = 20, batch_size = 32).
Empty item may cause malfunction, so it is recommended to fill all blanks.
However, 'total task','task size' and 'max contributor' are not for fit() function.

### total task
You can choose how many data shards you want to split.
If you choose 100, train data will be splitted into 100 data shards.

### task size
It means K batch size at K-batch sync SGD.
So, if you choose small K, then final model accuracy may be better. but training speed will be decreased as maximum participants get smaller.

## Learning requestor
As Learning requestor, you need to upload model file (as tensorflow supporting .h5 format), train data and train label.
Then, set parameters and hyper-parameters for distriburted learning.
Finally, click start button, then uploading and creating project proceed.

## Resource provider
As Resource provider, you only need to participate button.
DAIG management server will give you train data shard and model information autoatically. (irrelavant with model info and data info)
As DAIG client receive data, it starts distributed learning using tensorflow model.fit()
Also, you can stop it anytime you want by clicking stop button (or shutdown program)

# Some points of DAIG client
## One way to treat numpy file via https
## PyQT parallel thread

