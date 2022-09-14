import sqlite3
from random import choices
from string import ascii_letters, digits
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime as dt
import time
from zoneinfo import available_timezones

name = input("Enter your name:  ")
email = input("Enter the Email: ")
duration = input("Enter your duration(in  minutes: )  ")
conn = sqlite3.connect('test.sqlite3')

cursor = conn.cursor()

cursor.execute(
    """
            create table if not exists userdatabase(
                id integer primary key autoincrement,
                name varchar(20),
                email varchar(30),
                duration integer
            )

        """
)


def check_available(email):

    avail = cursor.execute(
        """
            select email from userdatabase
            where email = ?
        """, [email]
    ).fetchall()
    if avail == []:
        return True
    else:
        return False


def get_duration(email):
    duration = cursor.execute(
        """
    select duration from userdatabase 
        where email=? """, [email]).fetchall()

    return duration


def generate_password(k=15):
    chars = ascii_letters + digits
    return ''.join(choices(chars, k=k))


def add_user(name, email, duration):
    cursor.execute(
        """
        insert into userdatabase 
            (name,email,duration)
            values(?,?,?)
        
        """, [name, email, duration])


def send_password(email, password):
    from_ = '[Email]'
    to = email
    msg = MIMEMultipart()
    msg['From'] = from_
    msg['To'] = to
    msg['Subject'] = 'Reminder!!! To Change Password'
    pwd = '[app generated password]'
    text = f"""
            Your Password is Getting Old 
            Please Update your password now 

            your New Password is {password}
    """
    text_mime = MIMEText(text, 'plain')
    msg.attach(text_mime)

    print("[+] Connecting to server...")
    conn = smtplib.SMTP("smtp.gmail.com", 587)
    print("[+] Making Connection Secure...")
    conn.starttls()
    print("[+] Logging to the Server...")
    conn.login(from_, pwd)
    print("[+] Sending Password...")
    conn.sendmail(from_, to, msg.as_string())
    print('[+] Closing the Connection...')


def covert_list_integer(duration):
    tup = duration[0]
    real = tup[0]
    return int(real)


def send_after_duration(duration):

    sec = duration*60

    t = sec
    while t:
        time.sleep(1)
        t -= 1

    return False


if check_available(email):
    print("This Email is Available for Use ")
else:
    print("This email is in database ")
    while not check_available(email):
        email = input("Enter Diffrent Email: ")

print("[+] Adding User....")
add_user(name, email, duration)
min = covert_list_integer(get_duration(email))
print("[+] Waiting For Duration to Complete....")
while send_after_duration(min):
    pass
print("[+] Generating Password....")
new_password = generate_password()
send_password(email, new_password)
print("[+] Sucessfully Reminded....")

conn.commit()
conn.close()
