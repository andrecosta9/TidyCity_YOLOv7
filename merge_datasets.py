import os
import os.path
import shutil

main_path = '/mnt/c/Users/ccvcauser2/Desktop/Datasets/'
dataset1_name = 'Cardboard_missingDatasets'
dataset2_name = 'TidyCity_8classes_LabelStudio_OpenImages_Amesterdam'

#Path to the images and labels directories of dataset1
images_directory1 = main_path + dataset1_name + '/train/images/'
labels_directory1 = main_path + dataset1_name + '/train/labels/'

#Path to the images and labels directories of dataset2
images_directory2 = main_path + dataset2_name + '/train/images/'
labels_directory2 = main_path + dataset2_name + '/train/labels/'

#Classes in dataset1 and dataset2

#MELHORAR ISTO. Isto deve ser lido do ficheiro .yaml!
classes_dataset1 = ['Cardboard']
classes_dataset2 = ['Person', 'License plate', 'Plastic bag', 'Waste container', 'Billboard', 'Traffic sign', 'Graffiti', 'Cardboard']
classes_merged_dataset = ['Person', 'License plate', 'Plastic bag', 'Waste container', 'Billboard', 'Traffic sign', 'Graffiti', 'Cardboard']

merged_directory = main_path + 'Merged_' + dataset1_name + '_' + dataset2_name
#Create the merged images and labels directories
merged_images_directory = merged_directory + '/train/images/'
merged_labels_directory = merged_directory + '/train/labels/'


#Function that reads all the files names from images_directory1 and labels_directory1 and changes the filenames to its first characters until "_jpg"
def change_filenames():
    
    #Dataset1
    for filename1 in os.listdir(images_directory1):
        f = filename1.split("_jpg", maxsplit=1)[0]
        f1 = filename1.split("_JPG", maxsplit=1)[0]

        if f != filename1:
            os.rename(os.path.join(images_directory1, filename1), os.path.join(images_directory1, f + ".jpg"))
        #print("Filename already changed")
        elif f1 != filename1:
            os.rename(os.path.join(images_directory1, filename1), os.path.join(images_directory1, f1 + ".jpg"))
            
        
    for filename1 in os.listdir(labels_directory1):
        f = filename1.split("_jpg", maxsplit=1)[0]
        f1 = filename1.split("_JPG", maxsplit=1)[0]

        if f != filename1:
            os.rename(os.path.join(labels_directory1, filename1), os.path.join(labels_directory1, f + ".txt"))
        elif f1 != filename1:
            os.rename(os.path.join(labels_directory1, filename1), os.path.join(labels_directory1, f1 + ".txt"))
    
    print("Finished changing filenames from dataset1")
    
    #Dataset2
    for filename2 in os.listdir(images_directory2):
        f = filename2.split("_jpg", maxsplit=1)[0]
        f1 = filename2.split("_JPG", maxsplit=1)[0]

        if f != filename2:
            os.rename(os.path.join(images_directory2, filename2), os.path.join(images_directory2, f + ".jpg"))
        #print("Filename already changed")
        elif f1 != filename2:
            os.rename(os.path.join(images_directory2, filename2), os.path.join(images_directory2, f1 + ".jpg"))

    
    for filename2 in os.listdir(labels_directory2):
        f = filename2.split("_jpg", maxsplit=1)[0]
        f1 = filename2.split("_JPG", maxsplit=1)[0]

        if f != filename2:
            os.rename(os.path.join(labels_directory2, filename2), os.path.join(labels_directory2, f + ".txt"))
        elif f1 != filename2:
            os.rename(os.path.join(labels_directory2, filename2), os.path.join(labels_directory2, f1 + ".txt"))
    
    print("Finished changing filenames from dataset2")

#Function that creates the merged_images_directory and merged_labels_directory directories and copies all the images from dataset1 and dataset2 to the merged_images_directory
def create_merged_directories():
        
    #Check if the merged_images_directory and merged_labels_directory already exist. If they exist, dont create new ones
    if not os.path.exists(merged_images_directory):
        os.makedirs(merged_images_directory)
    if not os.path.exists(merged_labels_directory):
        os.makedirs(merged_labels_directory)
    
    #Copy all images from dataset1 to merged_images_directory
    for filename in os.listdir(images_directory1):
        
        if filename.endswith(".jpg"):
            #Check if the image already exists in the merged_images_directory
            if os.path.isfile(merged_images_directory + filename):
                continue
            else: 
                shutil.copy(os.path.join(images_directory1, filename), os.path.join(merged_images_directory, filename))
    
    #Copy all images from dataset2 to merged_images_directory without duplicates
    for filename in os.listdir(images_directory2):
        
        if filename.endswith(".jpg"):

            if os.path.isfile(merged_images_directory + filename):
                continue
            else:
                shutil.copy(os.path.join(images_directory2, filename), os.path.join(merged_images_directory, filename))


