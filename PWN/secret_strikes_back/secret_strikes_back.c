// gcc -m64 -no-pie -fno-stack-protector -o secret_strikes_back secret_strikes_back.c -Wno-implicit-function-declaration

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
    
    puts("Enter your input:");
    gets(buf);

    printf("Here you don't have 'secret' variable to overflow and get the flag. :)\n");

}

int main() {
    alarm(120); 
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    vuln();
    return 0;
}
