from rpyc import connect

class Laser:

    _controller = None
    _controller_name = ''
    _laser_number = 0

    # establishes connection
    def __init__(self, name, controller, laser_number, port_=9000):
        
        try:
            self._network_Connection = connect(name, port=port_)
        except:
            print("Network connection Failure")
            return
        self._controller_name = controller
        
        # ensures laser number is between 1 and 2
        assert(laser_number in (1, 2))
        self._laser_number = laser_number
        self._controller = self._network_Connection.root.controllers[controller]
        

    # returns the emission status of the chose laser
    def get_emission(self):
        return self._controller.get(f'{self._laser_number}emission')


    # returns the voltage offset of the chose laser
    def get_voltage_offset(self):
        return self._controller.get(f'laser{self._laser_number}.scan.offset')


    # Sets a laser to a chosen laser offset
    def set_voltage_offset(self, voltage_offset):
        return self._controller.set(f'laser{self._laser_number}.scan.offset', voltage_offset)
    
    def __repr__(self):
        return f'DLC_Pro_controller({self._controller_name})'