# pir-ssh-alarm
Detects people before they get to your desk.

My desk at work was facing a wall. As other people who write code with their headphones can attest, it scares the crap out of us when people walk up to ask us something, because to us, you just appeared out of nowhere. 

To solve this, I hooked up a PIR sensor I had lying around, a [RadioShack 2760347](https://www.radioshack.com/products/radioshack-passive-infrared-sensor?variant=20332053829) to ground, power, and signal to a Raspberry Pi. The Raspberry Pi runs a script on startup to watch for PID input. When motion is detected, it fires a SSH command to the server (your workstation) which you can use to play a sound.

# Raspberry Pi Setup
This walkthrough assumes you have some familiarity with using Linux and that you have a Raspberry Pi all setup and ready for commands.

### Connect your PIR sensor
Your PIR sensor should have come with some information on what voltage it likes, mine was fine with 3.3v or 5v. I used pin 01 for power, pin 06 for ground, and pin 11 for input. These are numbered by the board numbering, not GPIO, there's a difference. See [this](http://www.raspberry-pi-geek.com/var/rpi/storage/images/media/images/raspib-gpio/12356-1-eng-US/RasPiB-GPIO_lightbox.png) for a Pi pinout.
### SSH into your Pi.
### Install dependancies
The only special thing I needed was screen to keep our daemon visible. 

`sudo apt-get install screen -y`

Copy the clientPIR.py file into ~/scripts

```
mkdir ~/scripts
cd scripts
wget https://raw.githubusercontent.com/milesoberstadt/pir-ssh-alarm/master/clientPIR.py
```

### Configure clientPIR.py to use your server with SSH
Open the clientPIR.py file for editing

`nano clientPIR.py`

Change ssh address to the user and server you want to use (example: miles@192.168.1.1)

Ctrl + O to save

Ctrl + X to exit

Generate public and private keys for the Raspberry Pi

`ssh-keygen`

You can take the defaults for all of the prompts, just press enter.

Copy your Pi's public key over to your workstation, so it will trust your Pi. 

`ssh-copy-id -i ~/.ssh/id_rsa.pub miles@192.168.1.1` Where "miles@192.168.1.1" is your server's username and IP address 

Test your new passwordless config

`ssh miles@192.168.1.1`  

Add an entry to crontab to make the python script run when the Pi starts up.

`sudo crontab -e`

Add the following line to the end of the file

`@reboot /usr/bin/screen -dm /usr/bin/python /home/pi/scripts/pirAlarm.py`

Reboot the Pi, your configuration should be ready.

You can check that it worked by running `sudo screen -r`, which should attach you to the screen session started for this script.

# Server (workstation) setup
### Install dependancies
`sudo apt-get install sox -y`
### Make the server script that the client will call
```
mkdir ~/scripts
cd ~/scripts
wget https://github.com/milesoberstadt/pir-ssh-alarm/raw/master/serverPIR.sh
chmod +x serverPIR.sh
```

That's it, you should be all up and running!
