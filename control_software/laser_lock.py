from .moglabs_fzw import Wavemeter
from .DLC_Pro_Controller import Laser
from simple_pid import PID
import time

class Laser_lock:
    #possible DLC controllers: Barium, Photoionization, Lutetium_848nm_1244nm, Lutetium_646nm

    # laser wavelength in nm        493          650                646                     646                     848                  1052           413
    _wavemeter_port_reference=[['Barium', 1], ['Barium', 2], ['Lutetium_646nm', 2], ['Lutetium_646nm', 1], ['Lutetium_848nm_1244nm', 2], [0], ['Photoionization', 2]]# port 8 is not set up, and port 6 laser uses a different control system
    _PID_CONSTANTS =   [[626, 613.6363, 0],[626, 613.6363, 0],[626, 613.6363, 0],   [626, 613.6363, 0],    [626, 613.6363, 0],  [626, 613.6363, 0], [382.5, 459, 0]]
    # only 646 and 413 have been calibrated with the PID, all others are using default values

    _wavemeter_channel = 1
    _wavemeter = None
    _wavemeter_address = None
    _laser = None

    def __init__(self, wavemeter_address, network_address, laser_controller, laser_number):
        self._wavemeter_address = wavemeter_address
        
        #sets up connecting to the wavemeter
        self._wavemeter = Wavemeter(wavemeter_address)

        # sets up connection to the DLC_Pro_Controller and laser
        self._laser = Laser(network_address, laser_controller, laser_number)

        #finds the proper wavemeter port
        for i in range(len(self._wavemeter_port_reference)):
            if (self._wavemeter_port_reference[i] == [laser_controller, laser_number]):
                self._wavemeter_channel = i + 1
                return
        raise Exception("Laser not connected to the Wavemeter")
    
    # will lock the lasers to a certain wavelength
    def set_wavelength(self, setpoint_, Kp=_PID_CONSTANTS[_wavemeter_channel][0], Ki=_PID_CONSTANTS[_wavemeter_channel][1], 
                       Kd=_PID_CONSTANTS[_wavemeter_channel][2], time_running=-1, interval_delay=0.2, max_voltage=130, min_voltage=30, max_voltage_change=5):
        '''
            setpoint: target value
            Kp, Ki, Kd: PID constants
            time_running: number of minutes that the loop will run
        
        '''
        #because of how decreasing voltage increases the wavelength, Kp and Ki must be negative
        Kp = min(Kp, Kp*-1)
        Ki = min(Ki, Ki*-1)
        
        pid = PID(Kp, Ki, Kd, setpoint=setpoint_)
        change = 0
        index = 0
        
        previous_wavelength = self.get_wavelength()
        
        #if 0 will run untill interrupted, else it will run 
        while (True if time_running == -1 else (time_running *(1/interval_delay)) > index): #time running is in seconds

            st=time.time()

            #protects the program from crashing if the laser enters multi-mode/connection time outs
            try:
                wavelength = self.get_wavelength()
            except:
                wavelength = previous_wavelength
            if (type(wavelength) != float):
                wavelength = previous_wavelength

            #adds deadzone to the wavelength value
            wavelength = float(int(wavelength*100000))/100000

            #Runs the PID
            change = pid(wavelength)   

            #makes sure the change in voltage is not beyond the given max change
            change = self._interval_clamp(change, max_voltage_change*-1, max_voltage_change)


            #calculates what the new voltage offset will be and keeps it in a specific interval
            new_voltage = self._interval_clamp(self.get_voltage_offset()+(change), min_voltage, max_voltage)

            #alters the voltage according to the change from the pid
            self.set_voltage_offset(new_voltage)

            #updates previous_wavelength
            if (type(wavelength) == float):
                previous_wavelength = wavelength
            
            #ensure the program pauses is equal to the given interval_delay or how long the program takes to run
            et = time.time()
            time.sleep((interval_delay-(et-st)) if (interval_delay-(et-st)) > 0 else 0)
            index += 1
            
    
    #will repeadidly swap the target wavelengths
    #parameter wavelengths is a list
    #parameter wl_swapping is in seconds, total time rinning is in minutes
    def set__wavelengths(self, wavelengths, wl_swapping_interval = 1, total_time_running = -1):
        index = 0

        start_time = time.time()

        while (True if total_time_running == -1 else (time.time() - start_time <= total_time_running*60)): 
            
            for wl in wavelengths:

                #print('wavelength swap')
                self.set__wavelengths(wl, time_running = wl_swapping_interval)



    # returns laser's wavelength in nm(vac)
    def get_wavelength(self):
        return self._wavemeter[self._wavemeter_channel].wavelength
    
    # gets the laser voltage offset
    def get_voltage_offset(self):
        return self._laser.get_voltage_offset()
    
    #sets the laser votage offset
    def set_voltage_offset(self, offset):
        self._laser.set_voltage_offset(offset)

    #returns wavemeter port
    def get_wavemeter_port(self):
        return self._wavemeter_channel
    
    #will return the value if it is in the given interval, or the value closest to it in the interval
    def _interval_clamp(self, x, minval, maxval):
        return min(max(x, minval), maxval)
