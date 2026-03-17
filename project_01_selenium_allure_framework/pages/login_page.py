# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 07:49:26 2026

@author: Dylan
"""

from selenium.webdriver.common.by import By

class LoginPage:

    username_input = (By.ID, "username")
    password_input = (By.ID, "password")
    login_button = (By.CSS_SELECTOR, "button[type='submit']")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("https://the-internet.herokuapp.com/login")

    def enter_username(self, username):
        self.driver.find_element(*self.username_input).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()