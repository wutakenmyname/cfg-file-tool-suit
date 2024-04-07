#include "cfg_type.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <string.h>
#include <openssl/sha.h>
#include <fcntl.h>

#define mprintf(fmt, ...) printf("[%s,%d] " fmt, __func__, __LINE__, ##__VA_ARGS__)

typedef int (*object_parser_t)(unsigned char *data, int64 data_len);
typedef struct
{
    int64 object_id;
    object_parser_t parser;
}object_handler_t;

static int handle_name(unsigned char *data, int64 data_len)
{
    char name[128] = {0};
    snprintf(name, 128, "%s", data);
    printf("name: %s\n", name);
    return 0;
}

static int handle_height(unsigned char *data, int64 data_len)
{
    double height = -1;
    height = *(double *)(data);
    printf("height: %10lf\n", height);
    return 0;
}

static int handle_weight(unsigned char *data, int64 data_len)
{
    double weight = -1;
    weight = *(double *)(data);
    printf("weight: %10lf\n", weight);
    return 0;
}

static int handle_misc(unsigned char *data, int64 data_len)
{
    mprintf("goes here\n");
    return 0;
}

static int handle_boo(unsigned char *data, int64 data_len)
{
    int64 boo = -1;
    boo = *(int64 *)(data);
    printf("boo: %lld\n", boo);
    return 0;
}

static int handle_snmpmib(unsigned char *data, int64 data_len)
{
    
    return 0;
}

static int handle_id(unsigned char *data, int64 data_len)
{
    unsigned char buff[128] = {0};
    if (data_len < 128)
    {
        memcpy(buff, data, data_len);
        printf("id: ");
        int i = 0;
        for (; i < data_len; i++)
        {
            printf("%02x", buff + i);
        }
        printf("\n");
    }
    return 0;
}

static int handle_default(unsigned char *data, int64 data_len)
{
    mprintf("goes here\n");
    return 0;
}

void sha256_hash_string(const char *string, int64 string_len, unsigned char *hash) {
    printf("goes here\n");
    SHA256_CTX ctx;
    SHA256_Init(&ctx);
    SHA256_Update(&ctx, string, string_len);
    SHA256_Final(hash, &ctx);
}

static object_handler_t handlers[] = 
{
    {ID_1, handle_default},
    {ID_2, handle_default},
    {NAME, handle_name},
    {HEIGHT, handle_height},
    {WEIGHT, handle_weight},
    {MISC, handle_misc},
    {BOO, handle_boo},
    {SNMPMIB, handle_snmpmib},
    {ID, handle_id},
};
char is_little_endian()
{
    unsigned short t = 1;
    if (*((unsigned char *)(&t)) != 0)
    {
        printf("little endian\n");
        return 1;
    }

    printf("big endian\n");
    return 0;
}
int main(int argc, char **argv)
{
    int opt;
    char *file_name = NULL;
    int file_fd = -1;
    struct stat stat;
    unsigned char *file_content = NULL;
    unsigned char hash[SHA256_DIGEST_LENGTH];


    // 解析命令行参数
    while ((opt = getopt(argc, argv, "f:")) != -1) {
        switch (opt) {
            case 'f':
                file_name = optarg;
                break;
            default:
                fprintf(stderr, "Usage: %s -f <file_name>\n", argv[0]);
                exit(EXIT_FAILURE);
        }
    }

    // 检查文件名是否提供
    if (file_name == NULL) {
        fprintf(stderr, "Please provide a file name.\n");
        exit(EXIT_FAILURE);
    }

    if(access(file_name, F_OK) != 0)
    {
        mprintf("file not exist: %s\n", file_name);
        exit(EXIT_FAILURE);
    }

    file_fd = open(file_name, O_RDONLY);
    if (file_fd < 0)
    {
        mprintf("open file failed\n");
        exit(EXIT_FAILURE);
    }
    else
    {
        if (fstat(file_fd, &stat) < 0)
        {
            mprintf("stat file failed\n");
            exit(EXIT_FAILURE);
        }

        if (stat.st_size == 0)
        {
            mprintf("empty file\n");
            close(file_fd);
            exit(EXIT_FAILURE);
        }

        file_content = (unsigned char *)malloc(stat.st_size + 1);
        memset(file_content, 0, stat.st_size + 1);
        if (file_content == NULL)
        {
            close(file_fd);
            exit(EXIT_FAILURE);
        }

        if (read(file_fd, file_content, stat.st_size) != stat.st_size)
        {
            mprintf("read header failed\n");
            close(file_fd);
            exit(EXIT_FAILURE);
        }

        int64 i = 0;
        mprintf("file content: ");
        for (; i < stat.st_size; i++)
        {
            printf("%02x", file_content[i]);
        }
        printf("\n");
        mprintf("goes here\n");
        mprintf("file_content len: %lld, %02x \n", stat.st_size, file_content[32]);
        sha256_hash_string((unsigned char *)file_content + 32, stat.st_size - 32, hash);
        printf("hash computed: ");
        for (int64 i = 0; i < SHA256_DIGEST_LENGTH; i++) 
        {
            if (file_content[i] != hash[i])
            {
                mprintf("file is broker\n");
                close(file_fd);
                exit(EXIT_FAILURE);
            }
        }
        printf("\n");

        char little_endian = 0;
        little_endian = is_little_endian();
        mprintf("file is good\n");
        for (i = 32; i < stat.st_size;)
        {
            if (little_endian)
            {
                int64 obj_id = -1;
                int64 length = -1;
                memcpy(&obj_id, (unsigned char *)file_content + i, sizeof(obj_id));
                memcpy(&length, (unsigned char *)file_content + i + 8, sizeof(obj_id));
                
                printf("obj_id: %lld, length: %lld\n", obj_id, length);
                handlers[obj_id - 1].parser((unsigned char *)file_content + i + 8 + 8, length);
                i = i + 8 + 8 + length;

            }
            
        }
    }
    return 0;
}