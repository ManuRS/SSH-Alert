# SSH-Alert
Get notified via email when somehting happend in the ssh (bad pass, user not allowed, reset server)

## dayReport.py
Report of the day

## alert.py
If something strange happend last hour you will recive an email

## Intructions

You have to create a aux.py like this:

```python
fromaddr     = 'from@server.com'
toaddrs      = 'to@server.com'
pas          = 'password of fromaddr'
smtp         = 'smtp.sever.com:port'
ipstack_com  = '12345678901234567890123456789012' # ipstack.com needs API key
auth_log     = '/route/auth.log'
trusted_sshd_config    = '/route/sshd_backup_name'
system_sshd_config     = '/route/sshd_config'

```

Examples:

```python
smtp         = 'smtp.gmail.com:587' # GMail
auth_log     = '/var/log/auth.log'  # Debian based systems
trusted_sshd_config    = '/random/route/randname'  # Where you want
system_sshd_config     = '/etc/ssh/sshd_config'    # Debian based systems
```

Using GMail:
- May 30, 2022: Google no longer supports the use of an account and password directly to login in 3rd party apps.
- At least for now, is possible to create a specific password for 3rd party apps (different from your main password).
- For that, you need to enable 2FA in your Google Account and then create this app password.
- Finally, use this password in the variable "pas" on "aux.py" as usual.
- Check Google oficial details [here](https://support.google.com/accounts/answer/6010255) and [here](https://support.google.com/accounts/answer/185833)
- Since this method can be dropped by Google, we recommend using another email provider.
- If Google makes the use of OAuth mandatory, there are no plans to support it.

### Create cron tasks:

Open a terminal and write:

```
sudo crontab -e
```

Select your text editor if is your fisrt time using cron

Add this lines:

```
06 00 * * * python3 /route/dayReport.py
02 * * * * python3 /route/alert.py
```

### IP details source:

| Name                 | Details |
|----------------------|-------------------------|
| https://ipinfo.io/       | Not working in some enviroments        | 
| http://api.ipstack.com/  | Needs API key and lack of ISP info     | 
| http://ip-api.com/       | Default and the most complete info     | 

Change IP details source:

```
Go to getIPdata.py line 23 and select one function to call 
```

Note: Default service (or more to come) is not fully decided      


### Tips

- If is possible don't allow root users to connect by SSH

- If is possible run SSH-Alert from a user with no SSH connections allowed

### Crontab help

```
 ┌───────────────────────────  minute (0 - 59)
 │     ┌─────────────────────  hour (0 - 23)
 │     │     ┌───────────────  day of month (1 - 31)
 │     │     │     ┌─────────  month (1 - 12)
 │     │     │     │     ┌───  day of week (0 - 6 => Sunday - Saturday, or
 │     │     │     │     │                  1 - 7 => Monday - Sunday, or
 ↓     ↓     ↓     ↓     ↓                  Sun, Mon, ..., Sat)
 *     *     *     *     *     command
 min   hour  day   mon   week  command
 ```
 ```
 E.g.:
 15 09 * * Fri,Sat,Sun command
 - command every Friday, Saturday, and Sunday at 9:15.
 ```
