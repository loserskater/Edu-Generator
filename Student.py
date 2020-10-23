from types import SimpleNamespace
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import time
import json


allColleges = {
    'Mendocino College': {
        'url': 'https://www.opencccapply.net/gateway/apply?cccMisCode=141',
        'state': 'CA'
    },
    'Contra Costa College': {
        'url': 'https://www.opencccapply.net/gateway/apply?cccMisCode=311',
        'state': 'CA'
    },
    'Grossmont College': {
        'url': 'https://www.opencccapply.net/gateway/apply?cccMisCode=022',
        'state': 'CA'
    },
    'Antelope Valley College': {
        'url': 'https://www.opencccapply.net/gateway/apply?cccMisCode=621',
        'state': 'CA'
    },
    'Southwestern College': {
        'url': 'https://www.opencccapply.net/gateway/apply?cccMisCode=091',
        'state': 'CA'
    },
    'Westmoreland College': {
        'url': 'https://apply.westmoreland.edu/Datatel.ERecruiting.Web.External/Pages/createaccount.aspx',
        'state': 'PA'
    }
}


class Student:

    email = ''
    college = ''
    firstName = ''
    middleName = ''
    lastName = ''
    streetAddress = ''
    cityAddress = ''
    stateAddress = ''
    postalCode = ''
    phone = ''
    ssn = ''
    username = ''
    password = ''
    pin = ''
    birthdayMonth = ''
    birthdayDay = ''
    birthdayYear = ''
    eduMonth = ''
    eduDay = ''
    eduYear = ''


def suffix(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


def build_student(driver, college):
    student = Student()
    student.college = college
    student.stateAddress = allColleges.get(college).get('state')
    random.seed()
    letters = string.ascii_uppercase
    student.middleName = random.choice(letters)

    driver.get('https://names.igopaygo.com/people/fake-person')

    print('Getting random student info', end='')

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//select[@name='gender']/option[@value='M']"))
    ).click()

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//select[@name='country']/option[@value='" + student.stateAddress + "']"))
    ).click()

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//select[@name='real_cities']/option[@value='1']"))
    ).click()

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.ID, 'create'))
    ).click()

    time.sleep(1)

    name = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='given-name']"))
    ).text

    student.firstName = name.split()[1]
    student.lastName = name.split()[2]

    student.streetAddress = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='street-address']"))
    ).text

    student.cityAddress = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='locality']"))
    ).text

    student.postalCode = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='postal-code']"))
    ).text.split()[0]

    student.phone = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[text()='Phone:']/following-sibling::div/span/a"))
    ).text

    student.ssn = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[text()='SSN:']/following-sibling::div/a"))
    ).text

    student.username = student.firstName + str(suffix(7))
    student.password = student.lastName + str(suffix(5))
    student.pin = str(suffix(4))

    student.birthdayMonth = str(random.randint(1, 12))
    student.birthdayDay = str(random.randint(1, 27))
    student.birthdayYear = str(random.randint(1996, 1999))
    student.eduMonth = str(random.randint(1, 12))
    student.eduDay = str(random.randint(1, 27))
    student.eduYear = str(random.randint(2019, 2020))

    print(' (Complete)\nGetting email', end='')

    driver.get('https://generator.email/email-generator')

    domain = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "email_ch_text"))
    ).text.split('@')[1]

    student.email = str.lower(student.firstName + student.lastName) + '@' + domain

    print(' (Complete)')

    return student


def save_student(student):
    with open('myccAcc.txt', 'a') as f:
        f.write(json.dumps(vars(student)) + '\n')


def get_student_from_file():
    student_list = []
    index = 1
    with open('myccAcc.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        student = json.loads(line, object_hook=lambda d: SimpleNamespace(**d))
        if student.college == 'Westmoreland College':
            student.index = index
            student_list.append(student)
            index += 1

    print('\nSelect a student:')
    for student in student_list:
        print(str(student.index) + ' - ' + student.email)

    while True:
        data = int(input())
        if data > len(student_list) or data < 1:
            print("Invalid response, try again.")
            continue
        else:
            break

    for student in student_list:
        if student.index == data:
            return student

    return None
