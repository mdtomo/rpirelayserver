# Raspberry Pi Relay Server
> Control your relay board with a Raspberry Pi over a LAN. 

This is the command server for controlling a relay board, connected to your Raspberry Pi. Check out [Rpirelayclient](https://github.com/mdtomo/rpirelayclient) for the command line user interface client. You can run both client and server on the same machine attached to localhost (127.0.0.1). 

When the client connects to the server, the server will update the client with the default state of each relay. The client can turn on or off any of the relays and the state will be preserved for next time the client connects. 

## Installation/Usage

The main dependency for Rpirelayserver is [gpiozero](https://github.com/RPi-Distro/python-gpiozero). Please read their docs for installation instructions. Although this project was built using pipenv, pipenv is not designed to be run under root. Gpiozero must be run under root in order to get hardware access on the Raspberry Pi. Gpiozero will not function correctly under any virtual environment.

```sh
git clone https://github.com/mdtomo/rpirelayserver`
cd rpirelayserver
```

Change the settings in config.py and set the output pins you are using on your Raspberry Pi. Set the ip to 127.0.0.1 if you wish to run [Rpirelayclient](https://github.com/mdtomo/rpirelayclient) on the same Raspberry Pi. To control over a LAN use your Raspberry Pi's LAN ip address. (`ifconfig`). I would not recommend using your public ip address.

Run the server.

`sudo python3.7 rpirelayserver.py`

##License
This project is licensed under the MIT License - see the LICENSE.md file for details.
