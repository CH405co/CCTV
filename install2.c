/* This file is to install everything after python is successfully installed.
* The python installer adds Python to the PATH after the executable is installed.
* This means that pip will not work unless the program is restarted, or in this case, a second exe is ran.
* here is the second exe that will install packages. */

#include <stdio.h>
#include <stdlib.h>


int main() {
	// Begin CCTV install now that PIP is in the system PATH
	printf("\n\nPython has been installed, now the CCTV software will begin installation. Press any key to continue.\n\n");
	getch();

	// install required packages
	system("pip install opencv_python"); // UX
	printf("Required Python tools installed.\n\nInstalling software now...\n\n"); // UX

	// install software from github
	system("curl -L https://raw.githubusercontent.com/CH405co/CCTV/main/init.py -o init.py");
	printf("CCTV Software successfully installed.\n\n");

	// install the runner exe
	printf("Now installing launcher...");
	system("curl -L https://github.com/CH405co/CCTV/raw/main/launcher.exe -o CCTVViewer.exe");

	//maybe this works
	printf("The installation is complete, do you want to run the CCTV software now? (Y/n)\n> ");
	char input = _getch();

	if (input == 'y') {
		printf("%c", input);
		getch();
		system("CCTVViewer.exe");
	}
	else if (input == 'n') {
		printf("\nthank you for installing, have a great day...\npress enter else if");
		getch();
		exit(0);
	}
	else {
		printf("Sorry I didn't understand that. Here is a crash, (temporarily) (exit code 2, odd input)\n press enter else");
		getch();
		return(2);
	}
}