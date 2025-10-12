#include "lab1.h"

int main(int argc, char **argv)
{
    (void)argc;
    (void)argv;
    unsigned char *key;

    /*
     * TASK 1
     */
    // long long currtime = (long long) time(NULL);
    // key = generatekey(currtime);
    // phex(key, KEYSIZE);
    // free(key);

    /*
     * TASK 2
     *
     * You can uncomment the line below to test your solution to task 2.
     */
    // if (key != NULL)
    // {
    //     phex(key, KEYSIZE);
    //     free(key);
    // }

    key = findkey(argc, argv);
    phex(key, KEYSIZE);
    free(key);

    /*
     * TASK 3
     *
     * You can uncomment the line below to test your solution to task 3.
     */
    // key = readrandom();
    // phex(key, 32);
    // free(key);

    return EXIT_SUCCESS;
}
