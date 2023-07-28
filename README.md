# Store Monitoring System


Python Django framework and PostgreSQL database.

Step by step logic for last one day (uptime and downtime):
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


APIs :

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
