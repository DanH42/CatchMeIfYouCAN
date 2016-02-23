Catch Me If You CAN
===================

The most realistic Mario Kart 64 simulator ever

Requirements
------------

- Python 2.7+
- [PyKeyboard](https://github.com/SavinaRoja/PyUserInput)
- [m64py](http://m64py.sourceforge.net/) - A frontend for Mupen64Plus
- A copy of Mario Kart 64 as a ROM image
- Raspberry Pi + [PiCAN](http://skpang.co.uk/catalog/pican2-canbus-board-for-raspberry-pi-2-p-1475.html)
- [ODB-II to DB9 cable](https://www.sparkfun.com/products/10087) (you can also wire this yourself)
- A car (currently only tested on a 2012 Honda CR-V)
- A low-latency network connection between your Pi and the laptop running m64py

Setup
-----

Install SocketCAN on the Pi according to [this guide](http://skpang.co.uk/blog/archives/1165). Connect
the Pi to your car and verify that `./candump can0` prints a stream of data to your screen. If you're
using the ODB-II cable, keep in mind there are 3 jumpers -- SJ1, SJ2, and SJ3 -- that need to be
soldered on the board ([this PDF](http://skpang.co.uk/catalog/images/raspberrypi/pi_2/PICAN2UGB.pdf)
provides details).

Connect the Pi to your laptop. Your network configuration is up to you, but a hard-wired connection is
highly recommended due to latency concerns. We found that an Ethernet cable running directly from the
Pi to the laptop worked best, configured as such:

- On the Pi: `sudo ip ad add 10.0.0.10/24 dev eth0`
- On the laptop: `sudo ip ad add 10.0.0.20/24 dev eth0`

Assuming this setup, verify that the Pi can ping 10.0.0.20.

Launch m64py and load a Mario Kart 64 ROM. Using the default controls, try playing a game to make sure
everything works. Shift/Ctrl are gas/brakes respectively, and arrow keys steer.

Usage
-----

Level out your steering wheel as best as you can. **Put the car in park/neutral and make sure your
parking brake is on.** Take your feet off the pedals.

On the laptop, start the Python script as a normal user:

    python game.py

Start m64py and launch Mario Kart.

On the Pi, start candump and have it send relevant data to the laptop:

    ./candump can0,17c:7FF,1a6:7FF,156:7FF,294:7FF | nc -u 10.0.0.20 1738

By default, port 1738 is used. You can change this in the script if you experience a conflict.

Give focus to the m64py window.

**NOTE:** Once you start the script on the Pi, the Python script will begin emulating a keyboard. If
your steering wheel was not level or you had any pedals held down, this will cause key presses to be
passed to the active window. Move your focus to m64py as quickly as possible to avoid confusion.

You should be able to navigate the menu using the car. The steering wheel will move you left/right, and
gas/brakes will move you up/down menu trees.

Start racing!

Controls
--------

- Steering: Turn the steering wheel left/right.
- Acceleration: Hit the gas pedal. Gas is binary in Mario Kart, so more pressure will not increase speed.
- Brakes: Hit your brakes. Again, this is a binary input.
- Use item: Activate your winshield wipers.
- Jump: Toggle your high beams.
