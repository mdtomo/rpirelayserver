from pathlib import Path


class Config:

    host = '127.0.0.1'
    port = 2018
    log_level = 10 # DEBUG
    log_format = '%(asctime)s: %(levelname)s: %(module)s/%(funcName)s: %(message)s'
    save_path = Path.cwd() / 'data' / 'status.sav'
    gpios = (23, 24, 25, 26, 6, 5, 22, 27)