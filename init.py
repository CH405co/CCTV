"""

IN THIS VERSION, minor bug fixes, im gonna start with the cam double checker, then move onto the flag.


ADD LATER:
** Critical crashes **
double check to see if cam is alr open, don't allow if not. Create a simple list here in it, openCams = [], if index in openCams > print("nah") > commandMode() or openCams()

** Non crit **
function to clear cache of streaming cams. This should have the ability to end all streams.
if no cams are found, the printout is just blank. Maybe add something that says "no cameras were found"
preprogram window locations
open all cams at once
Plugins?

** UX & Design **
more colors and all that
"""


# Imports
import cv2
import getpass
import hashlib
import os
import pathlib
import platform
import subprocess
import tempfile
import time

# vars
attempts = 0 # This is used to track logins
cam = 0 # with this as the default, it should go to the webcam automatically and not crash.
camInf = 0     # used in camInfo()
index = ""     # used in openCamFeed()
#name = ""      # store username globally, coming later, i'm getting ahead of myself in these updates.
numCams = 0    # used in camCount()
openCams = []
tempPath = ""  # used to create list of cams


# Definitions
# This is used to detect how many cameras are attached to the host.
def camCount(): # guess what: it works! the value is stored in numCams
    global numCams

    while True:
        try:
            cap = cv2.VideoCapture(numCams) # start a camera
            if not cap.isOpened(): # if one doesnt open, stop
                break

            numCams += 1 # counter for cameras found
            cap.release() # again, release or cv2 is pissy
        
        except:
            print("No cameras were detected on your system. Try reconnecting the cameras.")
            input()

    return numCams # return final camera count

def camInfo(filePath): # this is used to scrape data from the available cameras and save it to a temp file to be listed later.
    global camInf
    with open(filePath, 'w') as file:
        while True:
            try:
                cap = cv2.VideoCapture(camInf) # set the camera
                if not cap.isOpened(): # if the cam isn't found, exit the while loop
                    break

                # Get the info from the cameras
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)

                cameraInfo = f"Camera {camInf} - Index: {camInf}, Resolution: {width}x{height}, FPS: {fps}\n" # create a string of camera info, by adding the f in the front, it supports {}. That also works with print()

                file.write(cameraInfo)

                camInf += 1 # iterate to the next cam
                cap.release() # release so it doesn't get mad
            except:
                # prevent crash on no cams found
                print("No cameras were detected on your system. Try reconnecting the cameras.")
                break

def checkForAcc():
    findAcc = list(pathlib.Path('./').glob('*.rpscf')) # look for associated save filetypes

    if not findAcc: # none are found
        newAcc = input("No user accounts have been found. Would you like to make one? y/n\n> ").lower() # create new acc?

        # Handle new acc
        if newAcc == "y": # create new account
            # general advice to create an admin account
            print("\n\nYou are required to create the administrator account first. The username for this account will be \"admin\"\n")
            success = 0
            while success != 1:
                # collect creds
                newName = "admin"
                print("Please enter the password below, then confirm it. ")
                newPass1 = getpass.getpass()
                newPass2 = getpass.getpass()

                # confirm creds
                if newPass1 == newPass2:
                    print("\n\nCredentials confirmed, creating account\n") # create the account after this
                    success = 1

                    # generate filename
                    newAccName = newName + ".rpscf"

                    # encrypt password
                    ep = hashlib.new('sha256')
                    ep.update(newPass1.encode())

                    # write to new file
                    with open(newAccName, 'a+') as create:
                        create.write(str(ep.hexdigest()))

                    # Without this, it dumps the user straight in. Make them login.
                    print("Account creation successful! Please log in now! (Username: admin)\n\n")
                    login()

                else:
                    retry = input("Passwords do not match. Try again? y/n\n> ")

                    if retry == "y":
                        print("Returning to user creation.\n")
                    elif retry == "n":
                        input("Ending the program. Goodbye!")
                        quit()


        elif newAcc == "n":
            input("Account creation canceled. Goodbye!")
            quit()
        else:
            print("Input not understood")
        
    else: # acc is found
        #print("Not empty?") # call login() from here
        login()

def checkOpenCam(index): # the entire purpose of this is error handling. It checks if the camera is already streaming, then sends the user back accordingly.
    if index not in openCams: # this works perfectly, because any
         # This catches camera indices that are too high. Ill add low later if this works. Heres the math again to subtract that one difference.
        try: # this try loop prevents the program from adding "back" or other strings to openCams and then promptly breaking.
            int(index)
            if int(index) <= (numCams - 1):
                openCams.append(index)
            else:
                input("Sorry, that camera was not found, returning to camera selection...")
                openCamFeed()
        except:
            if index == "back": # this if loop was added for checking if the user typed "back"
                commandMode()
            elif index == "list":
                print("Fetching camera information...\n")
                printCamInfo(tempPath)
            else:
                input("Sorry but " + index + " is not a valid input. Please enter a number, press enter to continue.")
                index = ""
                commandMode()
    
    elif index in openCams:
        print("\nSorry, that camera is already streaming. Returning to camera selection menu...")
        input("Enter to continue...")
        openCamFeed()
    else:
        print("\nOopsie Poopsie, an unknown error has occured.")
        input("Devpoint1...")
        openCamFeed()


