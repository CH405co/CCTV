# Imports
import cv2

cam = 0 # with this as the default, it should go to the webcam automatically and not crash.
numCams = 0
# Definitions
# This is used to detect how many cameras are attached to the host.
def camCount(): # guess what: it works! the value is stored in numCams
    global numCams

    while True:
        cap = cv2.VideoCapture(numCams) # start a camera
        if not cap.isOpened(): # if one doesnt open, stop
            break

        numCams += 1 # counter for cameras found
        cap.release() # again, release or cv2 is pissy

    return numCams # return final camera count

def close():
    print("Bye have a great day")
    exit()


# This one should show the camera display
def display_camera(camera):
    cap = cv2.VideoCapture(camera) # Setup the capture, store in a var

    # The code gets pissy if i put this by the elifs, so these vars are for the elifs and cam verification only.
    global cam      # frig so this starts at 0, while
    global numCams  # this starts at 1. This throws off the checking math. Easy fix, found by printing these vars after calling globals.
                    # ~some~ indices start at zero, others do not :)

    while True:
        ret, frame = cap.read() # by god do not remove the ret variable. It isn't in use but cv2 needs it to function.
        cv2.imshow('Camera Feed', frame) # Show the stream

        # Listen for inputs, handle them
        if cv2.waitKey(1) & 0xFF == ord('q'): # press q to quit. This shit was so finnicky
            break

        # Here is the improved cam selection code. It shouldn't crash anymore.
        elif cv2.waitKey(1) & 0xFF == ord('d'): # press d to move up a cam. Takes forever
            if cam < (numCams - 1): # if less than, go up. # The one is subtracted to fix the math as mentioned in the global calls. 
                print("Switching cameras...") # This is just a UX thing.
                cam += 1
                return cam
            else:
                print("sorry, this is the top camera. Press a to go down a camera") # we could store the hotkeys in a variable and replace a with whatever the user wants, that way they can change inputs. neat idea.
            
        elif cv2.waitKey(1) & 0xFF == ord('a'): # press a to do down a cam. takes way too long.
            if cam > 0: # this has to be zero, the number of cameras does not matter, the camera cannot be in the negatives. DUH stoopit. By having the same math as going up cameras, it would get stuck in the top cam.
                print("Switching cameras...") # This is just a UX thing.
                cam -= 1
                return cam
            else:
                print("sorry, this is the bottom camera. Press d to go up a camera")    
    cap.release() # cv2 gets pissy if you don't have the release statement. 
    cv2.destroyAllWindows()
    close() # end the program

# run
print("Detecting cameras...")
camCount() # count the cameras, this will be used to prevent the user from attempting to access a camera that does not exist (prevents crashes!)
print("Cameras found: " + str(numCams))
while True:
    cam # leave this, it passes to display_camera(). Breaks without it.
    display_camera(camera = cam) # start a video feed
