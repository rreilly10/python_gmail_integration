import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPAuthenticationError, SMTPException

import yaml

root = logging.getLogger()
root.setLevel(logging.DEBUG)


def get_config():
    with open("config.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exception:
            print(exception)
            return None


def get_conn(host, port):
    email_conn = SMTP(host, port)
    email_conn.ehlo()

    return email_conn


def close_con(conn):
    conn.quit()


def log_in(conn, username, password):
    try:
        conn.starttls()
        conn.login(username, password)
        logging.info("Log in Successful!")
        return True
    except SMTPAuthenticationError:
        logging.info("Unable to log-in")
        return False


def send_email(conn, sender, receivers, message):
    try:
        logging.info("Attempting to Send Message")
        conn.sendmail(sender, receivers, message)
    except SMTPAuthenticationError as exception:
        logging.info('Unable to Send Message: %s', exception)


if __name__ == "__main__":
    config = get_config()

    username = config.get("USERNAME")

    conn = get_conn(config.get("HOST"), config.get("PORT"))

    if not log_in(conn, username, config.get("PASSWORD")):
        exit()

    msg = MIMEMultipart("alternative")
    msg['Subject'] = "Hello"
    msg['From'] = username
    # msg['To'] = [username]

    plain_text = "This is a test"
    html_text = \
        """
        <html>
            <head></head>
            <body>
                <p>
                    Hey! <br>
                    Testing email <b>message</b>
                </p>
            </body>
        </html>
        """

    part1 = MIMEText(plain_text, 'plain')
    part2 = MIMEText(html_text, 'html')
    msg.attach(part1)
    msg.attach(part2)

    send_email(conn, username, [username], msg.as_string())

    close_con(conn)
