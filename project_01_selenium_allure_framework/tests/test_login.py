# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 07:54:23 2026

@author: Dylan
"""

import pytest 
from pages.login_page import LoginPage
from utils.driver_factory import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_valid_login(driver):

    login = LoginPage(driver)

    login.open()
    login.enter_username("tomsmith")
    login.enter_password("SuperSecretPassword!")
    login.click_login()
    
    # WAIT for the success message to appear
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )


    assert "secure" in driver.current_url