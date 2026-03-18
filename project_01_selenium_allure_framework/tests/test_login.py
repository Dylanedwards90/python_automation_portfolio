# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 07:54:23 2026

@author: Dylan
"""
import allure
from pages.login_page import LoginPage
from config.config import VALID_USERNAME, VALID_PASSWORD
from selenium.webdriver.common.by import By


@allure.title("Valid Login Test")
@allure.description("Verify that a user can log in with valid credentials")
def test_valid_login(driver):

    login = LoginPage(driver)

    login.login(VALID_USERNAME, VALID_PASSWORD)

    
    message = driver.find_element(By.ID, "flash").text

    assert "You logged into a secure area!" in message
    
@allure.title("Invalid Login Test")
@allure.description("Verify login fails with invalid credentials")
def test_invalid_login(driver):

    login = LoginPage(driver)

    login.login("wrong_user","wrong_password")

    message = driver.find_element(By.ID, "flash").text

    assert "Your username is invalid!" in message
    
@allure.title("Empty Login Test")
@allure.description("Verify login fails with no credentials entered")
def test_empty_login(driver):

    login = LoginPage(driver)

    login.login("","")
    
    message = driver.find_element(By.ID, "flash").text

    assert "Your username is invalid!" in message
    
