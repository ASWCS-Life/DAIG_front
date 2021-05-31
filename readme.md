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

