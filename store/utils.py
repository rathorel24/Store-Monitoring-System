from main.models import Store, StoreStatusLog, StoreStatus
from django.utils import timezone 
from pytz import timezone as pytz_timezone
import datetime


from main.models import Store
stores = Store.objects.all()[:50]
from main.views import trigger_report

for store in stores:
    trigger_report(store)