import logging
import os
from datetime import datetime

LOG_FILE=f'{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log' # format of our log files in str "05_06_2024_10_20_59.log"

log_path=os.path.join(os.getcwd(),"logs") #choose a desire path for our folder
os.makedirs(log_path, exist_ok=True) # create the folder of the path
LOG_FILE_PATH=os.path.join(log_path, LOG_FILE) # create a path for the file directly

logging.basicConfig(level=logging.INFO,
        filename=LOG_FILE_PATH,
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
        )

