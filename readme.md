# Repository Info
this is respository of DAIG (Distributed A.I Grid) project client program.
it is based on PyQt5 because we use tensorflow for model training and others.

DAIG (Distributed A.I Grid) 프로젝트의 클라이언트 프로그램 리포지토리 입니다.
이 클라이언트 프로그램은 PyQt5를 기반으로 텐서플로우를 사용하여 모델 훈련을 합니다.   
- - -

# What is DAIG?
DAIG (Distributed A.I Grid) is distributed deep learning based machine learning system.
Usually, deep learning based machine learning methods require more training time than other methods.
One way to solve this long training time problem is using multiple GPUs. However, it is pretty expensive.
So, we tried to use other people's left pc resources instead of multiple GPUs

DAIG는(Distributed A.I Grid) 딥러닝 분산학습 기반 머신러닝 시스템입니다.
보통 딥러닝 기반 머신러닝 기법들은 다른 기법들 보다 더 많은 훈련 시간이 요구됩니다.
이러한 긴 시간이 소비되는 문제를 해결하는 하나의 방법으로 다중 GPU들을 사용하는 방법이 있습니다. 하지만 이 방법은 많은 비용이 요구됩니다.
그래서 저희는 다중 GPU들을 사용하는 대신에 다른 사람들의 잉여 pc 자원을 사용하는 것을 고안했습니다.
- - -
# How DAIG works?
DAIG system consists of Learning requestor, Resource provider and Management server.
Learning requestor makes project and upload train data to Management server.
Then, Management server distribute train data shards and model information to registered Resource providers
When all train data shards are used for learning, Management server save final model and weight result at object storage.
Learning requestor can download trained model at anytime.

