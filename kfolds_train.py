import os
import random
import yaml
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MultiLabelBinarizer


TRAIN_PATH = '/mnt/c/Users/ccvcauser2/Desktop/Datasets/label_studio/batch1_2_3_corrected'
IMG_SIZE = 640
BATCH_SIZE = 32
WORKERS = 2
EPOCHS = 40
SEED = 42
NUM_FOLD = 5
CFG = 'cfg/training/yolov7-tiny_faceslicenses.yaml'
#WEIGHTS = '../Results/yolov7/yolov7-e6e_TidyCity_7classes_LabelStudio_bagwasteOpenImages/train/exp/weights/best.pt'
WEIGHTS = '../Models/yolov7-tiny.pt'
#PROJECT = '../Results/yolov7/yolov7-e6e_TidyCity_8classes_5_kfolds/train'
PROJECT = '../Results/yolov7/yolov7-tiny_peoplelicenses_kfolds/train'

NUM_CLASSES = 2
#CLASSES_NAMES = ['Person', 'License plate', 'Plastic bag', 'Waste container', 'Billboard', 'Traffic sign', 'Graffiti', 'Cardboard']
CLASSES_NAMES = ['Person', 'License plate']



#Function that runs through every image and corresponding annotation in a dataset in folder TRAIN_PATH, 
#splits it all into N diferent folds and creates a new folder for each fold with the images and annotations for that fold.
def create_folds(TRAIN_PATH, NUM_FOLD, SEED):

    # Create a list of all the image names in the dataset
    #image_names = os.listdir(TRAIN_PATH + '/images')
    image_names = []

    for file in os.listdir(TRAIN_PATH + '/images'):
        if file.endswith(".jpg"):
            image_names.append(file)

    # Create a list of all the image names without the extension
    image_names = [image_name.split('.')[0] for image_name in image_names]

    # Remove duplicates
    image_names = list(set(image_names))

    """ # Shuffle the list
    random.Random(SEED).shuffle(image_names)

    #Calculate the number of images in each fold withou leaving any images out
    images_per_fold = len(image_names) // NUM_FOLD
    #images_per_fold = int(len(image_names)/NUM_FOLD)

    print("Number of images in the dataset: ", len(image_names), "\n")
    print("Number of images per fold: ", images_per_fold, "\n")

    # Create a list of lists with the image names for each fold
    image_names = [image_names[i:i + images_per_fold] for i in range(0, len(image_names), images_per_fold)] """

    #Create a new folder called folds and inside it create a folder for each fold
    
    if os.path.exists(TRAIN_PATH + '/folds'):
        os.system(f'rm -rf {TRAIN_PATH}/folds')
        os.mkdir(TRAIN_PATH + '/folds')
    else: 
        os.mkdir(TRAIN_PATH + '/folds')
    
    #Copy the corresponding images and annotations to each fold folder
    for fold in range(NUM_FOLD):
        
        os.mkdir(f'{TRAIN_PATH}/folds/fold_{fold}')
        """ os.mkdir(f'{TRAIN_PATH}/folds/fold_{fold}/images')
        os.mkdir(f'{TRAIN_PATH}/folds/fold_{fold}/labels')

        for image_name in image_names[fold]:

            os.system(f'cp {TRAIN_PATH}/images/{image_name}.* {TRAIN_PATH}/folds/fold_{fold}/images')
            os.system(f'cp {TRAIN_PATH}/labels/{image_name}.txt {TRAIN_PATH}/folds/fold_{fold}/labels') """
   

    

    #Create a dataframe with each image name and the classes in it
    import pandas as pd

    df = pd.DataFrame(columns=['image_name', 'classes'])

    total_class_count = [0] * NUM_CLASSES

    for image_name in image_names:

        #Open the corresponding .txt file
        with open(TRAIN_PATH + '/labels/' + image_name + '.txt') as f:

            #Read the file and split it into a list of strings
            lines = f.read().splitlines()

            classes = []

            for line in lines:

                #Split each line into a list of strings
                line = line.split(' ')

                #Get the class of the object in the image
                classes.append(int(line[0]))

                total_class_count[int(line[0])] += 1
                #new_row = pd.DataFrame({'image_name': [image_name], 'classes': [classes]})
                

            new_row = {'image_name': image_name, 'classes': classes}
            df.loc[len(df)] = new_row


    #Print the total number of objects in each class
    for id, name in enumerate(CLASSES_NAMES):
        print(f"Class {name}: {total_class_count[id]} objects ({total_class_count[id]/sum(total_class_count)*100:.2f}%)")   

    print('\n')

    #Create csv file for df
    df.to_csv(TRAIN_PATH + '/df.csv', index=False)
    print(".csv file saved!" + '\n')

    skf = StratifiedKFold(n_splits=NUM_FOLD, shuffle=True, random_state=SEED)

    df_converted = df.copy()

    #Tive de fazer isto porque o skf.split() não funciona com multi-labels (este código converte os multi-labels em códigos binários... pelo que percebi)
    df_converted['classes'] = MultiLabelBinarizer().fit_transform(df['classes'])

    train_indexes = []
    test_indexes = []

    #fold_class_count = [[0] * NUM_CLASSES] * NUM_FOLD
    fold_class_count = []
    #fold_class_count_aux = [0]*NUM_CLASSES

    #Print the indexes of the training and validation data for each fold
    for i, (train_index, test_index) in enumerate(skf.split(df_converted['image_name'], df_converted['classes'])):
        #print(f"Fold {i}:")
        #print(f"  Train: index={train_index}, len={len(train_index)}")
        #print(f"  Test:  index={test_index}, len={len(test_index)}" + '\n')

        train_indexes.append(train_index)
        test_indexes.append(test_index)

        fold_class_count_aux = [0]*NUM_CLASSES

        #Save the number of objects in each class for each fold
        for index in test_indexes[i]:
            
            #print(index)
            #aux = df['classes'][index]
            aux = df.loc[index, "classes"]
            #print("IDS:", aux)

            for class_id in aux:
                
                #print("Class_id:", class_id)
                #fold_class_count[i][class_id] += 1
                fold_class_count_aux[class_id] += 1
        
        fold_class_count.append(fold_class_count_aux)
    
    #print("Class_count:", fold_class_count)

    
    #print(df.tail())

    #Print the number of objects in each class for each fold
    for fold in range(NUM_FOLD):

        print(f'FOLD{fold}:' + '\n')
        
        for id, name in enumerate(CLASSES_NAMES):   
            print(f"Class {name}: {fold_class_count[fold][id]} objects ({fold_class_count[fold][id]/sum(fold_class_count[fold])*100:.2f}%)")

        print('\n')

    #Create a new .txt file with the path to the training and validation data for each fold
    for fold in range(NUM_FOLD):
        
        with open(f'{TRAIN_PATH}/folds/fold_{fold}/train_split_fold_{fold}.txt', 'w') as f:

            with open(f'{TRAIN_PATH}/folds/fold_{fold}/valid_split_fold_{fold}.txt', 'w') as f2:

                """ for fold_aux in range(NUM_FOLD):
                    
                    for image_name in image_names[fold_aux]:
                        
                        if fold_aux != fold:

                            path = os.path.join( TRAIN_PATH + '/images/', image_name + '.jpg')
                            f.write(path + '\n')
                        else:
                            path2 = os.path.join( TRAIN_PATH + '/images/', image_name + '.jpg')
                            f2.write(path2 + '\n') """
                
                for image_name_train in df_converted['image_name'][train_indexes[fold]]:

                    path = os.path.join( TRAIN_PATH + '/images/', image_name_train + '.jpg')
                    f.write(path + '\n')

                    #fold_class_count[fold] = [sum(x) for x in zip(fold_class_count[fold], df_converted['classes'][train_indexes[fold]][int(image_name_train)])]

                for image_name_test in df_converted['image_name'][test_indexes[fold]]:

                    path2 = os.path.join( TRAIN_PATH + '/images/', image_name_test + '.jpg')
                    f2.write(path2 + '\n')

        # Create .yaml file 
    
        data_yaml = dict(
            train = f'{TRAIN_PATH}/folds/fold_{fold}/train_split_fold_{fold}.txt',
            val = f'{TRAIN_PATH}/folds/fold_{fold}/valid_split_fold_{fold}.txt',
            nc = NUM_CLASSES,
            names = CLASSES_NAMES
        )

        # Note that I am creating the file in the yolov5/data/ directory.
        with open(f'{TRAIN_PATH}/folds/fold_{fold}/fold_{fold}.yaml', 'w') as outfile:
            yaml.dump(data_yaml, outfile, default_flow_style=True)



