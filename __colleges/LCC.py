from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import Student


def apply(driver, student):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login_id"))
    ).send_keys(student.username)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pin_id"))
    ).send_keys(student.pin)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "verify_pin_id"))
    ).send_keys(student.pin)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "id____UID0"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "app_type_id"))
    )

    Select(driver.find_element_by_id('app_type_id')).select_by_index(1)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "id____UID0"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "term_id"))
    )

    Select(driver.find_element_by_id('term_id')).select_by_index(2)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "first_id"))
    ).send_keys(student.firstName)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "last_id"))
    ).send_keys(student.lastName)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "id____UID0"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Street Address and Phone"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "addr1_id"))
    ).send_keys(student.streetAddress)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "city_id"))
    ).send_keys(student.cityAddress)

    Select(driver.find_element_by_id('stat_id')).select_by_value(student.stateAddress)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "area_id"))
    ).send_keys(student.phone.split('-')[0])

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "phone_id"))
    ).send_keys(student.phone.split('-')[1:])

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ud1_yes_id"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ud2_no_id"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "id____UID0"))
    ).click()
