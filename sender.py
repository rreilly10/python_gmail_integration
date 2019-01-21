import logging
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
    logging.info("Attempting to Send Message")
    conn.sendmail(sender, receivers, message)


if __name__ == "__main__":
    config = get_config()

    username = config.get("USERNAME")

    conn = get_conn(config.get("HOST"), config.get("PORT"))

    if not log_in(conn, username, config.get("PASSWORD")):
        exit()

    send_email(conn, username, [username], "This is a test")

    close_con(conn)