################ MAIN ################


#create_folds(TRAIN_PATH, NUM_FOLD, SEED)

#WEIGHTS_TEST = f'{WEIGHTS}/fold_{fold}/exp/weights/best.pt'
CONF_THRES = 0.35
#PROJECT_TEST = '../Results/yolov7/yolov7-e6e_TidyCity_8classes_5_kfolds/test'
PROJECT_TEST = '../Results/yolov7/yolov7-e6e_TidyCity_8classes_5_kfolds_onlyWithPretrainedCOCO/test'

#Run the training script for each fold
for fold in range(NUM_FOLD):    
    print('TRAINING WITH FOLD', fold, ': ', '\n')

    #Don't forget that for yolov7-tiny you need to use the train.py instead of train_aux.py
    os.system(f'python3 train.py --img {IMG_SIZE} \
                    --batch-size {BATCH_SIZE} \
                    --workers {WORKERS} \
                    --epochs {EPOCHS} \
                    --data {TRAIN_PATH}/folds/fold_{fold}/fold_{fold}.yaml \
                    --cfg {CFG} \
                    --weights {WEIGHTS} \
                    --save_period 10\
                    --project {PROJECT}/fold_{fold} ')
    
    """ #To train with the best weights of the previous fold
    os.system(f'python3 train_aux.py --img {IMG_SIZE} \
                    --batch-size {BATCH_SIZE} \
                    --workers {WORKERS} \
                    --epochs {EPOCHS} \
                    --data {TRAIN_PATH}/folds/fold_{fold}/fold_{fold}.yaml \
                    --cfg {CFG} \
                    --weights {PROJECT}/fold_{fold}/exp/weights/best.pt \
                    --save_period 10\
                    --project {PROJECT}/fold_{fold} ') """
    
    print('###########################################################################################\n')

    """ print('TESTING WITH FOLD', fold, ': ', '\n')

    os.system(f'python3 test.py --img {IMG_SIZE} \
                    --data {TRAIN_PATH}/folds/fold_{fold}/fold_{fold}.yaml \
                    --weights {PROJECT}/fold_{fold}/exp/weights/best.pt \
                    --conf-thres {CONF_THRES} \
                    --project {PROJECT_TEST}/fold_{fold} \
                    --batch-size {BATCH_SIZE}') """
    