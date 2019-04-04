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
system_sshd_config     ="/route/sshd_config"

```

Examples:

```python
smtp         = 'smtp.gmail.com:587' # GMail
auth_log     = '/var/log/auth.log'  # Debian based systems
trusted_sshd_config    = '/random/route/randname'
system_sshd_config     = "/etc/ssh/sshd_config"   # Debian based systems
```

### Create cron tasks:

- Open a terminal and write:

```
sudo crontab -e
```

- Select your text editor if is your fisrt time using cron

- Add this lines:

```
06 00 * * * python3 /route/dayReport.py
02 * * * * python3 /route/alert.py
```

### Tips

- If is possible don't allow root users to connect by SSH

- If is possible run SSH-Alert from a user with no SSH connections allowed
