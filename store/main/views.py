from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Store, StoreStatusLog, StoreStatus
from .serializers import StoreSerializer
from rest_framework.response import Response
from django.utils import timezone 
from pytz import timezone as pytz_timezone
import datetime
import csv

def trigger_report(store):

    tz = store.timezone_str
    target_timezone = pytz_timezone(tz)
    local_time = timezone.now().astimezone(target_timezone) # - datetime.timedelta(days=180)
    utc_time = timezone.now() # - datetime.timedelta(days=180)
    current_day = local_time.weekday()
    current_time = local_time.time()


    # last one hour 
    last_one_hour_data = get_last_one_hour_data(store, utc_time, current_day, current_time)
    # last one day
    last_one_day_data = get_last_one_day_data(store, utc_time, current_day, current_time)

    # last one week
    last_one_week_data = get_last_one_week_data(store, utc_time, current_day, current_time)

    

    return last_one_hour_data , last_one_day_data , last_one_week_data

def get_last_one_hour_data(store, utc_time, current_day, current_time):
    last_one_hour_data = {"uptime" : 0 , "downtime" : 0 , "unit" : "minutes"}
    is_store_open = store.timings.filter(day=current_day,start_time__lte=current_time,end_time__gte=current_time).exists()
    if is_store_open:
        print(is_store_open,"ione hour")
        last_one_hour_logs = store.status_logs.filter(timestamp__gte=utc_time - datetime.timedelta(hours=1)).order_by('timestamp')
        if last_one_hour_logs:
            last_one_hour_log_status = last_one_hour_logs[0].status
            if last_one_hour_log_status == StoreStatus.ACTIVE:
                last_one_hour_data["uptime"] = 60
            else:
                last_one_hour_data["downtime"] = 60

    return last_one_hour_data
    

def get_last_one_day_data(store, utc_time, current_day, current_time):
    last_one_day_data = {"uptime" : 0 , "downtime" : 0, "unit" : "hours"}
    one_day_ago = current_day - 1 if current_day > 0 else 6
    is_store_open = store.timings.filter(day__gte=one_day_ago,day__lte=current_day,start_time__lte=current_time,end_time__gte=current_time).exists()
    if is_store_open:
        print(is_store_open,"one day")
        last_one_day_logs = store.status_logs.filter(timestamp__gte=utc_time - datetime.timedelta(days=1)).order_by('timestamp')
        last_one_day_log_status = last_one_day_logs.values_list('status',flat=True)
        for status in last_one_day_log_status:
            if status == StoreStatus.ACTIVE:
                last_one_day_data["uptime"] += 1
            else:
                last_one_day_data["downtime"] += 1
    return last_one_day_data

def get_last_one_week_data(store, utc_time, current_day, current_time):
    last_one_week_data = {"uptime" : 0 , "downtime" : 0, "unit" : "hours"}
    one_week_ago = current_day - 7 if current_day > 0 else 0
    is_store_open = store.timings.filter(day__gte=one_week_ago,day__lte=current_day,start_time__lte=current_time,end_time__gte=current_time).exists()
    if is_store_open:
        print(is_store_open,"one_week")
        last_one_week_logs = store.status_logs.filter(timestamp__gte=utc_time - datetime.timedelta(days=7)).order_by('timestamp')
        last_one_week_log_status = last_one_week_logs.values_list('status',flat=True)
        for status in last_one_week_log_status:
            if status == StoreStatus.ACTIVE:
                last_one_week_data["uptime"] += 1
            else:
                last_one_week_data["downtime"] += 1
    
    return last_one_week_data




class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    @action(detail=True, methods=['GET'])
    def trigger_report(self, request):
        store = self.get_object()
        report_id = trigger_report(store)
        return Response.OK({"report_id": report_id})