#Function that saves all images to merged_images_directory. Compares the .txt files names in both labels directories and merge the files that have the same name. 
#Save the merged labels to merged_labels_directory
def merge_datasets():
    
    create_merged_directories()

    print("Finished merging the images!")

    #MELHORAR ISTO..... CASO EXISTA UMA IMAGEM EM COMUM QUE JÁ TENHA CLASSES EM COMUM ENTRE DATASETS, ESCREVER NO FICHEIRO .TXT APENAS OS LABELS QUE FALTAM E AJUSTAR O CLASS_ID DOS QUE JÁ LÁ ESTAVAM

    #Merge the labels from dataset1 and dataset2
    for filename in os.listdir(labels_directory1):

        #print("filename: ", filename)

        if os.path.isfile(labels_directory2 + filename):
            with open(labels_directory1 + filename, 'r') as f1:
                with open(labels_directory2 + filename, 'r') as f2:
                    with open(merged_labels_directory + filename, 'a') as f3:

                        #Check the class id (first character of each line) and change it to the new class id. The new class id is the index of the class in the merged dataset
                        for line in f1:
                                
                            class_id = line.split(' ')[0]
                            class_name = classes_dataset1[int(class_id)]
                            new_class_id = classes_merged_dataset.index(class_name)
                            line = str(new_class_id) + line[1:]
                            
                            """ print("f1: ", class_id)
                            print(class_name)
                            print(line) """

                            f3.write(line)
                        
                        #When using write() the cursor is at the end of the file. So we need to add a new line before writing the next line.
                        f3.write('\n')

                        for line in f2:
                                    
                            class_id = line.split(' ')[0]
                            class_name = classes_dataset2[int(class_id)]
                            new_class_id = classes_merged_dataset.index(class_name)
                            line = str(new_class_id) + line[1:]

                            """ print("f2: ", class_id)
                            print(class_name)
                            print(line) """

                            f3.write(line)
                        
        else:
            #shutil.copy(os.path.join(labels_directory1, filename), os.path.join(merged_labels_directory, filename))

            with open(labels_directory1 + filename, 'r') as f1:
                with open(merged_labels_directory + filename, 'a') as f3:

                    #Check the class id (first character of each line) and change it to the new class id. The new class id is the index of the class in the merged dataset
                    for line in f1:
                            
                        class_id = line.split(' ')[0]
                        class_name = classes_dataset1[int(class_id)]
                        new_class_id = classes_merged_dataset.index(class_name)
                        line = str(new_class_id) + line[1:]

                        """ print("f1 (only dataset1): ", class_id)
                        print(class_name)
                        print(line) """
                        
                        f3.write(line)

        """ if filename == "0003bb040a62c86f.txt":
            break """
        
    
    for filename in os.listdir(labels_directory2):
        #print("filename: ", filename)
        
        if os.path.isfile(merged_labels_directory + filename):
            continue
        else:
            #shutil.copy(os.path.join(labels_directory2, filename), os.path.join(merged_labels_directory, filename))

            with open(labels_directory2 + filename, 'r') as f2:
                with open(merged_labels_directory + filename, 'a') as f3:

                    #Check the class id (first character of each line) and change it to the new class id. The new class id is the index of the class in the merged dataset
                    for line in f2:
                            
                        class_id = line.split(' ')[0]
                        class_name = classes_dataset2[int(class_id)]
                        new_class_id = classes_merged_dataset.index(class_name)
                        line = str(new_class_id) + line[1:]

                        """ print("f2 (only dataset2): ", class_id)
                        print(class_name)
                        print(line) """
                        
                        f3.write(line)
        

    
    #Criar um ficheiro .yaml com a ordem das classes
    """ #Create the dataset.yaml file for the merged dataset
    with open(merged_directory + '/dataset.yaml', 'w') as f:
        f.write('train: ' + merged_directory + '/images """
                

#Main function
if __name__ == "__main__":
    change_filenames()
    print("Filenames changed")
    
    merge_datasets()
    print("Datasets merged!")






    
                            
                            
                            

                        