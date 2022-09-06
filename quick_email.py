# Send Email with Python 

from absl import app
from absl import flags
from dotenv import load_dotenv
from yagmail import SMTP
import os

load_dotenv()

FLAGS = flags.FLAGS
flags.DEFINE_string('reciever', os.getenv('DEFAULT_EMAIL'), 'Email to send email to')
flags.DEFINE_string('subject', 'Testing subject', 'Subject of the email')
flags.DEFINE_string('body', 'Testing body', 'Body of the email')
flags.DEFINE_list('attachments', [], 'Comma-separated list of real files to attach to email')

class EmailProvider:

    def __init__(self, user, pw):
        self.user = user
        self.pw = pw

    def Email(self, reciever, subject, body):
        mail = SMTP(user=self.user, password=self.pw)
        mail.send(reciever, subject = subject, contents = body)
        mail.close()
        print("Email Sent")

    def Email_With_Attachment(self, reciever, subject, body, attachment):
        mail = SMTP(user=self.user, password=self.pw)
        mail.send(reciever, subject = subject, contents = body, attachments = attachment)
        print("Email Sent")

def main(argv):
    email_provider = EmailProvider(os.getenv('GMAIL_USER'), os.getenv('GMAIL_PASS'))
    if len(FLAGS.attachments) == 0:
        email_provider.Email(FLAGS.reciever, FLAGS.subject, FLAGS.body)
    else:
        email_provider.Email_With_Attachment(FLAGS.reciever, FLAGS.subject, FLAGS.body, FLAGS.attachments)

if __name__ == "__main__":
    app.run(main)
    