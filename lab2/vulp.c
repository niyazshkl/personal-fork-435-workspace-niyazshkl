#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main()
{
    char *fn = "/tmp/XYZ";
    char buffer[60];
    FILE *fp;
    int ruid = getuid();
    int euid = geteuid();

    /* get user input */
    scanf("%50s", buffer);

    // temporarily disable the root privilage using seteuid
    if (seteuid(ruid) == -1)
    {
        printf("some error happened\n");
        return 1;
    }
    if (!access(fn, W_OK))
    {
        // sleep(10); Removing Sleep after completion of Task 2A.

        // Grant back the root privilage using seteuid
        if (seteuid(euid) == -1)
        {
            printf("some error happened\n");
            return 1;
        }
        fp = fopen(fn, "a+");
        fwrite("\n", sizeof(char), 1, fp);
        fwrite(buffer, sizeof(char), strlen(buffer), fp);
        fclose(fp);
    }
    else
    {
        // always correctly restore privileges before exiting
        seteuid(euid);
        printf("No permission \n");
    }
}
