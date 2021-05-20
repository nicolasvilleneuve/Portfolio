from flask import Flask, render_template, url_for, request, redirect
import os
import csv
import smtplib

igor_email = "THISEMAILACCOUNTISNTREAL@gmail.com"
igor_password = "THISPASSWORDISNTREAL"
my_email = 'THISEMAILISNTREAL@gmail.com'

app = Flask(__name__)
print(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        full_name = data['full_name']
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{full_name}, {email}, {subject}, {message}')

def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as real_database:
        full_name = data['full_name']
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(real_database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([full_name,email,subject,message])

        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(igor_email, igor_password)
            connection.sendmail(from_addr=igor_email, to_addrs=my_email, msg=f"Subject: Someone Contacted You Through Your Website "
                                                                       f"\n\n Their name is {full_name}, "
                                                                                    f"email is: {email},"
                                                                                    f"subject is:{subject}"
                                                                                    f"and message is: {message}")

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
   if request.method == 'POST':
       try:
           data = request.form.to_dict()
           write_to_file(data)
           write_to_csv(data)
           return redirect('/thankyou.html')
       except:
           return 'did not save to database'
   else:
       return 'Something went wrong, please try again'
