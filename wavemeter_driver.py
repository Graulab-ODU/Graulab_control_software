import mogdevice
import time


class Wavemeter_driver:
    wm = None


    # parameterized constructor
    def __init__(self, link):
        
        self.connect_to_wavemeter(link)

    
    # attempts to create a connecting with the wavemeter
    def connect_to_wavemeter(self, link, attempt=0):
         #will ensure that it is not on its 10th connection attempt
        if attempt >= 10:
            print('Wavemeter Connection Failure')
            return

        try: 
            self.wm = mogdevice.MOGDevice('mog-fzw-a03052.graulab.odu.edu')
        except Exception as e:
            print("wavemter connection error ",attempt, ":", e)
            time.sleep(1)
            self.connect_to_wavemeter(link, attempt+1)
    
    # gets the wavelength
    @property
    def getWL(self):
        laserNumber = 1
        #checks the wavemeter's connection
        if self.connection_status == False:
            return 'Wavemeter connection failure'

        #sets the laser to the specified input
        #sockets 1 through 8 
        if 1 <= laserNumber <= 8:
            self.wm.ask('optsw,set,'+str(laserNumber))
        else:
            self.wm.ask('optsw,set,1')

        #will attempt to measure the wavelength, if it fails it returns 'low contrast'
        try:
            wl = self.wm.ask('meas,wl')
        except RuntimeError:
            return 'Low Contrast'
        return wl 
    

    # checks the connection to the wavemeter
    def connection_status(self):
        return self.wm.connected()
    
    # will reconnect to the wavemeter
    def reconnect(self,timeout=1,check=True): 
        self.wm.reconnect(timeout, check)
    


#x = Wavemeter_driver('mog-fzw-a03052.graulab.odu.edu')

#print('wavemeter connection: ', x.connection_status)
#print('wavelength: ', x.getWL)