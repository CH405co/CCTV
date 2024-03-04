from init import clearTemps
import cv2
import os

# vars
index = ""
numCams = 0

# read indexVal.tmp
def findIndex(dir, prefix):
    files = os.listdir(dir)
    file = [file for file in files if file.startswith(prefix)] # from here on I will just be changing the file var value, too many names gets confusing.

    # strip the list attribute from the file name
    file = str(file[0])

    #read the file
    with open(file, "r") as file:
        index = file.read()

    # convert the content of the temp file back into an int
    index = int(index)

    # return the number of the camera
    return index

# read numCams.tmp
def findNumCams(dir, prefix):
    files = os.listdir(dir)
    file = [file for file in files if file.startswith(prefix)] # from here on I will just be changing the file var value, too many names gets confusing.

    # strip the list attribute from the file name
    file = str(file[0])

    #read the file
    with open(file, "r") as file:
        numCams = file.read()

    # convert the content of the temp file back into an int
    numCams = int(numCams)

    # return the number of the camera
    return numCams

def main(): # idk how much I want to get into nested functions
    dir = "."
    prefix = "index"
    prefix2 = "numCams" # god i hate this, sorry but this naming convention just works.
    index = findIndex(dir, prefix) # get the value of index
    numCams = findNumCams(dir, prefix2) # get the value of numCams
    imshow = "Camera: " + str(index)
    if index >= 0: # Root out out of scope ints, negative nums
        if index <= numCams: # root out ints too big
            cap = cv2.VideoCapture(index)
            while True:
                ret, frame = cap.read()
                cv2.imshow(imshow, frame)

                if cv2.waitKey(1) & 0xFF == ord('q'): # listen for the user to press q to quit.
                    break
        else:
            print("Sorry, that camera cannot be found. Please refer to \"list\" for available cameras")
    else:
            print("Sorry, that camera cannot be found. Please refer to \"list\" for available cameras")


main()