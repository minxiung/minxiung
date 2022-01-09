#include <stdlib.h>
#include <stdio.h>

void do_something(FILE *pfile)
{   
     char buf[128];
     fscanf(pfile, "%s", buf);
}

int main(int argc, char **argv)
{
    char dummy[1024];
    FILE *pfile;
    printf("Vulnerable001 starts...\n");
    if(argc>=2) pfile = fopen(argv[1], "r");
    if(pfile) do_something(pfile);
    printf("Vulnerable001 ends....\n");
}
