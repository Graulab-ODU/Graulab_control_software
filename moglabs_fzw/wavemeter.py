import mogdevice 
import time

class Wavemeter:
    _device = None
    _addr = ''


    # parameterized consctor
    def __init__(self, address):
        self._addr = address
        self._connect_to_wavemeter(self._addr)

    
    # attempts to create a connecting with the wavemeter
    def _connect_to_wavemeter(self, addr):
         #will ensure that it is not on its 10th connection attempt
        for i in range(10):
            try: 
                self._device = mogdevice.MOGDevice(addr)
                break
            except Exception as e:
                print("wavemter connection error ",i, ":", e)
                time.sleep(1)
    
    # checks the connection to the wavemeter
    def connection_status(self):
        return self._device.connected()
    
    # changes the wavemeter's optical fiber input port
    def set_port(self, channel_index):
        if(channel_index in (1,2,3,4,5,6,7,8)):
            self._device.ask(f'optsw,set,{channel_index}')
            print('port:', channel_index)
        else:
            raise IndexError


    # overrides the index operator
    def __getitem__(self, channel_index): #will return the object of the correct channel
        
        # ensure that the index is a valid channel
        if(channel_index in (1,2,3,4,5,6,7,8)):
            return Channel(self._device, channel_index)
        else:
            raise IndexError
        
    # makes a representation of the wavemeter object
    def __repr__(self):
        return f'Wavemeter(\'{self._addr}\')'




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
    

    def __repr__(self):
        return f'(Channel {self._index}): Wavelength: {self.wavelength}'

    @property
    def fringe(self):
        '''Returns the all 4 interference fringes as an array'''
        
        #collected fringes 0 through 3, and converts them from byte array to a list
        array0 = list(self._device.ask_bin(f'meas,img,0'))
        array1 = list(self._device.ask_bin(f'meas,img,1'))
        array2 = list(self._device.ask_bin(f'meas,img,2'))
        array3 = list(self._device.ask_bin(f'meas,img,3'))

        #returns all 4 lists, removes any extra data beyond the 512th index
        return array0[:512-len(array0)], array1[:512-len(array1)], array2[:512-len(array2)], array3[:512-len(array3)]

    @property
    def fringe0(self):
        '''Returns only the 0th interference fringe as an array'''
        
        #collected fringe 0 converts it from byte array to a list
        array = list(self._device.ask_bin(f'meas,img,0'))

        #returns the list and removes any extra data beyond the 512th index
        return array[:512-len(array)]
    
    @property
    def fringe1(self):
        '''Returns only the 1st interference fringe as an array'''
        
        #collected fringe 1 converts it from byte array to a list
        array = list(self._device.ask_bin(f'meas,img,1'))

        #returns the list and removes any extra data beyond the 512th index
        return array[:512-len(array)]
    
    @property
    def fringe2(self):
        '''Returns only the 2nd interference fringe as an array'''
        
        #collected fringe 2 converts it from byte array to a list
        array = list(self._device.ask_bin(f'meas,img,2'))

        #returns the list and removes any extra data beyond the 512th index
        return array[:512-len(array)]
    
    @property
    def fringe3(self):
        '''Returns only the 3rd interference fringe as an array'''
        
        #collected fringe 3 converts it from byte array to a list
        array = list(self._device.ask_bin(f'meas,img,3'))

        #returns the list and removes any extra data beyond the 512th index
        return array[:512-len(array)]

