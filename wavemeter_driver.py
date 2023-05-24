import mogdevice
import time


class Wavemeter_driver:
    wm = None
    connection_status2 = False

    # parameterized constructor
    def __init__(self, link):
        
        self.connect_to_wavemeter(link)

    
    # attempts to create a connecting with the wavemeter
    def connect_to_wavemeter(self, link, attempt=0):
         #will ensure that it is not on its 10th connection attempt
        if attempt >= 10:
            print('Wavemeter Connection Failure')
            return

        self.connection_status2 = False
        try: 
            self.wm = mogdevice.MOGDevice('mog-fzw-a03052.graulab.odu.edu')
            self.connection_status2 = True
        except Exception as e:
            print("wavemter connection error ",attempt, ":", e)
            time.sleep(1)
            self.connect_to_wavemeter(link, attempt+1)
    
    # gets the wavelength
    @property
    def getWL(self):
        laserNumber = 1
        #checks the wavemeter's connection
        if self.connection_status2 == False:
            return 'Wavemeter connection failure'

        # if input is not 1-8, it will be set to 1
        if 1 > laserNumber or laserNumber > 8:
            laserNumber = 1
        else:
            self.wm.ask('optsw,set,'+str(laserNumber))

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
    
