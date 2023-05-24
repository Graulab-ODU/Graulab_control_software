import mogdevice
import time


class Wavemeter:
    _device = None


    # parameterized consctor
    def __init__(self, link):
        
        self._connect(link)

    
    # attempts to create a connecting with the wavemeter
    def _connect(self, link, attempt=0):
         #will ensure that it is not on its 10th connection attempt
        if attempt >= 10:
            print('Wavemeter Connection Failure')
            return

        try: 
            self.wm = mogdevice.MOGDevice(link)
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


    # overrides the index operator
    def __getitem__(self, channel): #will return the object of the correct channel
        return self.channels.wavelength(channel)
        
    # makes a representation of the wavemeter object
    def __repr__(self):
        return 'Wavemeter(\'\')'

    
    
    



class Channel:
    _device = None

    def __init__(self, device):
        self._device = device

    
    def wavelength(self, channel):
        self._device.ask('optsw,set,'+str(channel))
        return self.wavelength_1
        
    @property
    def wavelength_1(self):
        self.device.ask('optsw,set,1')