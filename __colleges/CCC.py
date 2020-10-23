from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import random
import Student


prefix = ['855', '561', '800', '325', '330', '229']


def random_phone_num_generator():
    first = str(random.choice(prefix))
    second = str(random.randint(1, 888)).zfill(3)
    last = (str(random.randint(1, 9998)).zfill(4))
    while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
        last = (str(random.randint(1, 9998)).zfill(4))
    return f'({first}) {second}-{last}'


def apply(driver, student):
    url = Student.allColleges.get(student.college).get('url')

    driver.get(url)

    driver.find_element_by_xpath('//*[@id="portletContent_u16l1n18"]/div/div[2]/div/a[2]').click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "accountFormSubmit"))
    ).click()

    print('Account Progress - 1/3', end='')

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "inputFirstName"))
    ).send_keys(student.firstName)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "inputMiddleName"))
    ).send_keys(student.middleName)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "inputLastName"))
    ).send_keys(student.lastName)

    driver.find_element_by_xpath('//*[@id="hasOtherNameNo"]').click()

    driver.find_element_by_xpath('//*[@id="hasPreferredNameNo"]').click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputBirthDateMonth option[value="' + str(student.birthdayMonth) + '"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputBirthDateDay option[value="' + str(student.birthdayDay) + '"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputBirthDateYear'))
    ).send_keys(student.birthdayYear)

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputBirthDateMonthConfirm option[value="' + str(student.birthdayMonth) + '"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputBirthDateDayConfirm option[value="' + str(student.birthdayDay) + '"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputBirthDateYearConfirm'))
    ).send_keys(student.birthdayYear)

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, '-have-ssn-yes'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.NAME, 'ssn'))
    ).send_keys(student.ssn)

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.NAME, 'ssnConfirm'))
    ).send_keys(student.ssn)

    element = driver.find_element_by_id('accountFormSubmit')
    desired_y = (element.size['height'] / 2) + element.location['y']
    window_h = driver.execute_script('return window.innerHeight')
    window_y = driver.execute_script('return window.pageYOffset')
    current_y = (window_h / 2) + window_y
    scroll_y_by = desired_y - current_y

    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

    element.click()

    print(' (Success)')

    print('Account Progress - 2/3', end='')

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputEmail'))
    ).send_keys(student.email)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputEmailConfirm'))
    ).send_keys(student.email)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputSmsPhone'))
    ).send_keys(student.phone)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputStreetAddress1'))
    ).send_keys(student.streetAddress)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputCity'))
    ).send_keys(student.cityAddress)

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputState option[value="' + student.stateAddress + '"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputPostalCode'))
    ).send_keys(student.postalCode)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'accountFormSubmit'))
    ).click()

    try:
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="messageFooterLabel"]').click()

        while True:
            check_input_phone = driver.find_element_by_id('inputSmsPhone')
            check_error = check_input_phone.get_attribute('class')
            if check_error == 'portlet-form-input-field error':
                print('Invalid Number, Retrying....')
                check_input_phone.clear()
                student.phone = random_phone_num_generator()
                check_input_phone.send_keys(student.phone)
                time.sleep(0.4)
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, 'inputAlternatePhone_auth_txt'))
                ).click()

                try:
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="messageFooterLabel"]'))
                    ).click()
                except Exception as e:
                    print(e)
                    break
                continue
            else:
                break

    except Exception as e:
        print(e)

    time.sleep(1)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'accountFormSubmit'))
    ).click()

    try:
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'messageFooterLabel'))
        ).click()

        time.sleep(0.7)

        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, 'inputAddressValidationOverride'))
        ).click()

        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'accountFormSubmit'))
        ).click()

    except Exception as e:
        print(e)
        pass

    print(' (Success)\nAccount Progress - 3/3')

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputUserId'))
    ).send_keys(student.username)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputPasswd'))
    ).send_keys(student.password)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputPasswdConfirm'))
    ).send_keys(student.password)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputPin'))
    ).send_keys(student.pin)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputPinConfirm'))
    ).send_keys(student.pin)

    #
    # Question 1
    #

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputSecurityQuestion1 option[value="5"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputSecurityAnswer1'))
    ).send_keys("John")

    #
    # Question 2
    #

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputSecurityQuestion2 option[value="6"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputSecurityAnswer2'))
    ).send_keys(student.lastName)

    #
    # Question 3
    #

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputSecurityQuestion3 option[value="7"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'inputSecurityAnswer3'))
    ).send_keys("Doe")

    Student.save_student(student)

    print('Please fill the captcha and click Create My Account')

    wait = 180
    while True:
        mins, secs = divmod(wait, 60)
        timeformat = '\rWaiting {:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='')
        try:
            driver.find_element_by_xpath("//*[contains(text(),'Account Created')]")
            print('\rCaptcha Solved!')
            break
        except NoSuchElementException:
            if wait == 0:
                print('\nCaptcha not solved. Exiting')
                return
            time.sleep(1)
            wait -= 1
            continue

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="registrationSuccess"]/main/div[2]/div/div/button'))
    ).click()

    print('Details Progress - 1/8', end='')

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.NAME, 'application.termId'))
    )

    dropdown_menu = Select(driver.find_element_by_name('application.termId'))
    dropdown_menu.select_by_index(2)

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputEduGoal option[value="B"]'))
    ).click()

    dropdown_menu = Select(driver.find_element_by_id('inputMajorId'))
    dropdown_menu.select_by_index(random.randint(1, 7))

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.NAME, '_eventId_continue'))
    ).click()

    print(' (Success)')

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputAddressSame'))
    ).click()

    time.sleep(0.7)

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="column2"]/div[6]/ol/li[2]/button'))
    ).click()

    # Page 2

    dropdown_menu = Select(driver.find_element_by_name('appEducation.enrollmentStatus'))
    dropdown_menu.select_by_index(1)

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputHsEduLevel option[value="4"]'))
    ).click()

    pass_year = [3, 4]

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputHsCompMM option[value="' + str(random.choice(pass_year)) + '"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputHsCompDD option[value="' + str(student.eduDay) + '"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputHsCompYYYY'))
    ).send_keys(student.eduYear)

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputCaHsGradYes'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputCaHs3yearNo'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputHsAttendance1'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#hs-input-sf-state option[value="' + student.stateAddress + '"]'))
    ).click()

    search = driver.find_element_by_id('hs-school-name')
    search.clear()
    search.send_keys('high')
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'hs-suggestions'))
    )
    time.sleep(1)

    parent = driver.find_element_by_class_name('autocomplete-menu')
    it = parent.find_elements_by_tag_name("li")

    if len(it) < 5:
        print('Changing State....')
        Select(driver.find_element_by_id('hs-input-sf-state')).select_by_value('CA')

        search.clear()
        search.send_keys('high', Keys.ENTER)
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, 'hs-suggestions'))
        )
        time.sleep(1)

        parent = driver.find_element_by_class_name('autocomplete-menu')
        it = parent.find_elements_by_tag_name("li")
        if len(it) > 5:
            print('State Changed, Resuming')

    try:
        time.sleep(1)
        it[random.randint(4, 8)].click()
    except Exception as e:
        print(str(e), 'can\'t click')

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputGPA'))
    ).send_keys(Keys.BACKSPACE, '400')

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputHighestEnglishCourse option[value="4"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputHighestEnglishGrade option[value="A"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputHighestMathCourseTaken option[value="7"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputHighestMathTakenGrade option[value="A"]'))
    ).click()

    time.sleep(0.7)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="column2"]/div[14]/ol/li[2]/button'))
    ).click()

    print('Details Progress - 2/8 (Success)')

    print('Details Progress - 3/8', end='')

    # Military

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputCitizenshipStatus option[value="1"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputMilitaryStatus option[value="1"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="column2"]/div[6]/ol/li[2]/button'))
    ).click()

    print(' (Success)')

    print('Details Progress - 4/8', end='')

    # Residency

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputCaRes2YearsYes'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputHomelessYouthNo'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputIsEverInFosterCareNo'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="column2"]/div[7]/ol/li[2]/button'))
    ).click()

    # driver.find_element_by_xpath('//*[@id="column2"]/div[7]/ol/li[2]/button').click()

    print(' (Success)')

    print('Details Progress - 5/8', end='')

    # Intersts

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputEnglishYes'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputFinAidInfoNo'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputAssistanceNo'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputAthleticInterest1'))
    ).click()

    element = driver.find_elements_by_class_name('ccc-form-layout')[5]
    desired_y = (element.size['height'] / 2) + element.location['y']
    window_h = driver.execute_script('return window.innerHeight')
    window_y = driver.execute_script('return window.pageYOffset')
    current_y = (window_h / 2) + window_y
    scroll_y_by = desired_y - current_y

    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

    allElements = element.find_elements_by_tag_name('li')

    rndList = [2, 1, 2, 2]

    occurance = 0
    inputChecked = False

    while occurance < 2:
        for elementxx in allElements:
            myRandom = random.choice(rndList)
            xx = elementxx.find_element_by_class_name('portlet-form-input-checkbox')
            if xx.get_attribute('id') == 'inputOnlineClasses' and inputChecked == False:
                myRandom = 1
                inputChecked = True
            if myRandom == 1:
                occurance += 1
                element = xx
                desired_y = (element.size['height'] / 2) + element.location['y']
                window_h = driver.execute_script('return window.innerHeight')
                window_y = driver.execute_script('return window.pageYOffset')
                current_y = (window_h / 2) + window_y
                scroll_y_by = desired_y - current_y

                driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
                xx.click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="column2"]/div[9]/ol/li[2]/button'))
    ).click()

    # driver.find_element_by_xpath('//*[@id="column2"]/div[9]/ol/li[2]/button').click()

    print(' (Success)')

    print('Details Progress - 6/8', end='')

    # Demographic

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputGender option[value="Male"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputTransgender option[value="No"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputOrientation option[value="StraightHetrosexual"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputParentGuardianEdu1 option[value="6"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#inputParentGuardianEdu2 option[value="2"]'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputHispanicNo'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputRaceEthnicity800'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputRaceEthnicity' + str(random.randint(801, 809))))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="column2"]/div[7]/ol/li[2]/button'))
    ).click()

    # driver.find_element_by_xpath('//*[@id="column2"]/div[7]/ol/li[2]/button').click()

    print(' (Success)')

    print('Details Progress - 7/8', end='')

    # Supplemental

    if student.college == 'Mendocino College':
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, 'YESNO_1_yes'))
        ).click()

        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, 'YESNO_2_no'))
        ).click()

        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, 'YESNO_3_no'))
        ).click()

        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, 'YESNO_4_no'))
        ).click()

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, '_supp_TEXT_1'))
        ).send_keys("NONE")

        driver.find_element_by_name("_eventId_continue").click()

    elif student.college == 'Antelope Valley':

        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#_supp_MENU_1 option[value="B"]'))
        ).click()

        driver.find_element_by_name("_eventId_continue").click()

    print(' (Success)')

    print('Details Progress - 8/8', end='')

    # Submission

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputConsentYes'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputESignature'))
    ).click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'inputFinancialAidAck'))
    ).click()

    print(' (Success)')

    element = driver.find_element_by_xpath('//*[@id="submit-application-button"]')
    desired_y = (element.size['height'] / 2) + element.location['y']
    window_h = driver.execute_script('return window.innerHeight')
    window_y = driver.execute_script('return window.pageYOffset')
    current_y = (window_h / 2) + window_y
    scroll_y_by = desired_y - current_y

    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

    # driver.find_element_by_xpath('//*[@id="submit-application-button"]').click()
    element.click()

    print('Complete!\nRun check_email.py in a day or two')
