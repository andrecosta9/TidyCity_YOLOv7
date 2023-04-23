import os

#Command to convert COCO dataset to YOLOv5 format
#os.system('fiftyone convert --input-dir /mnt/c/Users/ccvcauser2/Desktop/coco-2017/train --input-type fiftyone.types.COCODetectionDataset --output-dir /mnt/c/Users/ccvcauser2/Desktop/coco-2017/ --output-type fiftyone.types.YOLOv5Dataset')


#images_directory = '/mnt/c/Users/ccvcauser2/Desktop/coco-2017/train/images/val'
#images_directory = '/mnt/c/Users/ccvcauser2/Desktop/open-images-v7/train/images/'
images_directory = '/mnt/c/Users/ccvcauser2/Desktop/peoplelicenses_dataset_merge4k/images/'
labels_directory = '/mnt/c/Users/ccvcauser2/Desktop/coco-2017/train/labels/val/'

txt_list = os.listdir(labels_directory)
#print(txt_list)
count_person = 0
check_null = 1
count_nulls = 0

""" for txt_file in txt_list:

    with open(labels_directory + txt_file, 'r') as file_r:
        
        labels = file_r.readlines()
        #print(labels)
        with open(labels_directory + txt_file, 'r') as file_w:
        
            for line in labels:
                
                if line[0] == '1' and line[1] == ' ':
                    
                    #Since im only using one class the id must be 0 otherwise train.py gives an error
                    aux_list = list(line)
                    aux_list[0] = '0'
                    new_line = ''.join(aux_list)
                    
                    file_w.writelines(new_line)
                    print(line)
                    print(txt_file)

                    check_null = 0  #file not null
                    count_person += 1

    if check_null == 1:
        os.remove(labels_directory + txt_file)
        count_nulls += 1

    check_null = 1 #reset
     """

from utils.datasets import * 

autosplit(images_directory, [0.7, 0.3, 0.0], annotated_only=True)

print(count_nulls)
print("Finished deleting unnecessary labels!" + '\n' + "Total no. of ""person"" annotations: ", count_person)
        
