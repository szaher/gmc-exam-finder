GMC Exam Slot Finder
====================

This script will help doctors who would like to book an exam slot with [GMC](https://webcache.gmc-uk.org/ecustomer_enu/index.aspx) to keep monitoring the available bookings till they find a slot in the required country on the required date(month).


###. Prerequisites
* Download Selenium driver from [Here](https://github.com/mozilla/geckodriver/releases) 
    * Download the one valid for your operating system
    * Extract it
    * make sure to name it `geckodriver` and place it next to the python script
* Python 3.6 or later
* Gmail app password from [Here](https://myaccount.google.com/apppasswords)
    * You can follow instructions available [Here](https://support.google.com/accounts/answer/185833?hl=en)
    * This is required to send emails in case the script found a match.

###. Installation
* Make sure you have downloaded Selenium driver 
* Place the selenium driver next to lucinda.py script
* Rename to selenium driver to `geckodriver`
* Install requirements
    ```shell script
    pip install -r requirements.txt
    ```
* Run lucinda.py
    ```shell script
    python lucinda.py -h
    usage: GMC [-h] [-u USERNAME] [-p PASSWORD] [-c COUNT] [-w WAIT] --email EMAIL
               --email-password EMAIL_PASSWORD [--country COUNTRY] --month MONTH
    
    optional arguments:
      -h, --help            show this help message and exit
      -u USERNAME, --username USERNAME
                            GMC Username
      -p PASSWORD, --password PASSWORD
                            GMC Password
      -c COUNT, --count COUNT
                            Hpw long should we retry. Default is 3 retrials.
      -w WAIT, --wait WAIT  How many seconds to wait between retrials. Default is
                            300.
      --email EMAIL         Email address to notify in case we found a match. Only
                            gmail is supported.
      --email-password EMAIL_PASSWORD
                            Email address to notify in case we found a match.
      --country COUNTRY     Country of exam.
      --month MONTH         Month of exam
    ```
  
###. How it works
The program runs with your GMC username & password and keeps refreshing the website till it finds a match or your count is finished.
If it found a match it will send an email to your provided email to notify you.

####. Run it

* Execute the following command
    ```shell script
    python lucinda.py --username GMC_USERNAME --password GMC_PASSWORD --count 10000000 --email dremail@gmail.com -- email-password GMAIL_APP_PASSWORD --country EGYPT --month 6 
    ```

Thank You!
========== 
