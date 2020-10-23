import time
from selenium import webdriver
import Student
from __colleges import CCC, WCC


def start_bot():
    with open('prefBrowser.txt', 'r') as fp:
        browser = fp.read()

    try:
        # For Chrome
        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument("user-data-dir=./selenium")
            driver = webdriver.Chrome(options=options, executable_path=r'./webdriver/chromedriver')
        # For Firefox
        elif browser == 'firefox':
            # cap = DesiredCapabilities().FIREFOX
            # cap['marionette'] = True
            driver = webdriver.Firefox(executable_path=r'./webdriver/geckodriver')
        elif browser == '':
            print('Error - Run setup.py first')
            exit()
    except Exception as e:
        time.sleep(0.4)
        print('\nError - ' + str(e))
        return
    
    driver.maximize_window()
    driver.delete_all_cookies()
    return driver


def new_application(college):
    driver = start_bot()
    student = Student.build_student(driver, college)

    url = Student.allColleges.get(student.college).get('url')

    if 'opencccapply' in url:
        CCC.apply(driver, student)
    elif 'westmoreland' in url:
        WCC.apply(driver, student)


def continue_application(college):
    student: Student.Student

    student = Student.get_student_from_file()

    if student is None:
        print('Something bad happened, try again')
        return

    print('Applying as ' + student.firstName + ' ' + student.lastName)

    driver = start_bot()
    WCC.continue_app(driver, student)


def main():
    print('\nKeep an eye on this console!')
    time.sleep(2)
    print('Select a college:')

    colleges = list(Student.allColleges.keys())
    for index, college in enumerate(colleges):
        print(str(index + 1) + ' - ' + college)

    while True:
        data = int(input())
        if data > len(Student.allColleges) or data < 1:
            print("Invalid response, try again.")
            continue
        else:
            break

    college = colleges[data - 1]

    print('\nSelected College: ' + college)

    if college == 'Westmoreland College':
        print('1 - New Application\n2 - Check email and continue application')

        while True:
            data = int(input())
            if data not in (1, 2):
                print("Invalid response, try again.")
                continue
            else:
                break

        if data == 2:
            continue_application(college)
            return

    new_application(college)


if __name__ == '__main__':
    main()
