import os
import logging
from sms.models import ScheduledDispatch
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from twilio.rest import Client

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="dispatched_sms",
    ignore_result=True
)
def sendSms():
    """
    Send sms for dispatched goods
    """
    smses = ScheduledDispatch.objects.values('dispatchItem', 'dispatchRecipient', 'dispatchID')

    for sms in smses:
        try:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            twilio_number = os.getenv('TWILIO_NUMBER')
            client = Client(account_sid, auth_token)

            client.messages \
                .create(
                body='Your item '+sms['dispatchItem']+ ' Has been dispatched',
                from_= twilio_number,
                to='+254'+str(sms['dispatchRecipient']),
            )
        
            ScheduledDispatch.objects.filter(dispatchID=sms['dispatchID']).delete()
        except Exception as e:
            logging.basicConfig(filename='sms.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
            logging.error('Email unsuccesfully sent: ', str(e))
            logger.info(sms['dispatchItem'])
        

        