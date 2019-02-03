from gpiozero import DigitalOutputDevice


class Relay(DigitalOutputDevice):
    
    def __init__(self, pin):
        '''
        Relays are active low so set the default of active_high to False.
        This prevents all of the relays from turning on then off when
        initializing.
        '''
        super().__init__(pin, active_high=False)

