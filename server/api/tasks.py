
from datetime import datetime
from django.utils import timezone

from .models import Subscription
#celery logger
from celery.utils.log import get_task_logger
from celery import shared_task

@shared_task
def check_and_fulfuill():
    logger = get_task_logger(__name__)
    subscriptions = Subscription.objects.filter(next_fulfillment_date__lte=timezone.now(), is_active=True)
    for subscription in subscriptions:
        subscription.fulfill()
    

    

        
    