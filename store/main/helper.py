import tempfile
from .models import StoreStatus,  ReportStatus , StoreStatusLog
from django.utils import timezone 
from pytz import timezone as pytz_timezone
import datetime
import csv
import os

def generate_report(store,report):
    
    tz = store.timezone_str if store.timezone_str else 'America/Chicago'
    target_timezone = pytz_timezone(tz)
    # hard coding current time as max of all the logs
    time = StoreStatusLog.objects.all().order_by('-timestamp').first().timestamp
    local_time = time.astimezone(target_timezone)
    utc_timezone = pytz_timezone('UTC')
    utc_time = time.astimezone(utc_timezone)
    current_day = local_time.weekday()
    current_time = local_time.time()

    # last one hour 
    last_one_hour_data = get_last_one_hour_data(store, utc_time, current_day, current_time)
    # last one day
    last_one_day_data = get_last_one_day_data(store, utc_time, current_day, current_time)

    # last one week
    last_one_week_data = get_last_one_week_data(store, utc_time, current_day, current_time)
    data = []
    data.append(store.pk)
    data.extend(list(last_one_hour_data.values()))
    data.extend(list(last_one_day_data.values()))
    data.extend(list(last_one_week_data.values()))

    generate_csv_file(store, report, data)
    return report

def generate_csv_file(store, report, data):
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = f"{store.pk}-{report.pk}.csv"
        temp_file_path = os.path.join(temp_dir, file_name)

        with open(temp_file_path, "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["store_id", "last_one_hour uptime", "last_one_hour downtime", "last_one_hour unit", "last_one_day uptime", "last_one_day downtime", "last_one_day unit", "last_one_week uptime", "last_one_week downtime", "last_one_week unit"])
            csv_writer.writerow(data)
        report.report_url.save(file_name, open(temp_file_path, "rb"))
        report.status = ReportStatus.COMPLETED
        report.save()

def get_last_one_hour_data(store, utc_time, current_day, current_time):
    last_one_hour_data = {"uptime" : 0 , "downtime" : 0 , "unit" : "minutes"}
    is_store_open = store.timings.filter(day=current_day,start_time__lte=current_time,end_time__gte=current_time).exists()
    if is_store_open:
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