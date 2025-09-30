// gcc -m64 -o hakla_bank hakla_bank.c -Wno-implicit-function-declaration  -Wno-stringop-overflow

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct Customer {
    char name[32];
    bool is_admin;
    char username[32];
    char password[32];
}Customer;

Customer admin;
Customer player;

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
        exit(1);
    } else {
        puts("Could not read flag.");
    }

    fclose(fp);
}

void add_customer() {
    char name[32];
    unsigned long secret_username;
    unsigned long secret_password;

    printf("Enter your name: ");
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = 0;

    secret_username = (unsigned long)admin.username;
    secret_password = (unsigned long)admin.password;

    
    strcpy(player.name, name);
    player.is_admin = false;
    strcpy(player.username, "Aam Aadmi");
    strcpy(player.password, "lordhakla");
    printf("Welcome, ");
    printf(name); 
    printf("\n");

}

void see_admin_details() {
    printf("\nDo you really think I will give you the details???\n");
    printf("All you will get is his name: ");
    printf(admin.name);
    printf("\n");

}

void change_username() {

    printf("Enter a new username: ");
    gets(player.username);

}

void login_as_admin() {
    if((strstr(player.username,admin.username) != NULL) && (strstr(player.password, admin.password) != NULL)) {
        printf("Successfully logged in as an Admin");
        player.is_admin = true;
    }else {
        printf("Your Username and Password doesn't match with that of the admin.Try again!\n");
    }

}

void see_player_details() {
    printf("Your details are as following: \n");
    printf("Name: %s\n",player.name);
    if(player.is_admin){
        printf("is_admin: True\n");
    }else {
        printf("is_admin: False\n");
    }
    printf("username: %s\n",player.username);
    printf("Password: %s\n",player.password);
}

void see_flag(Customer customer) { 
    if(customer.is_admin == false) {
        printf("Flag is only for the admin to see.\n");
    }else{
        win();
    }
}

void menu() {

    char input[64];
    int choice;
    printf("\n--- HaklaBank Menu ---\n");
    printf("1) Add Customer\n2) Change username\n3) See admin details\n4) Login as admin\n5) See my details\n6)Quit\n\n");
    printf("input: ");

    if (fgets(input, sizeof(input), stdin) == NULL) {
        return;
    }

    choice = atoi(input);

    switch (choice) {
        case 1:
            add_customer();
            break;
        case 2:
            change_username();
            break;
        case 3:
            see_admin_details();
            break;
        case 4:
            login_as_admin();
            break;
        case 5:
            see_player_details();
            break;
        case 6:
            printf("Goodbye!\n");
            exit(0);
        case 1337:
            see_flag(player);
            break;
        default:
            printf("Invalid choice, try again.\n");
            break;
    }

}

int instantiate_admin_struct(){
    FILE *fp = fopen("cred.txt", "r");
    if (!fp) {
        printf("cred.txt not found.Pls make one in the current directory with the form as follows:\n<name>,true,<username>,<password>\n");
        exit(0);
    }

    char buffer[128];
    if (!fgets(buffer, sizeof(buffer), fp)) {
        fprintf(stderr, "Failed to read line\n");
        fclose(fp);
        return 1;
    }
    fclose(fp);

    // Remove trailing newline if present
    buffer[strcspn(buffer, "\n")] = '\0';

    // Parse using strtok
    char *token = strtok(buffer, ",");
    int field = 0;

    while (token != NULL) {
        if (field == 0) {
            strncpy(admin.name, token, sizeof(admin.name) - 1);
            admin.name[sizeof(admin.name) - 1] = '\0';
        } else if (field == 1) {
            admin.is_admin = (strcmp(token, "true") == 0);
        } else if (field == 2) {
            strncpy(admin.username, token, sizeof(admin.username) - 1);
            admin.username[sizeof(admin.username) - 1] = '\0';
        } else if (field == 3) {
            strncpy(admin.password, token, sizeof(admin.password) - 1);
            admin.password[sizeof(admin.password) - 1] = '\0';
        }
        field++;
        token = strtok(NULL, ",");
    }

    return 0;
}


int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    instantiate_admin_struct();

    printf("Welcome to the HaklaBank dear customer! :)\n");

    while(1){
        menu();
    }
    return 0;
}
