# SHH-Alert
Get notified via email when somehting happend in the ssh (bad pass, user not allowed)

## dayReport.py
Report of the day

## alert.py
If something strange happend last hour you will recive an email

## dayReport.py
Resumen of the day

## Intructions
Create cron tasks:

crontab -e

06 00 * * * python3 /route/dayReport.py

02 * * * * python3 /route/alert.py
