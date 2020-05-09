###
#
# GMC exam slot finder.
# @author: Saad Zaher <eng.szaher[at]gmail.com>
#
#
###
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import sys
import argparse


def get_rows(table):
    rows = []
    trs = table.find_all("tr")
    for tr in trs:
        row = []
        for td in tr:
            row.append(td.text)
        rows.append(row)
    return rows


def send_email(args, data):
    mail_content = ''' As per your request free slot found.'''
    if isinstance(data, list):
        for row in data:
            mail_content += '''on {} in {}.'''.format(row[4], row[3])

    mail_content += '''Please take an action and book it now! \n \n \n 7obiiiii'''

    # The mail addresses and password
    sender_address = args.email
    sender_pass = args.email_password
    receiver_address = args.email
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Plab1: Exam slot found!'  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


def check_right_table(table):
    tr = table.find("tr")
    return tr.has_attr("class")


def setup_args(args=[]):
    parser = argparse.ArgumentParser("GMC")
    parser.add_argument("-u", "--username", help="GMC Username")
    parser.add_argument("-p", "--password", help="GMC Password")
    parser.add_argument("-c", "--count", default=3, type=int, help="Hpw long should we retry. Default is 3 retrials.")
    parser.add_argument("-w", "--wait", default=300, help="How many seconds to wait between retrials. Default is 300.")
    parser.add_argument("--email", required=True, help="Email address to notify in case we found a match. "
                                                       "Only gmail is supported.")
    parser.add_argument("--email-password", required=True, help="Email address to notify in case we found a match.")
    parser.add_argument("--country", default="Egypt", help="Country of exam.")
    parser.add_argument("--month", required=True, help="Month of exam")

    if len(args) < 1:
        parser.print_usage()
        parser.print_help()
        sys.exit(1)
    return parser.parse_args(args=args)


def login(driver, args):
    driver.get("https://webcache.gmc-uk.org/ecustomer_enu/index.aspx")
    delay = 3  # seconds

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'submitLogin')))
        print("Page is ready!")
        time.sleep(5)
    except TimeoutException:
        time.sleep(5)
        print("Loading took too much time!")
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    login = driver.find_element_by_id("submitLogin")

    username.send_keys(args.username)
    password.send_keys(args.password)
    login.submit()
    time.sleep(10)


def get_booking_source_after_login(driver):
    client_id = "_sweclient"
    driver.switch_to.frame(client_id)

    driver.switch_to.frame("_sweview")

    link = driver.find_element_by_link_text("My Tests")
    link.click()

    time.sleep(5)

    book = driver.find_element_by_link_text("Test Bookings")
    book.click()
    time.sleep(5)

    btest = driver.find_element_by_link_text("Book Test")
    btest.click()
    time.sleep(5)
    check = driver.find_element_by_id("s_30_cb")
    check.click()

    contine = driver.find_element_by_link_text("Continue with Booking")
    contine.click()
    time.sleep(3)
    return driver.page_source


def refresh(driver):
    driver.refresh()
    return driver.page_source


def parse_source(args, source):
    soup = BeautifulSoup(source, "html.parser")
    form = soup.find(name="form", attrs={"name": "SWEForm4_0"})
    tables = form.find_all(name="table")
    for table in tables:
        if check_right_table(table):
            break
    rows = get_rows(table)
    # print(json.dumps(rows, sort_keys=True, indent=4))
    return check_results_for_country(rows=rows, country=args.country, month=args.month)


def main():
    args = setup_args(sys.argv[1:])
    if not args.username:
        args.username = getpass.getuser()
    if not args.password:
        args.password = getpass.getpass()
    driver = webdriver.Firefox(executable_path="./geckodriver")
    try:
        login(driver, args)
        source = get_booking_source_after_login(driver=driver)
        count = args.count
        loop_stop = args.wait / 60
        while count > 0:
            refresh(driver)
            rows = parse_source(args, source)
            if rows:
                send_email(args=args, data=rows)
            i = 0
            while i < 60:
                print('.', end='')
                time.sleep(loop_stop)
                i += 1
            count -= 1
    finally:
        driver.close()


def check_results_for_country(rows, country="Egypt", month="06"):
    matches = []
    for row in rows:
        if country in row:
            date: str = row[1]
            if date.find(month) != -1:
                matches.append(row)
                # send_email(when=date, where="{}/{}".format(row[4], row[3]))
                print("MONTH FOUND.... BOOK NOW!!!!")
    return matches


if __name__ == "__main__":
    main()
