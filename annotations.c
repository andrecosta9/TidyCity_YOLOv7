#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//#define MAX_CLASSES 26
#define MAX_CLASSES 2
#define MAX_CLASS_NAME_LENGTH 50

/* char* target_classes[MAX_CLASSES] = {"Plastic bag", "Waste container", "Billboard", "Traffic sign", "Stop sign",
                        "Sofa bed", "Couch", "Studio couch", "Bed", "Infant bed", "Television",
                        "Refrigerator", "Washing machine", "Home appliance", "Kitchen appliance", 
                        "Shelf", "Cabinetry", "Bathroom cabinet", "Filing cabinet", "Chest of drawers",
                        "Drawer", "Nightstand", "Table", "Coffee table", "Kitchen & dining room table", "Cupboard"};
 */
char* target_classes[MAX_CLASSES] ={"Person", "Vehicle registration plate"};

int target_classes_id[MAX_CLASSES];
int annotations_count[MAX_CLASSES] = {0};

char* images_directory = "/mnt/c/Users/ccvcauser2/Desktop/open-images-v7/train/data";
char* labels_directory = "/mnt/c/Users/ccvcauser2/Desktop/open-images-v7/train/labels/";
char* classes_file = "/mnt/c/Users/ccvcauser2/Desktop/open-images-v7/train/metadata/classes.csv";
char* predictions_file = "/mnt/c/Users/ccvcauser2/Desktop/open-images-v7/train/labels/detections.csv";


void SaveBoundingBoxToFile(char* image_id, int label, float x_min, float x_max, float y_min, float y_max) {
    char file_path[200];
    sprintf(file_path, "%s%s.txt", labels_directory, image_id);

    FILE* f;
    if ((f = fopen(file_path, "a")) != NULL) {
        fprintf(f, "%d %f %f %f %f\n", label, (x_max + x_min) / 2, (y_max + y_min) / 2, x_max - x_min, y_max - y_min);
        fclose(f);
    }
    else if ((f = fopen(file_path, "w")) != NULL) {
        fprintf(f, "%d %f %f %f %f\n", label, (x_max + x_min) / 2, (y_max + y_min) / 2, x_max - x_min, y_max - y_min);
        fclose(f);
    }
    else {
        printf("Failed to open file %s\n", file_path);
    }
}

void ReadClassesFile() {
    FILE* f;
    if ((f = fopen(classes_file, "r")) != NULL) {
        char line[200];
        char* ptr;
        while (fgets(line, sizeof(line), f) != NULL) {
            ptr = strtok(line, ",");
            int id = atoi(ptr);
            ptr = strtok(NULL, ",");
            ptr[strcspn(ptr, "\r\n")] = 0;
            for (int i = 0; i < MAX_CLASSES; i++) {
                if (strcmp(ptr, target_classes[i]) == 0) {
                    target_classes_id[i] = id;
                    break;
                }
            }
        }
        fclose(f);
    }
    else {
        printf("Failed to open file %s\n", classes_file);
    }
}

void ReadPredictionsFile() {
    FILE* f;
    if ((f = fopen(predictions_file, "r")) != NULL) {
        char line[200];
        char* ptr;
        int row_count = 0;
        while (fgets(line, sizeof(line), f) != NULL) {
            if (row_count != 0) {
                
                ptr = strtok(line, ",");
                char image_name[100];
                strcpy(image_name, ptr);

                ptr = strtok(NULL, ",");
                int class_id = atoi(ptr);

                ptr = strtok(NULL, ",");
                float confidence = atof(ptr);

                ptr = strtok(NULL, ",");
                float x_min = atof(ptr);

                ptr = strtok(NULL, ",");
                float x_max = atof(ptr);

                ptr = strtok(NULL, ",");
                float y_min = atof(ptr);

                ptr = strtok(NULL, ",");
                float y_max = atof(ptr);

                for (int i = 0; i < MAX_CLASSES; i++) {
                    if (class_id == target_classes_id[i]) {
                        SaveBoundingBoxToFile(image_name, i, x_min, x_max, y_min, y_max);
                        annotations_count[i]++;
                        break;
                    }
                }           
                
            }
        }
    }
}

int main() {
    ReadClassesFile();
    printf("Classes: %s %s", target_classes[0], target_classes[1]);
    printf("Ids: %d %d", target_classes_id[0], target_classes_id[1]);

    ReadPredictionsFile();

    for (int i = 0; i < MAX_CLASSES; i++) {
        printf("Class: %s, Count: %d\n", target_classes[i], annotations_count[i]);
    }

    return 0;
}