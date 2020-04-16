#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <string.h>

#include <sys/time.h>

#define REST 4000000
char* endCommand = "am force-stop com.not.aa_image_viewer";

int main(int argc, char *argv[] )
{
    int i = 0, j = 0;
    int M = 0;
    struct timespec start, end;
    double diff;

    char myCommand[200];
    char category[5];

    int M_lim = atoi(argv[1]);
    int N = 0;
    printf("Daemon Start! \n");
    printf("Turn off Wifi!!\n");

    usleep(8500000);
    for(M=0;M<M_lim;M++)
    {
        for(N=1;N<9;N++)
        {
            for(j = 0 ; j<4 ; j++)
            {
                if(j==0)
                    sprintf(category, "a");
                else if(j==1)
                    sprintf(category, "ab");
                else if(j==2)
                    sprintf(category, "ac");
                else if(j==3)
                    sprintf(category, "abcd");

                for(i = 0 ; i < 9 ; i++)
                {
                    clock_gettime(CLOCK_MONOTONIC, &start);

                    sprintf(myCommand, "am start -a android.intent.action.VIEW -d file:////storage/emulated/0/Pictures/%d/%s/image_%s_%d.bmp -t image/* -n com.not.aa_image_viewer/com.not.aa.ImageDetailActivity",N,category,category,i);
                    system(myCommand);
                    usleep(4530000);
                    clock_gettime(CLOCK_MONOTONIC, &end);

                    diff = (end.tv_sec - start.tv_sec) + 1e-9 * (end.tv_nsec - start.tv_nsec);
                    printf("[%lf]\n", diff); 
                }
            }
        }
    }
    system(endCommand);
    system("input keyevent 26");
    return 0;
}
