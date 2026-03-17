# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 07:54:24 2026

@author: Dylan
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def get_driver():

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    return driver