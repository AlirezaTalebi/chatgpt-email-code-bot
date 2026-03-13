import imaplib
import config
from email.utils import parsedate_to_datetime
from pyrogram import Client, enums, filters
from pyrogram.types import Message


OPENAI_SENDERS = (
    "noreply@tm.openai.com",
    "noreply@email.openai.com",
    "noreply@tm1.openai.com",
    "otp@tm1.openai.com",
)


def check_email(username, password, imap_host, provider_name):
    """
    Check an email inbox using IMAP and return the latest ChatGPT code email subject.

    Args:
        username (str): Email username.
        password (str): Email app password.
        imap_host (str): IMAP server host.
        provider_name (str): Provider label for error messages.

    Returns:
        str: The latest code email subject.
    """
    imap_server = None

    try:
        imap_server = imaplib.IMAP4_SSL(imap_host)
        imap_server.login(username, password)
        imap_server.select("inbox")

        status, messages = imap_server.fetch("1:*", "(BODY[HEADER.FIELDS (SUBJECT FROM DATE)])")

        if status != "OK":
            return "No code found in recent emails."

        latest_code = None
        latest_date = None

        for msg in messages[::-1]:
            try:
                if len(msg) > 1:
                    email_header = msg[1].decode("utf-8", errors="ignore")
                    lines = email_header.splitlines()

                    from_line = next((line for line in lines if line.startswith("From:")), None)
                    subject_line = next((line for line in lines if line.startswith("Subject:")), None)
                    date_line = next((line for line in lines if line.startswith("Date:")), None)

                    sender = from_line.split(": ", 1)[1] if from_line else "Unknown Sender"
                    subject = subject_line.split(": ", 1)[1] if subject_line else "No Subject"
                    date_str = date_line.split(": ", 1)[1] if date_line else None

                    if date_str:
                        email_date = parsedate_to_datetime(date_str)

                        if any(email in sender for email in OPENAI_SENDERS):
                            if latest_date is None or email_date > latest_date:
                                latest_date = email_date
                                latest_code = subject

            except Exception as e:
                print("Error while processing email:", e)

        if latest_code:
            return latest_code

        return "No code found in recent emails."

    except Exception as e:
        raise Exception(f"Error while connecting to the {provider_name} email server.") from e
    finally:
        if imap_server is not None:
            try:
                imap_server.logout()
            except Exception:
                pass


def check_gmail(username, password):
    """
    Check Gmail using IMAP protocol.

    Args:
        username (str): Gmail email username.
        password (str): Gmail app password.

    Returns:
        str: The latest code from ChatGPT emails.
    """
    return check_email(username, password, "imap.gmail.com", "Gmail")


def check_yahoo_email(username, password):
    """
    Check Yahoo email using IMAP protocol.

    Args:
        username (str): Yahoo email username.
        password (str): Yahoo email password.

    Returns:
        str: The latest code from ChatGPT emails.
    """
    return check_email(username, password, "imap.mail.yahoo.com", "Yahoo")

# Call the function and print the result

app = Client(config.APP['session'], api_hash=config.APP['api_hash'], api_id=config.APP['api_id'], workdir=config.APP['workdir'])

@app.on_message(filters.command("code", prefixes=['']))
async def get_code(client, message:Message):
    if message.chat.id not in config.CHAT_IDS:
        return

    if config.MAIL == 'GMAIL':
        result = str(check_gmail(config.USERNAME, config.PASSWORD))
    elif config.MAIL == 'YAHOO':
        result = str(check_yahoo_email(config.USERNAME, config.PASSWORD))
    else:
        await message.reply("Invalid email provider specified in config.")
        return

    code = ''.join(filter(str.isdigit, result))

    if not code:
        await message.reply(result)
        return

    await message.reply(f' The Code is: \n\n`{code}`', parse_mode=enums.ParseMode.MARKDOWN)


app.run()
