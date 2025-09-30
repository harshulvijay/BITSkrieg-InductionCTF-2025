// gcc -m64 -o functions_assemble functions_assemble.c -no-pie -Wno-implicit-function-declaration

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
        printf("Could not read flag.");
    }

    fclose(fp);
}


void vuln() {
    char buffer[300];
    printf("There is a gathering of functions happening.\n");
    printf("All the functions GOT TABLE addressed to them. So the waiter knows exactly where to serve them.\n");
    printf("Can you call the win function to give a toast to everyone??");

    fgets(buffer, sizeof(buffer), stdin);
    printf(buffer);

    puts("The end.");
    
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    vuln();
    return 0;
}
