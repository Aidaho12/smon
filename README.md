# smon
Simple monitoring TCP ports with alerting via Telegram

# Use

```
# smonctl -h
usage: smonctl [-h] {list,add,del,enable,disable} ...

Simple service for monitoring TCP ports

positional arguments:
  {list,add,del,enable,disable}
    list                List of services
    add                 Add new service to monitoring
    del                 Delete service from monitoring
    enable              Enable service monitoring
    disable             Disable service monitoring

optional arguments:
  -h, --help            show this help message and exit
```

# Install

Just copy repository to /opt/smon and exicute next commands:

```
cd /opt/smon
sudo chmod +x *.py
pip3 install -r requirements.txt
sudo ./sql.py
sudo mv smon.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable smon
sudo systemctl start smon
```

# Settings

Edit /opt/smon/smon.cfg with your env
