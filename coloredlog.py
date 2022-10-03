'''
Author : Philippe Saint-Amand
Date : 2022-10-03

Description:
    Goal of this script is to have possibility of :
    - standard python logging with extra level (SUCCESS)
    - colored console logging
    - Logging to file
    - Possibility to log on both conosle & file but using different formatter for console and log file
'''
import colorama as c
import logging
import os

class ColorFormatter(logging.Formatter):
    c.init(autoreset=True)
    color_reset = c.Style.RESET_ALL
    # Change this dictionary to suit your coloring needs!
    COLORS = {
        "DEBUG": c.Fore.MAGENTA,
        "INFO": c.Fore.BLUE,
        "SUCCESS": c.Fore.GREEN,   # This is a custom level
        "WARNING": c.Fore.YELLOW,
        "ERROR": c.Fore.RED,
        "CRITICAL": c.Fore.RED + c.Back.WHITE
    }
    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        if color:           
            record.levelname = color + record.levelname
            record.msg = record.msg  + self.color_reset 
        return logging.Formatter.format(self, record)

class ColorLogger(logging.Logger):
    def __init__(self, name="log", console=True, logfile="", console_level=logging.WARNING, file_level=logging.DEBUG):
        # self = logging.getLogger(name)
        # self.setLevel(logging.DEBUG)        
        logging.Logger.__init__(self, name, logging.DEBUG)
        if logfile:
            path = os.path.dirname(os.path.abspath(logfile))
            if path and not os.path.exists(path):
                os.makedirs(path)                   #create logging directory if not exists

            fh = logging.FileHandler(logfile, encoding='utf-8')
            fh.setLevel(file_level)
            fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.addHandler(fh)

        # Put the console handler as last otherwise message is modified with color and appear as well in the file
        if console:
            ch = logging.StreamHandler()
            ch.setLevel(console_level)
            ch.setFormatter(ColorFormatter("%(levelname)s - %(message)s"))
            self.addHandler(ch)

if __name__ == "__main__":
    # Some usefull variables 
    SUCCESS = 25
    APPNAME, _ = os.path.splitext(os.path.basename(__file__))
    CUR_DIR=os.path.dirname(os.path.abspath(__file__))
    LOG_DIR=os.path.join(CUR_DIR,"log")
    LOGFILE = os.path.join(LOG_DIR,APPNAME+".log")
    # LOGFILE = APPNAME+".log"

    # Sample loggin creation with logging entries
    logging.addLevelName(SUCCESS, 'SUCCESS')
    logger = ColorLogger(name=APPNAME, console=True, logfile=LOGFILE, console_level=SUCCESS)
    logger.debug('This message should go to the log file')
    logger.info('So should this')
    logger.warning('And this, too')
    logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
    logger.critical('Try a critical message')
    logger.log(SUCCESS, 'Then success level that is a custom level')