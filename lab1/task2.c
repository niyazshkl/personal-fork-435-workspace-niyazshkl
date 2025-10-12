#include "./tiny-AES-c/aes.h"
#include "lab1.h"
#include <stdint.h>

uint8_t hexval(char c)
{
    if (c >= '0' && c <= '9')
        return c - '0';
    if (c >= 'a' && c <= 'f')
        return c - 'a' + 10;
    if (c >= 'A' && c <= 'F')
        return c - 'A' + 10;
    return 0;
}

void hexstr_to_bytes(const char *hex, uint8_t *out)
{
    for (int i = 0; i < 16; i++)
    {
        out[i] = (hexval(hex[2 * i]) << 4) | hexval(hex[2 * i + 1]);
    }
}

/* ------------------------------------------------------------------------------
 *
 *  TASK 2
 *
 *  YOU NEED TO COMPLETE THIS FUNCTION.
 *
 *  This function finds and returns the key used by Alice to encrypt her tax
 *  documents.
 *
 *  Note:
 *      Within this function, you can use the generatekey(...)
 *      function from task 1. Remember, this function allocates space
 *      for the key that it generates on the stack. For every key you
 *      generate (except for the one this function returns) you will
 *      need to call the free() function.
 *
 *  Arguments:
 *      argc: the number of command line arguments.
 *      argv: an array of strings passed in from the command line
 *
 *  Return:
 *      A pointer to a character array on the heap.
 *
 */
unsigned char *findkey(int argc, char **argv)
{

    // TODO 1. Initialize and read in arguments.
    char *pt_hex = argv[1];
    char *ct_hex = argv[2];
    char *iv_hex = argv[3];

    uint8_t plaintext_bytes[KEYSIZE];
    uint8_t ciphertext_bytes[KEYSIZE];
    uint8_t iv_bytes[KEYSIZE];

    hexstr_to_bytes(pt_hex, plaintext_bytes);
    hexstr_to_bytes(ct_hex, ciphertext_bytes);
    hexstr_to_bytes(iv_hex, iv_bytes);

    struct AES_ctx ctx;

    int start = 1524013729; // Found by running date -d "2018-04-17 21:08:49" +%s
    int end = 1524020929;   // Found by running date -d "2018-04-17 23:08:49" +%s

    // I used the below linked online AES calculator along the way when I was debugging if I had the AES_128 CBC encrypt setup correctly:
    // https://paymentcardtools.com/basic-calculators/aes-calculator

    // TODO 2. Generate keys.
    for (int curr = start; curr <= end; curr++)
    {
        unsigned char *key = generatekey((long long)curr);
        // This API call initializes the context with the specific key and IV being used.
        AES_init_ctx_iv(&ctx, key, iv_bytes);

        uint8_t testbuf_bytes[KEYSIZE];
        memcpy(testbuf_bytes, plaintext_bytes, KEYSIZE);

        /* This API call encrypts the input buffer named 'testbuf_bytes'.
         * The resulting ciphertext will be written into the input buffer
         * and the previous testbuf_bytes will be overwritten. */
        AES_CBC_encrypt_buffer(&ctx, testbuf_bytes, KEYSIZE);
        // TODO 3. Verify match.
        if (memcmp(testbuf_bytes, ciphertext_bytes, KEYSIZE) == 0)
        {
            // TODO 4. Return Alice's key
            return key;
        }
        free(key);
    }
    return NULL;
}