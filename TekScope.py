import vxi11

class TekScope(vxi11.Instrument):
    '''
    A class that uses the vxi11 library to interface a
    Tektronix MSO6 scope.

    Check out https://github.com/python-ivi/python-vxi11

    Last modified: 22/10/2020 by Eugenio Senes
    '''

    def __init__(self, hostname):
        super().__init__(hostname)
        print(self.ask('*IDN?'))
        self.write('HEADer ON')

    # ----- OVERLOAD
    def query(self, message):
        return self.ask(message)

    # ----- GENERAL SETTINGS


    # ----- FILESYSTEM MANAGEMENT
    def ls_full_directory(self):
        return self.query('FIlESystem:DIR?')

    def ls_with_details(self):
        '''
        Returns the detailed file list: for every file you get
        "name; type; size; modification date; modification time"
        '''
        return self.query('FIlESystem:LDIR?')

    def get_current_dir(self):
        return self.query('FILESystem:CWD?').split(' ')[-1]

    def set_current_dir(self, dirname):
        '''
        This directory must exist. Otherwise no error and not set.
        '''
        return self.write('FILESystem:CWD \"'+dirname+'\"')

    def homedir(self):
        return self.query('FILESystem:HOMEDir?').split(' ')[-1]

    def rmdir(self, dirname):
        '''
        Removes directory, but it must be empty
        '''
        self.write('FILESystem:RMDir \"'+dirname+'\"')

    def mkdir(self, dirname):
        self.write('FILESystem:MKDir \"'+dirname+'\"')

    def delete(self, fname):
        self.write('FILESystem:DELEte \"'+fname+'\"')

    def rename(self, fname, new_name):
        self.write('FILESystem:REName \"'+fname+'\",\"'+new_name+'\"')

    def copy(self, fname, destination):
        self.write('FILESystem:COPy \"'+fname+'\",\"'+destination+'\"')

    def unmount_usb(self):
        self.write('FILESystem:UNMOUNT:DRIve')

    # ----- ACQUISITION MANAGEMENT
    def acquisition_general_state(self):
        return self.query('ACQUIRE?')

    def get_acquisition_mode(self):
        return self.query('ACQUIRE:MODe?')

    def set_acquisition_mode(self, state, single_mode=True):
        # acquisition setting, tracewise
        if state in ['SAMple', 'PEAKdetect', 'HIRes', 'AVErage', 'ENVelope']:
            self.write('ACQUIRE:MODe '+state)
        else:
            raise ValueError('Unkonwn state')
        #acquisition setting, shotwise
        if single_mode:
            self.write('ACQuire:STOPAfter SEQUENCE')
        else:
            self.write('ACQuire:STOPAfter RUNSTop')

    ### START/STOP ACQUISITION
    def acquisition_start(self):
        self.write('ACQUIRE:STATE 1')

    def acquisition_stop(self):
        self.write('ACQUIRE:STATE 0')

    def acquisition_is_running(self):
        return self.query('ACQUIRE:STATE?')

    def get_acquisition_number(self):
        '''
        Return the acquisition number from the last RUN command
        '''
        return int(self.query('ACQUIRE:NUMAcq?').split(' ')[-1])
    ### AVERAGING MODE --> set mode AVErage
    def get_number_averages(self):
        return int((self.query('ACQUIRE:NUMAVg?')).split(' ')[-1])

    def set_number_averages(self, num_avg):
        self.write('ACQUIRE:NUMAVg '+str(num_avg))
    ### SEQUENCE MODE --> how many trigger events are acquired
    def get_acquisition_sequence_length(self):
        return int((self.query('ACQUIRE:SEQuence:NUMSEQuence?')).split(' ')[-1])

    def set_acquisition_sequence_length(self, num_acq):
        self.write('ACQUIRE:SEQuence:NUMSEQuence '+str(num_acq))

    def get_acquisition_sequence_number(self):
        '''
        During a sequence acquisition, returns the current acquisition number
        '''
        return int((self.query('ACQUIRE:SEQuence:CURrent?')).split(' ')[-1])
    ### FAST ACQUISITION
    def set_fast_acquisition(self, state):
        if state in ['ON', 'OFF']:
            self.write('ACQUIRE:FASTACQ:STATE '+state)
        else:
            raise ValueError('State must be ON or OFF')

    def get_fast_acquitsition(self):
        return (self.query('ACQUIRE:FASTACQ:STATE?')).split(' ')[-1]

    # ----- SAVE COMMANDS
    def set_save_destination(self, path):
        self.write("SAVEON:FILE:DEST \""+path+'\"')

    def get_save_destination(self):
        return (self.query("SAVEON:FILE:DEST?")).split(' ')[-1]

    def set_save_on_trigger(self, state):
        if state in ['ON', 'OFF']:
            self.write('SAVEON:TRIGger '+state)
        else:
            raise ValueError('State must be ON or OFF')

    def set_save_waveform(self, state, file_format):
        '''
        Set save waveform on trigger. State = ON/OFF.
        Format = INTERNal / SPREADSheet
        '''
        if state in ['ON', 'OFF']:
            self.write('SAVEON:WAVEform '+state)
            if file_format in ['INTERNal','SPREADSheet']:
                self.write('SAVEON:WAVEform:FILEFormat '+file_format)
            else:
                raise ValueError('Invalid file format')
        else:
            raise ValueError('State must be ON or OFF')

    def set_save_channel(self, channel):
        if channel in ['CH1', 'CH2', 'CH3', 'CH4', 'ALL']:
            self.write('SAVEON:WAVEform:SOURce '+channel)
        else:
            raise ValueError('Invalid channel')

    ## TODO: the getters ...

    # ----- CUSTOM ACQUISTION SETUP
    def setup_single_acquisition(self, shot_number):
        '''
        An acquisition of N shots.
        Then the trigger stops.
        Result --> N traces (saved, if required to)
        '''
        self.acquisition_stop()
        self.set_acquisition_mode('SAMple', single_mode=True)
        self.set_acquisition_sequence_length(shot_number)

    def setup_average_acquisition(self, avg_number):
        '''
        An acquisition of the average of N shots.
        Then the trigger stops.
        Result --> 1 trace (saved, if required to)
        '''
        self.acquisition_stop()
        self.set_acquisition_mode('AVErage', single_mode=True)
        self.set_number_averages(avg_number)

    def setup_save_traces(self, save_folder, channel):
        '''
        Setup to save on each trigger the traces in .xls format.
        Channels: CH1, ..., ALL
        It will try to create the destination folder.
        '''
        self.acquisition_stop()
        self.mkdir(save_folder)
        self.set_save_destination(save_folder)
        self.set_save_on_trigger('ON')
        self.set_save_waveform('ON', 'SPREADSheet')
        self.set_save_channel(channel)
