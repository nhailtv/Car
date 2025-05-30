sudo apt update
sudo apt upgrade

libcamera-hello --version
sudo apt install -y libcamera0 python3-libcamera

python3 -m pip install picamera2

sudo apt install -y realvnc-vnc-server
sudo raspi-config

sudo systemctl enable vncserver-x11-serviced
sudo systemctl start vncserver-x11-serviced
sudo systemctl status vncserver-x11-serviced

sudo apt install -y python3-picamera2
python3 -m venv venv

git clone https://github.com/ultralytics/yolov5.git
git clone https://github.com/anhtp22it/self-driving-car

python3 -m venv --system-site-packages ~/Desktop/car/venv
sudo apt install -y libqt5gui5 libqt5core5a
