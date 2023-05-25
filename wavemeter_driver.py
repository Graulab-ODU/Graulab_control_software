import mogdevice
import time
import numpy as np

class Wavemeter:
    _device = None


    # parameterized consctor
    def __init__(self, link):
        
        self._connect_to_wavemeter(link)

    
    # attempts to create a connecting with the wavemeter
    def _connect_to_wavemeter(self, link, attempt=0):
         #will ensure that it is not on its 10th connection attempt
        if attempt >= 10:
            print('Wavemeter Connection Failure')
            return

        try: 
            self._device = mogdevice.MOGDevice(link)
        except Exception as e:
            print("wavemter connection error ",attempt, ":", e)
            time.sleep(1)
            self._connect_to_wavemeter(link, attempt+1)

        
    

    # gets the wavelength
    @property
    def getWL(self):
        laserNumber = 1
        #checks the wavemeter's connection
        if self.connection_status == False:
            return 'Wavemeter connection failure'

        
        #will attempt to measure the wavelength, if it fails it returns 'low contrast'
        try:
            wl = self.wm.ask('meas,wl')
        except RuntimeError:
            return 'Low Contrast'
        return wl 
    
    # checks the connection to the wavemeter
    def connection_status(self):
        return self._device.connected()


    # overrides the index operator
    def __getitem__(self, channel_index): #will return the object of the correct channel
        print('index: ', channel_index)
        return Channel(self._device, channel_index)
        
    # makes a representation of the wavemeter object
    def __repr__(self):
        return 'Wavemeter(\'\')'

    
    
    



class Channel:
    _device = None
    _index: int=0
    def __init__(self, device, index):

        # if input is not 1-8, it will be set to 1
        if 1 > index or index > 8:
            index = 1

        self._device = device
        self._index = index

        
        self._device.ask('optsw,set,'+str(index))


        
    
    @property
    def wavelength(self):
        # changes sockets the wavemeter is measuring
        self._device.ask('optsw,set,'+str(self._index))

        #will attempt to measure the wavelength, if it fails it returns 'low contrast'
        try:
            wl = self._device.ask('meas,wl,vac')
            value = float(wl.replace('nm(vac)', ''))
        except RuntimeError:
            return 'Low Contrast'
        return value

    @property
    def fringe(self):
        '''Returns the interference fringe as a numpy array'''
        return np.frombuffer(self._device.ask_bin('meas,img,2'), dtype='uint8')

#numpy.frombuffer(_device.ask_bin('meas,img,{_index}), dtype='uint8')

#add functions for the interference fringe (there are two of them)
#   wm.ask('meas,contrast')  measures the contrast which is the fringe quality
#  the saturation is the fringe quality