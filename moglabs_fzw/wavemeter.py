import moglabs_fzw.mogdevice as mogdevice
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
        for i in range(10):
            try: 
                self._device = mogdevice.MOGDevice(link)
                break
            except Exception as e:
                print("wavemter connection error ",attempt, ":", e)
                time.sleep(1)
    
    # checks the connection to the wavemeter
    def connection_status(self):
        return self._device.connected()
    
    # changes the wavemeter's optical fiber input port
    def set_port(self, port):
        if(0 < port <= 8):
            self._device.ask(f'optsw,set,{port}')
            print('port:', port)
        else:
            raise IndexError


    # overrides the index operator
    def __getitem__(self, channel_index): #will return the object of the correct channel
        
        # ensure that the index is a valid channel
        if(0 < channel_index <= 8):
            print('index: ', channel_index)
            return Channel(self._device, channel_index)
        else:
            raise IndexError
        
    # makes a representation of the wavemeter object
    def __repr__(self):
        return 'Wavemeter(\' \')'




class Channel:
    _device = None
    _index: int=0
    _etalon = 0
    def __init__(self, device, index):
        self._device = device
        self._index = index
        self._device.ask('optsw,select,'+str(index))


    @property
    def wavelength(self):
        # changes sockets the wavemeter is measuring
        self._device.ask('optsw,select,'+str(self._index))

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
        return Fringe(self._device)
    
    
    


class Fringe:
    _device = None
    _etalon_index: int=0

    def __init__(self, _device):
        self._device = _device

    @property
    def _fringe(self):
        '''Returns the interference fringe as a numpy array'''
        array = np.frombuffer(self._device.ask_bin(f'meas,img,{self._etalon_index}'), dtype='uint8')
        return array[:512-len(array)]
        #returns a 512 byte array, this removes the extra data

    
    # overrides the index operator
    def __getitem__(self, etalon_index): 
        #checks the index
        if(0 <= etalon_index <= 3):
            self._etalon_index = etalon_index
            return self._fringe
        else:
            raise IndexError