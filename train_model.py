import numpy as np
from alexnet import alexnet

WIDTH = 80
HEIGHT = 60
LR = 1e-3
EPOCHS = 8
MODEL_NAME = 'pygta5-car-{}-{}-{}epochs.model'.format(LR,'alextnetv2',EPOCHS)

model = alextnet(WIDTH,HEIGHT,LR)

train_data = np.load('training_data_v2.npy')

train = train_data[:-500]
test  =train_data[-500:]

X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
Y = [i[1] for i in train]


test_X = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
test_Y = [i[1] for i in test]

model.fit({'input':X},{'targets' : Y}, n_epoch = EPOCHS,
          validation_set=({'input':test_X},{'targets':test_Y}),
          snapshot_step=500 , show_metric=True , run_id=MODEL_NAME)

# tensorboard --logdir=foo:C:/Users/Atharva/Desktop/Self Driving Vehicle/log

model.save(MODEL_NAME)
