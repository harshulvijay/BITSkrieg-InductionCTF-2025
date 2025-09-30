// gcc -m64 -o rakshabandhan_gift rakshabandhan_gift.c -no-pie -Wno-implicit-function-declaration

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sister() {
    FILE *fp;
    char flag[128];

    fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        perror("flag.txt not found.\nPlease make flag.txt in your working directory for debugging.");
        exit(1);
    }

    if (fgets(flag, sizeof(flag), fp) != NULL) {
        printf("Here, a gift for you too: %s\n", flag);
    } else {
        puts("Could not read flag.");
    }

    fclose(fp);
}
    


void vuln() {
    unsigned long addr;

    puts("I forgot to send my sister a gift for this rakshabandhan. More importantly I don't even know where she lives :).");
    puts("Can you help me find her address??");

    if (scanf("%lx", &addr) != 1) {
        puts("Invalid input.");
        exit(1);
    }

    if (addr == (unsigned long)sister) {
        puts("Thank you for your help.");
        sister(); 
    } else {
        puts("Wrong address, the package is destroyed now :(");
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
