# Store Monitoring System

This is a backend system built using Python Django framework and PostgreSQL database to monitor the status of several restaurants in the US. The system tracks whether the stores are online or not during their business hours and provides restaurant owners with detailed reports on store uptime and downtime.

# Problem : 
A system monitors several restaurants in the US and needs to monitor if the store is online or not. All restaurants are supposed to be online during their business hours. Due to some unknown reasons, a store might go inactive for a few hours. Restaurant owners want to get a report of the how often this happened in the past.   

build backend APIs that will help restaurant owners achieve this goal.

# Data Source: 
CSV can be found in /store/main/csv_data
1. We poll every store roughly every hour and have data about whether the store was active or not in a CSV.  The CSV has 3 columns (`store_id, timestamp_utc, status`) where status is active or inactive.  All timestamps are in **UTC**
2. We have the business hours of all the stores - schema of this data is `store_id, dayOfWeek(0=Monday, 6=Sunday), start_time_local, end_time_local`
    1. These times are in the **local time zone**
    2. If data is missing for a store, assume it is open 24*7
3. Timezone for the stores - schema is `store_id, timezone_str`
    1. If data is missing for a store, assume it is America/Chicago
    2. This is used so that data sources 1 and 2 can be compared against each other. 

APIs to output a csv filte o the user that has the following schema
- Uptime and downtime should only include observations within business hours
`store_id, uptime_last_hour(in minutes), uptime_last_day(in hours), update_last_week(in hours), downtime_last_hour(in minutes), downtime_last_day(in hours), downtime_last_week(in hours)`

# Solution: - 

- Tech used: 
Python Django framework and PostgreSQL database.

# Step by step logic for last one day (uptime and downtime):
- Initialize a dictionary last_one_day_data with keys "uptime", "downtime", and "unit". The values for "uptime" and "downtime" are set to 0, and "unit" is set to "hours".

- Calculate one_day_ago as the day of the week one day before the current_day. If current_day is 0 (Monday), set one_day_ago to 6 (Sunday).
- Check if the store is open during the last one day (one_day_ago to current_day) at the current time (current_time). 
- This is done by querying the store.timings to see if there is any entry that matches the conditions for day and time.
- If the store is not open during the last one day, return the initialized last_one_day_data.
- If the store is open during the last one day, query the store.status_logs to get all the logs within the last one day (utc_time - 1 day to utc_time) and order them by timestamp.
- Loop through each log in last_one_day_logs:
- Check if the log's timestamp falls within the store's business hours on that day (log_in_store_business_hours). This is done by querying the store.timings to see if there is any entry that matches the conditions for day and time.
- If the log is not within the store's business hours, skip it and move to the next log.
- If the log's status is "active", increment the "uptime" value in last_one_day_data by 1 hour.
- If the log's status is not "active", increment the "downtime" value in last_one_day_data by 1 hour.
- Same logic has been followed for last one hour and last one week uptime and downtime.


# APIs :

1) Trigger Report
   curl --request GET \
  --url http://localhost:8000/store/9200325206334396031/trigger_report/ \
  --header 'Content-Type: application/json' \
  --data '	'
   
3) Get Report
   curl --request POST \
  --url http://localhost:8000/store/get_report/ \
  --header 'Content-Type: application/json' \
  --data '{
	"report_id": 74
	
}'
