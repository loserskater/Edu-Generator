import webbrowser
from time import sleep

emails = ["Check All"]


def get_emails():
    with open('students.txt', 'r') as f:
        accounts = f.readlines()

    for line in accounts:
        emails.append(line.split('"email": "')[1].split('"')[0])


def main():
    get_emails()

    print("Select an email to check:")

    for index, email in enumerate(emails):
        print(str(index) + ' - ' + email)

    while True:
        data = int(input())
        if data > len(emails) or data < 0:
            print("Invalid response, try again.")
            continue
        else:
            break
    if data == 0:
        emails.pop(0)
        webbrowser.open('https://generator.email/')
        sleep(10)
        for email in emails:
            webbrowser.open('https://generator.email/'+email, new=2)
            sleep(5)
    else:
        webbrowser.open('https://generator.email/' + emails[data])


if __name__ == '__main__':
    main()
