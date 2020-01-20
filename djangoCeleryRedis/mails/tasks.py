import os
import logging
from datetime import datetime
from mails.models import Accounts, ExpiredAccounts
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = get_task_logger(__name__)

# for demonstration, all tasks run ince / minute

# using 1 minute as tesing periodic intervals
@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="retrieve_expired_accounts",
    ignore_result=True
)
def get_expired_accounts():
    """
    Save expired accounts to Expired Accounts Model
    """
    expired = Accounts.objects.filter(accountExpiryDate >= datetime.now()).values_list('accountEmail', flat=True)
    for accountEmail in expired:
        ExpiredAccounts.objects.update_or_create(accountEmail=accountEmail)

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="emails_expired_accounts",
    ignore_result=True
)
def sendEmails():
    """
    Send emails to expired accounts
    """

    try:
        expired = ExpiredAccounts.objects.values_list('accountEmail', flat=True)
        for accountEmail in expired:
            message = Mail(
                from_email='ouko.sherman@gmail.com',
                to_emails=accountEmail,
                subject='Account Expiry',
                html_content="Heeey sorry but your account has expired."
            )

            # sending email via send grid
            sg = SendGridAPIClient(account_sid = os.getenv('SENDGRID_KEY'))
            response = sg.send(message)
            
            # logging errors
            if(response.status_code == 202):
                ExpiredAccounts.objects.filter(accountEmail=accountEmail).delete()
            else:
                logging.basicConfig(filename='mails.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
                logging.error('Email unsuccesfully sent')
        
    except Exception as e:
        logging.basicConfig(filename='mails.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
        logging.error('Email unsuccesfully sent: ', str(e))

