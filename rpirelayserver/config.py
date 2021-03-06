from pathlib import Path


class Config:

    host = '192.168.0.15' # use 127.0.0.1 if running both client and server on the Raspberry Pi.
    port = 2018
    log_level = 10 # DEBUG
    log_format = '%(asctime)s: %(levelname)s: %(module)s/%(funcName)s: %(message)s'
    log_to_file = True
    log_file_path = Path.cwd() / 'data' / 'log.log'
    save_path = Path.cwd() / 'data' / 'status.sav'
    gpios = (23, 24, 25, 26, 6, 5, 22, 27) # Set to the outputs you are using.
