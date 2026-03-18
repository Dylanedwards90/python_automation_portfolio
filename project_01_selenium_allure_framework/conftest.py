# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 20:31:16 2026

@author: Dylan
"""

import allure
import pytest
from utils.driver_factory import get_driver

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()
    
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot,
                          name = 'Failure Screenshot',
                          attachment_type = allure.attachment_type.PNG)