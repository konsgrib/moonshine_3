http://pont.ist/rabbit-mq/



sudo nano /etc/systemd/system/my_script.service


[Unit]
Description=My Python Script

[Service]
ExecStart=/home/pi/Projects/moonshine_3/.venv/bin/python3 /home/pi/Projects/moonshine_3/your_script.py
Restart=always
User=pi
Group=pi
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target


====================================================================
sudo systemctl enable producer
sudo systemctl start producer
sudo systemctl status producer


sudo ln -s /home/pi/Projects/moonshine_3/services/producer.service /etc/systemd/system/producer.service
sudo systemctl enable producer
sudo systemctl start producer
sudo systemctl status producer
sudo ln -s /home/pi/Projects/moonshine_3/services/display.service /etc/systemd/system/display.service
sudo systemctl enable display
sudo systemctl start display
sudo systemctl status display
sudo ln -s /home/pi/Projects/moonshine_3/services/alarm.service /etc/systemd/system/alarm.service
sudo systemctl enable alarm
sudo systemctl start alarm
sudo systemctl status alarm
sudo systemctl daemon-reload
sudo ln -s /home/pi/Projects/moonshine_3/services/buttons.service /etc/systemd/system/buttons.service
sudo systemctl enable buttons
sudo systemctl start buttons
sudo systemctl status buttons
sudo systemctl daemon-reload

sudo ln -s /home/pi/Projects/moonshine_3/services/moonshine.target /etc/systemd/system/moonshine.target
sudo systemctl enable moonshine.target
sudo systemctl start moonshine.target
sudo systemctl stop moonshine.target

sudo systemctl disable producer
sudo systemctl disable buttons
sudo systemctl disable alarm
sudo systemctl disable display