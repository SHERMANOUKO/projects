import os
import logging
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/15')),
    name="task_save_latest_flickr_image",
    ignore_result=True
)
def task_save_latest_flickr_image():
    """
    Saves latest image from Flickr
    """
    message = Mail(
        from_email='ouko.sherman@gmail.com',
        to_emails='fibonaccilimited@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>'
    )
    try:
        sg = SendGridAPIClient("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")
        # print("here")
        response = sg.send(message)
        # print("then here")
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
        logger.info("Success")
        logger.info(response.status_code)
    except Exception as e:
        # print(e)
        logger.info("failed")
    
   



