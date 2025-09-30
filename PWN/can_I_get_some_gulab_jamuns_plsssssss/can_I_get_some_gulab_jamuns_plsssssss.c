// gcc -m64 -o can_I_get_some_gulab_jamuns_plsssssss can_I_get_some_gulab_jamuns_plsssssss.c -Wno-implicit-function-declaration

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
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
    uint32_t gulab_jamun = 0;
    int ask = 0;

    printf("How many gulab jamun do you want?: ");
    scanf("%d", &ask);
    
    if (ask > 1) {
        printf("You will only get 1 gulab jamun.\n");
        exit(1);
    }


    gulab_jamun = ask;
    if (gulab_jamun > 1){
        win();
    }
    
}

int main() {
    alarm(30);
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    vuln();
    return 0;
}
