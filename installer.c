// to link and compile:
// cl installer.c
// link installer.obj /OUT:installer.exe

#include <stdio.h>
#include <stdlib.h>

int main() {
	printf("Welcome to the CCTV software install wizard, copyright 2024. Press enter to begin.\n\n"); // UX
	getch(); // UX, similar to python's input()


	// Install python on Windows
	#ifdef _WIN32
		printf("Validating Python installation.\n\n");


		system("curl https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe -o python_installer.exe"); // get python installer
		printf("\n\n\033[31mPlease check the \"Add Python to PATH\" box at the bottom, then select \"Install Now\". When that is complete, click \"Disable PATH length limit\", then click Close.\n"); // ux
		system("start python_installer.exe /norestart"); // run py install
		printf("\n\n\033[31mIf you already have Python installed, press \"Cancel\"\nWAIT UNTIL PYTHON INSTALLER IS COMPLETE, \033[0mthen press any key to continue.\n\n\n");
		getch();
		system("del python_installer.exe"); // delete installer
	#endif
	
		printf("\n\nPython installation is complete. Installing additional dependencies...\n\n");
		system("curl -L https://github.com/CH405co/CCTV/raw/main/install2.exe -o install2.exe"); // this needs to be the GitHub link to install2.exe
		printf("Press enter to run install2.exe \n"); //(if this fails, run it manually...) << add that in if necessary...
		getch();
		system("install2.exe");

}
