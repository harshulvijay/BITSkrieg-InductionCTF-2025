#include <stdio.h>
#include <stdlib.h>

int main() {
    char buffer[128];
    char flag[64];

    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        perror("flag.txt not found,please make one yourself for testing.");
        return 1;
    }
    fgets(flag, sizeof(flag), f);
    fclose(f);

    printf("My boss has been pulling my strings lately, would you like to comment on it: ");

    fgets(buffer, sizeof(buffer), stdin);
    printf(buffer);

    printf("\nDone!\n");
    return 0;
}

