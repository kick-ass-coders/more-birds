import os
from random import shuffle

def test_train(folder):
    
    # create list of images
    img_list = os.listdir(folder)

    # assign random subset of 80% to put in train folder
    # create copy of img_list
    mixed = img_list[:]
    # randomly sort
    shuffle(mixed)
    # calculate number equal to 80% of images
    train_len = round(len(mixed)*.8)
    # subset randomly sorted list for 80%
    train_sub = mixed[:train_len]
    # create subset of remaining 20%
    test_sub = mixed[train_len:]
    
        # move those to train folder
    for file in train_sub:
        os.rename("E:/bird_project/"+folder+"/"+file, "E:/bird_project/train/"+folder+"/"+file)
        
    # put remaining subset in test folder
    for file in test_sub:
        os.rename("E:/bird_project/"+folder+"/"+file, "E:/bird_project/test/"+folder+"/"+file)