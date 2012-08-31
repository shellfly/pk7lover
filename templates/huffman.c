#include <stdio.h>
#include <stdlib.h>

typedef char* item;
typedef struct node* link;
typedef link tree;
struct node{
        item level;
        link left;
        link right;
};

link makenode(item level) {
        link n = NULL;

        if ((n=malloc(sizeof(*link))) == NULL) {
                printf("malloc error,perhaps memory is limited..");
                exit(EXIT_FAILURE);
        }

        n->level = level;
        n->left = NULL;
        n->right = NULL;
        return n;
}

tree maketree(link left, link right) {
        tree t = NULL;
        
        if ( (t=malloc(sizeof(*tree))) == NULL) {
              printf("malloc error,perhaps memory is limited..");
              exit(EXIT_FAILURE);  
        }

        t->left = left;
        t->right = right;
        t->level = left->level + right->level;
        return t;
}

int main(int argc, char *argv[]) {
        
        return 0;
}
