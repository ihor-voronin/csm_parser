from backports import configparser


class Config:
    __conf = None

    clean_after_processing = False

    @staticmethod
    def config():
        if Config.__conf is None:  # Read only once, lazy.
            Config.__conf = configparser.ConfigParser()
            Config.__conf.read("config.ini")
        return Config.__conf