def clearTemps(ext): # this will be used to delete all temp files in the folder. Call at the beginning or end only.
    # create list of files in dir
    cd = os.getcwd()
    files = os.listdir(cd)

    # go through each file
    for file in files:
        if file.endswith(ext):
            curPath = os.path.join(cd, file) # curPath = current path

            try:
                os.remove(curPath)
                #print(f"Deleted: {curPath}") enable this to print what file was deleted and when.
            except Exception as e:
                print(f"Error deleting {curPath}: {e}")

def commandMode():
    os.system("cls")
    command = input("Choose an option: \n\"list\" to list all available cameras\n\"open\" to open a camera feed\n\"quit\" to exit the program\nand more coming later.\n\n> ").lower() # collect input

    # process the input
    if command == "list": # list the cameras
        printCamInfo(tempPath)
    elif command == "open":
        openCamFeed()
    elif command == "quit":
        clearTemps('.tmp')
        quit()
    else: # return on failure
        print("\nSorry, I didn't recognize that input. Please try again.\n\n")
        time.sleep(.5)
        commandMode()

def flag():
    stars = '\033[0;34m' # ANSI blue
    strip = '\033[91m' # ANSI red
    reset = '\033[0m'  # reset color

    # stripes
    pattern = [
        f"{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={strip}=======================",
        f"{stars}=={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}=={reset}{reset}=======================",
        f"{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={strip}=======================",
        f"{stars}=={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}=={reset}{reset}=======================",
        f"{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={strip}=======================",
        f"{stars}=={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}=={reset}{reset}=======================",
        f"{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={reset}*{stars}={strip}=======================",
        f"{reset}====================================",
        f"{strip}====================================",
        f"{reset}====================================",
        f"{strip}====================================",
        f"{reset}====================================",
        f"{strip}===================================={reset}",
    ]

    for line in pattern:
        if '=' in line:
            print(line)
        else:
            print(stars + line + reset)

def login(): # this will be used to login securely
    # kick out at three failed attempts
    global attempts # get this to track login attempts
    if attempts == 3:
        input("Too many failed attempts have been made, exiting now. Press enter to close...")
        quit()

    # collect creds
    global name
    name = input("Username: ")
    pwd = getpass.getpass()           # input("Password: ")

    # encrypt the password inputted to sha-256
    # use this to print the value   print(e.hexdigest())
    e = hashlib.new('sha256')
    e.update(pwd.encode())

    # create file name for search
    uname = name + '.rpscf'

    # search for the username
    try: # try to open the file
        with open(uname, 'r') as creds: # open the file
            val = creds.read() # read the file, line 1 will be the password.

        if val == e.hexdigest(): # If the saved hash = input hash, get past login.
            print("Login success") # Login code here
        else: # Password didn't work.
            print("Username / password is incorrect")
            attempts += 1 # add one
            login()
    except: # Failure if file not found
        print("\nUsername / password is incorrect\n")
        attempts += 1 # add one
        login()

def openCamFeed():
    index = input("\nPlease select a camera number to view. If you are unsure of what cameras are available, type \"list\"\nTo return to the main menu, type \"back\"\n\n> ") # collect input
    
    # check to see if the camera is already open
    checkOpenCam(index)
    
    # this is used to send numCams to a temp file
    prefix = "indexVal"
    suffix = ".tmp"
    with tempfile.NamedTemporaryFile(mode='w', prefix = prefix, suffix = suffix, delete=False, dir=".") as indexTemp:
        indexTemp.write(str(index))
    try: # this is hairy, but i took out a bunch of data type checking and nothing broke.
        int(index)
        print("Opening camera...\n\n\n")

        # open in new window
        if platform.system() == "Windows":
            subprocess.Popen(["python", "openCam.py"])

    except ValueError:
        if index == "list": # print the list of cams
            index = ""
            printCamInfo(tempPath)

        elif index == "back":
            index = ""
            commandMode()

        else: # return error
            print("Please enter a number with no other characters.")

    #return index
    commandMode()

def printCamInfo(tempPath):
    with open(tempPath, 'r') as file:
        content = file.read()
        print(content)
    input("\n\nPress enter to continue...")
    commandMode()

# runtime
# start the camera detection phase
def main():
    checkForAcc() # this leads to login() now, it won't be called in main() anymore.
    clearTemps('.tmp')
    os.system("cls")
    flag()
    print("\n\nWelcome to CCTV by RPS Systems. 2024\nSearching for cameras...\n\n")
    camCount() # Find the cameras
    os.system("cls") # this hides an error from finding the first nonexistant camera.
    flag()
    print("\n\nWelcome to CCTV by RPS Systems. 2024\nSearching for cameras...\n\nCameras found: " + str(numCams) + "\n\n") # reprint everything, jank asf but it werks

    # this section is used to create the temp file for the camera data.
    global tempPath
    tempPath = tempfile.mktemp() # create the temp
    open(tempPath, 'w').close() # clear any existing data
    camInfo(tempPath)


    # this is used to send numCams to a temp file
    prefix = "numCams"
    suffix = ".tmp"
    with tempfile.NamedTemporaryFile(mode='w', prefix = prefix, suffix = suffix, delete=False, dir=".") as openCamTemp:
        openCamTemp.write(str(numCams))

    os.system("cls") # another error hider
    # end camera detection phase

    # start command phase
    flag()
    print("Welcome to CCTV by RPS Systems. 2024\nSearching for cameras...\n\nCameras found: " + str(numCams) + "\n\nAll systems functional...\nPress any key to begin...") # reprint everything, jank asf but it werks
    input()

    while True:
        commandMode()

if __name__ == "__main__":
    main()