#include <stdio.h>
#include <string.h>
#include <stdlib.h>

double aging_init[8][8];
double aging_t[8][8];
double aging_t_1[8][8];

char buff[1500];


char* t="../val_init";
char* init = "../val_t";
char* t_1 = "../val_t-1";

int main ()
{
    FILE *pFile = NULL;

    pFile = fopen(t, "r");

    if(pFile != NULL)
        fgets(buff, 1500, pFile);


    printf("%s\n\n", buff);

    fclose(pFile);


    char *ptr = strtok(buff,",");
    aging_t[0][0] = atof(ptr);

    for(int i = 1 ; i < 64 ; i++)
    {
          ptr = strtok(NULL,",");
        aging_t[i/8][i%8] = atof(ptr);
//        aging_t[i/8][i%8] = 0;
    }

//    printf("%s\n", ptr);
//    char *ptr2 = strtok(NULL,",");
//    printf("%s\n",ptr2);

    printf("[%15s]\n","mode");
    for(int i = 0 ; i < 64 ; i++)
    {
        printf("%15d ", (int)(aging_t[i/8][i%8]));
        if(i%8==7)
            printf("\n");
    }
    return 0;
}