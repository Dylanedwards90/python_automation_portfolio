# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 07:49:26 2026

@author: Dylan
"""

import allure
from selenium.webdriver.common.by import By
from config.config import BASE_URL

class LoginPage:

    username_input = (By.ID, "username")
    password_input = (By.ID, "password")
    login_button = (By.CSS_SELECTOR, "button[type='submit']")
    
    def __init__(self, driver):
        self.driver = driver
      
    @allure.step("Open login page")
    def open(self):
        self.driver.get(BASE_URL)

    @allure.step("Enter Username")
    def enter_username(self, username):
        self.driver.find_element(*self.username_input).send_keys(username)
    
    @allure.step("Enter Password")
    def enter_password(self, password):
        self.driver.find_element(*self.password_input).send_keys(password)
    
    @allure.step("Click Login Page")
    def click_login(self):
        self.driver.find_element(*self.login_button).click()
        
    @allure.step("Login with username: {username}")
    def login(self, username, password):
        self.open()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()