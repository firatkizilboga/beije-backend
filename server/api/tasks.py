from datetime import datetime
from django.utils import timezone

#celery logger
from celery.utils.log import get_task_logger
from celery import shared_task

from .models import Subscription


@shared_task
def check_and_fulfuill():
    """
    Check if any subscription is due for fulfillment and fulfill it
    """
    logger = get_task_logger(__name__)
    logger.info("Checking for subscriptions to fulfill")
    subscriptions = Subscription.objects.filter(next_fulfillment_date__lte=timezone.now(), is_active=True)
    for subscription in subscriptions:
        subscription.fulfill()
    

    

        
    