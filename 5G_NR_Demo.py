
import sys

sys.path.append("./x64")

import Leap,thread, time

from socket import *

RX=RY=RZ=0
LX=LY=LZ=0
gHandExist = False

UDP_SERVER = "192.168.1.12"
#UDP_SERVER = "192.168.16.116"
UDP_PORT = 6666
DEST_PORT= 9999

def send_data(sock, dat):
    if sock:
        sock.sendto(dat, (UDP_SERVER, DEST_PORT))
        print "LEFT Hand: X=%d Y=%d Z=%d RIGHT Hand: X=%d Y=%d Z=%d \n" % (LX,LY,LZ, RX,RY,RZ)
    pass
    
def TaskProc():
    global LX,LY,LZ,RX,RY,RZ
    
    #Init socket
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(('0.0.0.0',UDP_PORT))
    
    
    while True:
        if gHandExist:
            #print "LEFT Hand: X=%d Y=%d Z=%d RIGHT Hand: X=%d Y=%d Z=%d \n" % (LX,LY,LZ, RX,RY,RZ)
            time.sleep(0.1)
            if LZ < -30 and RZ < -30:
                print 'FORWARD'
                send_data(s, "FORWARD")
            elif LZ > 60 and RZ > 60:
                print 'BACK'
                send_data(s, "BACK")
            elif LZ < -30 and RZ > 60:
                print 'RIGHT'
                send_data(s, "RIGHT")
            elif LZ > 60 and RZ < -30:
                print 'LEFT'
                send_data(s, "LEFT")
            elif LY <90 and RY <90 :
                print 'DIG'
                send_data(s, "DIG")
            elif LY > 180 and RY > 180:
                print 'LIFT'
                send_data(s, "LIFT")
            else:
                pass
                
            
    pass
    
class SampleListener(Leap.Listener):
    
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        global LX,LY,LZ,RX,RY,RZ,gHandExist
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
        #      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            #print "  %s, id %d, position: %s" % (
            #    handType, hand.id, hand.palm_position)
            
            pos = hand.palm_position
            
            if hand.is_left:
                #print 'Left hand: X=%d Y=%d Z=%d \n' % (int(pos[0]), int(pos[1]), int(pos[2]))
                LX = int(pos[0])
                LY = int(pos[1])
                LZ = int(pos[2])
            else:
                #print 'Right hand: X=%d Y=%d Z=%d \n' % (int(pos[0]), int(pos[1]), int(pos[2]))
                RX = int(pos[0])
                RY = int(pos[1])
                RZ = int(pos[2])
            pass
            
        if not frame.hands.is_empty:
            #print "#"
            gHandExist = True
            pass
        else:
            gHandExist = False
            
def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    thread.start_new_thread(TaskProc,())
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)
    

if __name__ == "__main__":
    main()
