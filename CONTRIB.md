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





    1  pwd
    2  mkdir .ssh
    3  cd .ssh
    4  ls -l
    5  chmod 600 id_ed25519
    6  ls -l
    7  cd ../
    8  mkdir Projects
    9  ls -l
   10  cd Projects/
   11  git clone git@github.com:konsgrib/moonshine_3.git
   12  cd moonshine_3/
   13  python --v
   14  python --version
   15  python -m venv .venv
   16  . .venv/bin/activate
   17  pip install -r requirements.txt 
   18  pip install -r requirements.txt --force-pi
   19  pip install --force-pi -r requirements.txt
   20  pip install -r requirements.txt --install-option="--force-pi"
   21  pip install -r requirements.txt 
   22  pip install Adafruit_DHT --install-option="--force-pi"
   23  pip install -r requirements.txt 
   24  vim requirements.txt 
   25  sudp apt install vim
   26  sudo apt install vim
   27  vim requirements.txt 
   28  pip install -r requirements.txt 
   29  vim requirements.txt 
   30  sudo apt update -y
   31  sudo apt-get install rabbitmq-server
   32  sudo systemctl enable rabbitmq-server
   33  sudo systemctl start rabbitmq-server
   34  sudo rabbitmq-plugins enable rabbitmq_management
   35  rabbitmqctl add_user newadmin s0m3p4ssw0rd
   36  rabbitmqctl set_user_tags newadmin administrator
   37  rabbitmqctl set_permissions -p / newadmin ".*" ".*" ".*"
   38  sudo rabbitmqctl add_user newadmin s0m3p4ssw0rd
   39  sudo rabbitmqctl set_user_tags newadmin administrator
   40  sudo rabbitmqctl set_permissions -p / newadmin ".*" ".*" ".*"
   41  sudo rabbitmqctl add_user pi Pi#2024
   42  sudo rabbitmqctl set_user_tags pi administrator
   43  sudo rabbitmqctl set_permissions -p / pi ".*" ".*" ".*"
   44  sudo raspi-config
   45  htop
   46  sudo history
   47  sudo hist
   48  history
   48  history
   49  sudo ln -s /home/pi/Projects/moonshine_3/services/producer.service /etc/systemd/system/producer.service
   50  sudo systemctl enable producer
   51  sudo ln -s /home/pi/Projects/moonshine_3/services/display.service /etc/systemd/system/display.service
   52  sudo systemctl enable display
   53  sudo ln -s /home/pi/Projects/moonshine_3/services/alarm.service /etc/systemd/system/alarm.service
   54  sudo systemctl enable alarm
   55  sudo ln -s /home/pi/Projects/moonshine_3/services/buttons.service /etc/systemd/system/buttons.service
   56  sudo systemctl enable buttons
   57  sudo ln -s /home/pi/Projects/moonshine_3/services/moonshine.target /etc/systemd/system/moonshine.target
   58  sudo systemctl enable moonshine.target
   59  sudo systemctl start moonshine.target