import mogdevice

'''
Pretty much rewrite all of this,

-   will need a property detector
overall driver will be a class
'''
class wavemeter_driver:
    wm = None
    connection_status = False


    # parameterized constructor
    def __init__(self, link):
        
        self.connect_to_wavemeter(link)

    
    # attempts to create a connecting with the wavemeter
    def connect_to_wavemeter(self, link):
         
        self.connection_status = True
        try: 
            self.wm = mogdevice.MOGDevice('mog-fzw-a03052.graulab.odu.edu')
        except Exception as e:
            self.connection_status = False
            print("wavemter error:", e)
    
    
    # gets the wavelength
    def getWL(self, laserNumber):
        #checks the wavemeter's connection
        if self.connection_status == False:
            return 'Wavemeter connection failure'

        #sets the laser to the specified input
        #sockets 1 through 8 
        if 1 <= laserNumber <= 8:
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
    


#x = wavemeter_driver('mog-fzw-a03052.graulab.odu.edu')
#print(x.getWL(1))