DAIG 시스템은 학습요청자, 리소스 제공자 그리고 관리 서버로 구성됩니다.
최초에 학습요청자는 프로젝트를 생성하고 관리 서버로 훈련 데이터를 전송합니다.
이후, 관리 서버는 훈련 데이터의 파편과 모델 정보를 해당 프로젝트에 참여하는 리소스 제공자에게 나눠줍니다.
모든 훈련 데이터 파편에 대한 학습이 끝나면, 과리 서버는 훈련된 최종 모델과 가중치 결과들을 오브젝트 스토리지에 저장합니다.
학습요청자는 훈련된 최종 모델을 언제든지 다운받을 수 있습니다.
## DAIG structure
![image](https://user-images.githubusercontent.com/22979031/120693675-47bba700-c4e4-11eb-94b6-f079a1ae0f46.png)
![image2](https://user-images.githubusercontent.com/22979031/120912837-895b7600-c6cd-11eb-93a9-890f489ed992.PNG)
- - -
# DAIG client dependency
|Name|version|usage|
|------|---|---|
|PyQT5|5.12|for UI and multi-thread develoment|
|tensorflow|2.5.0|for model training|
|numpy|1.19.5|for data manipulation|
|requests|2.25.1|for http communication|
|h5py|3.1.0|for model saving|

- - -
# How to launch?
To laucnh client program, you should install necessary libraries which are 'Tensorflow, Numpy, Requests, h5py, PyQT5'.

Then, you can launch client program by running main.py like 
```
python main.py
```
Currently, we are working on converting this project into single executable file.

클라이언트 프로그램을 실행하기 위해선 파이썬 라이브러리인 'Tensorflow, Numpy, Requests, h5py, PyQT5' 을 수동으로 설치해야 합니다.

이후, ui 폴더에서
main.py like 
```
python main.py
```
로 클라이언트 프로그램을 실행할 수 있습니다.

현재 저희는 이 프로젝트를 단일 실행 파일로 실행할 수 있도록 만드는 작업중에 있습니다. 
- - -
# How DAIG's distribution works?
We constructed DAIG distribution and result gathering system based on K-batch sync SGD.
And it gathers trained gradients based on all-reduce method.
K-batch size can be controlled by Learning requestor.
So, its final result is also contorlled by Learning requestor.

저희는 DAIG을 K-batch sync SGD 기반의 분산 및 결과 수집 시스템으로 구성했습니다.
그리고 훈련된 가중치를 all-reduce 기법으로 처리합니다.
K-batch 사이즈는 학습요청자가 조정할 수 있기 때문에
최종 결과 또한 학습요청자가 조정할 수 있습니다.
- - -
# How to use DAIG?
Make account and then log in.
Then, you can choose between two modes, Learning requestor(left) and Resource provider(right)

계정을 만들고 로그인 합니다.
이후, 학습요청자(좌측)와 리소스제공자(우측) 모드를 선택할 수 있습니다.

## Learning requestor
As learning requestor, you can create distributed learning porject by clicking + button on top menu bar.
Then, you will see project setting UI. first, upload your model file and data files.
Model file should be .h5 format file supported by tensorflow as model.save() and it must also contain compile information
Data files must be uploaded as two files. One is for train data and another is for label of train data.
Also these Data files should be stored as numpy file containing train data as numpy array ('dtype = object' is recommended)
(instruction will be written later).
After attach files, you can set hyper parameters for learning. each item will be directly put into tensorflow model.fit().
If you choose epoch = 20, batch_size =32, then it will perform tensorflow based training as model.fit(epoch = 20, batch_size = 32).
Empty item may cause malfunction, so it is recommended to fill all blanks.
However, 'total task','task size' and 'max contributor' are not for fit() function.

학습 요청자는 상단 메뉴 바에서 '+' 버튼을 통해 분산 학습 프로젝트를 생성할 수 있습니다.
이후, 인터페이스에서 프로젝트 설정화면을 볼 수 있습니다.
최초에 모델, 데이터 파일을 업로드합니다.
모델 파일은 텐서플로우의 model.save()에서 지원되는 .h5 포맷이어야 하며, 이 모델 파일은 컴파일 정보도 포함해야 합니다.
데이터 파일은 두개의 파일로 업로드 되어야합니다. 하나는 훈련데이터, 다른 하나는 훈련데이터의 레이블 데이터입니다.
또한, 이 데이터 파일들은 훈련데이터들을 넘파이 배열로 처리한 넘파이 파일이어야 합니다.
('dtype = object'이 되야 합니다)
(자세한 안내사항은 작성 예정입니다)
파일을 업로드한 이후, 학습에 사용할 하이퍼 파라미터들을 설정할 수 있습니다.
각 파라미터들은 텐서플로우의 model.fit()에 바로 적용됩니다.
예를들어 epoch = 20, batch_size = 32 로 설정시, 텐서플로우의 model.fit(epoch = 20, batch_size = 32)로 학습이 진행됩니다.
하지만 다른 파라미터들인 'total task', 'task size' 그리고 'max_contributer' 는 model.fit() 함수에 적용되는 값이 아닙니다.

### total task
You can choose how many data shards you want to split.
If you choose 100, train data will be splitted into 100 data shards.

task size(총 테스크 수)로 얼마나 데이터 파편들을 나눌지 설정할 수 있습니다.
만약 이 값을 100으로 설정시, 훈련 데이터는 100개의 데이터 파편으로 나뉩니다.

### task size
It means K batch size at K-batch sync SGD.
So, if you choose small K, then final model accuracy may be better. but training speed will be decreased as maximum participants get smaller.
On the other hands, if you choose big K,project will be finished in shorter time. But, its accuracy may be worse.
However, detail depends on situations.

task size(테스크 사이즈)는 K-batch sync SGD에서 K batch size 수를 의미합니다.
따라서 작은 수의 K로 설정하면 최종 모델의 accuracy는 올라가지만, max contributor(최대 기여자)값이 작아질 수 록 학습 속도는 저하됩니다.
반면에, 큰 값의 K로 설정하면 학습 속도는 빨라지지만, accuray 값은 나빠질 수 있습니다.
하지만 accuracy 나 학습 속도는 위뿐만 아니라 모든 상황을 고려해야 합니다.

### max contributor
This means max participants in your project in single batch.
So, max contributor more than task size will be useless.

max contributor(최대 기여자)는 프로젝트의 단일 batch에 최대 학습 참여자를 의미합니다.
따라서 max contributor 값이 task size보다 초과하면 그 초과한 수만큼의 기여자는 의미가 없습니다.

## Learning requestor
As Learning requestor, you need to upload model file (as tensorflow supporting .h5 format), train data and train label.
Then, set parameters and hyper-parameters for distriburted learning.
Finally, click start button, then uploading and creating project proceed.

학습요청자는 모델파일(텐서플로우에서 지원하는 .h5 포맷), 학습 데이터, 학습 레이블을 업로드 합니다.
그리고 분산학습에 적용될 파라미터들과 하이퍼 파라미터들을 설정합니다.
마지막으로 시작 버튼을 누르면 파일 업로딩과 프로젝트 생성이 시작됩니다.

## Resource provider
As Resource provider, you only need to participate button.
DAIG management server will give you train data shard and model information autoatically. (irrelavant with model info and data info)
As DAIG client receive data, it starts distributed learning using tensorflow model.fit()
Also, you can stop it anytime you want by clicking stop button (or shutdown program)

리소스제공자는 참여 버튼을 누르기만 하면 됩니다.
DAIG 관리 서버는 자동으로 리소스제공자에게 학습 데이터 파편과 모델 정보를 줍니다.
(모델 정보 및 데이터 정보와는 상관없이)
DAIG 클라이언트가 데이터를 받으면 텐서플로우의 model.fit()를 통해 분산학습을 시작합니다.
또한 리소스제공자는 언제든지 학습 중단(또는 프로그램 끄기)이 가능합니다.

- - -
# Some points of DAIG client
## One way to treat numpy file via https
## PyQT parallel thread
- - -
### caution!
* This project has been developed by korean developers. So, there are some korean comments.
And server is usually off because of maintainance fee (not a big deal for single project but will be quite a lot for hundreds of projects). 
So, if you want to try by your own, please visit https://github.com/netroid314/ASWCS_back for server codes.
* If you upload incorrect type of model or data, it may cause eniter system malfunction
* DAIG reads train data at once. so, if train data size is too big (like 20GB or more / depends on computer performance), you may not be able to upload total data. upload for big data will be supported later.
* Some parameters have limitation.

* 이 프로젝트는 한국 개발자들이 개발했습니다. 따라서 코드에 한국어 코멘트들이 많이 있습니다.
그리고 서버의 사용요금 때문에 관리 서버는 주로 꺼진상태입니다. (단일 프로젝트를 관리할 때는 문제가 되지않지만, 수백 단위의 프로젝트를 운영할 때 서버의 사용요금이 문제가 될 수 있습니다)
만약 이 프로젝트를 주도적으로 사용해보고 싶다면 https://github.com/netroid314/ASWCS_back 를 방문하여 서버 코드를 확인하세요.

* 맞지 않는 모델과 데이터 타입의 업로드로 인해 시스템 오작동이 생길 수 있습니다.
* DAIG 시스템은 학습 데이터를 한번에 읽습니다. 따라서 만약 훈련 데이터 사이즈가 너무 크면(20GB 보다 큰 값들 / 컴퓨터 성능에 따라 달라질 수 있습니다), 모든 데이터 업로드가 불가능할 수 있습니다. 큰 사이즈의 데이터는 이후 지원예정입니다.
* 몇몇의 파라미터들은 한계값이 설정되어 있습니다.