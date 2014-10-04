HUMBLEDOOR
----------

This is a simple internet of things (IoT) project that opens the door if you send if you send the right direct message to it.

###Functionality

1. Copy the project to your RaspberryPi.
2. Plug in power and internet connection to it.
3. Setup the circuit and mechanical linkage to you door's latch as shown in the attached diagrams. [TODO: add diagrams]
4. Setup Twitter credentials and the control pin (the physical pin which the relay is connected to) in `conf.ini` file. [TODO]
5. Start the program by running `./humbledoor`. This will begin the program is background. To run the program in foreground use `./humbledoor -f`. Log can be found in `logs` directory. [TODO]

###Dependency

This project depends on a couple if Python packages that you need to install before you begin:

1. RPi.GPIO
2. tweepy

TODO: write dependency installation


Happy hacking!
