# Ori
from os import path
from datetime import datetime
from time import sleep
import random as rd

# Pip
from pywebio.output import put_image as pw_put_image
import cv2
from subprocess import run as adb_run, DEVNULL, PIPE

# Private
import utils.config as cfg
import utils.log as log
from utils.PPOCR_api import GetOcrApi
import utils.adb as adb

class test_case:
    def __init__(self):
        self.start = self.start()
    
    

    def start(self):
        print("start")

test_case().start