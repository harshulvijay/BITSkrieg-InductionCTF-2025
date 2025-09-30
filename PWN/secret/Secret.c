// gcc -m64 -o secret secret.c -Wno-implicit-function-declaration 

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void win() {
    FILE *fp;
    char flag[128];

    fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        perror("flag.txt not found.\nPlease make flag.txt in your working directory for debugging.");
        exit(1);
    }

    if (fgets(flag, sizeof(flag), fp) != NULL) {
        printf("Congrats! Here’s your flag: %s\n", flag);
    } else {
        puts("Could not read flag.");
    }

    fclose(fp);
}
    


void vuln() {
    char buf[64];
    char secret[64];
    

    puts("Enter your input:");
    gets(buf);

    if (strcmp(secret,"booyeah") == 0) {
        puts("Secret unlocked!");
        win();
    } else {
        puts("Nope, not the secret.");
    }
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    vuln();
    return 0;
}
