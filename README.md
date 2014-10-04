HUMBLEDOOR
----------

This is a simple internet of things (IoT) project that opens the door if you send the right direct message to it. Like in the [Alibaba and The Forty Thieves](http://www.gutenberg.org/files/37679/37679-h/37679-h.htm) story?! Ahem, aaa... yeah, ahem, exacly, yes. Yeah...

###Quick Start

1. Copy the project to your RaspberryPi.
2. Plug in power and internet connection to it.
3. Setup the circuit and mechanical linkage to you door's latch as shown in the attached diagrams. Scroll down for [circuit diagram](#circuit-diagram).
4. **[Setup Twitter credentials](#twitter-credentials)** and the control pin (the physical pin which the relay is connected to) in `conf.ini` file.
5. Start the program by running `sudo ./humbledoor start`. This will begin the program is background. To run the program in foreground use `sudo ./humbledoor start -f`. Log can be found in `logs` directory.
6. To stop the program you will need to execute `sudo ./humbledoor stop`
7. The `humbledoor` script follows the init script pattern. So, you can basically execute the following commands: `sudo ./humbledoor {start|stop|status|restart}`

All set!

![Alibaba and the fourty thieves](http://i.imgur.com/1tpIohz.jpg)

###Customizing the Project
You can customize all the variables of the project by tweaking the `conf.ini` file.

Everytime the Twitter user whose credential is used in this project receives a direct message, the program does one of the three things:

1. If message incoming message **exactly the same** as the "keyword"[1], "a pin"[2] is sent HIGH/ON signal for "some time"[3]. A "welcome message"[4] is send to the sender.
2. If the incoming message matches "a regular expression"[5], the sender is replied with "a tease reply"[6], which is usually a sarcastic comment.
3. If the incoming message does not match the keyword or the regular expression. "A generic response" [7] is sent.

All the information is logged in a "log file"[8] and you can decide the "verbosity"[9] of the log file.


[1] **keyword:** This is essentity the magic word that is needed to be sent to the door as a direct message(DM) to open it. Default is `open sesame`. You can change it to any message to work as open command. Make sure it is not so complicated that you forget it or cannot type on your phone and lock yourself out. That will be a shame.

[2] **relay pin:** Set the _physical_ pin number on your Raspberry Pi that is connected to the relay or whatever external apparatus that you have deviced to open the door. When the magic words (the keyword) is sent as DM this pin is set to HIGH/ON/+5v. Default pin is pin #`12`.

[3] **open_duration_sec:** Pin stays on for this many seconds on receipt of the keyword. The unit is seconds. The default "ON" duration is `20` seconds.

[4] **welcome_msg:** This message is send as a response of successfully opening the door. A welcoming message is a _welcoming message_ that you wanted to welcome your guest with. You can do fun stuffs like sense the temperature and tell the visitor that temperature is 42 degree celcius inside and to take his or her jacket off before entering. But the default messages is, `Welcome to the cavern, my lord. This is your servent Humbledoor.`

[5] **tease_on:** This is a regular expression. If anyone sends a DM that matches to this regular expression (case insensitive) is replied with the text set as teaser_text variable. The defaut is `^open`, so anything that starts with "open" but is not the keyword, is replied with the teaser_text. So, "Open Barley" is not a good idea.

[6] **teaser_text:** A teaser text is, usually, a sarcasmic reply from the door to make a fun experience. The default teaser text is `Is it you, Kasim?`, because you know it is Kasim, in the Alibaba story he is the guy who forgot the keyword, and started trying different grain names but sesame. Please try to not be offensive with because you know, _with great power comes great responsibility_.

[7] **ffwd_msg:** Forward message is a message which is like saying I will convey your message. Or just some helpful response like, "Hey, this is Derpina's door. If you wanted to meet her or open her door, _call her maybe_." But the default is a boring reply: `Hey,You have reached to Humbledoor. I will forward your message to my master. Thanks.`

[8] **log_dir:** is the directory when application log is stored. By default it is saved in `logs` directory in the main directory.

[9] **log_level:** there are only a couple of logs in the script. But you can control what you wanted to see in the log by setting this value to any of the following: debug, info, warning, error, critical. The default is `debug`

###Twitter Credentials

You must set Twitter credentials to make this application work. And it is **NOT OPTIONAL**. Please use your favorite search engine to dig out how to set up a Twitter application. Basically, you need to go to https://apps.twitter.com/ , login with your Twitter credentials, click "Create New App" button fill in details. Fill the URL to anything, say, http://google.com, or something else. Check that you agree with policies and click on "Create Your Application". Go to "Keys and Access Tokens". After this **make sure** you go ahead and allow the app to "read, write and access direct message" of the account. Now generate your access token. Now, you should be seeing four things:

1. Consumer Key: This is what needed to set as `consumer_key` replacing the default `YOUR_CONSUMER_KEY`
2. Consumer Secret: This is what needed to be set as `consumer_secret` in place of  `YOUR_CONSUMER_SECRET`
3. Access Token: is what replaces `access_token` from its default `YOUR_ACCESS_TOKEN`
4. Access Token Secret: This is needed be places as `access_token_secret` instead of default `YOUR_ACCESS_TOKEN_SECRET`


Now you are all set to use Humbledoor!

###Dependency

This project depends on a couple if Python packages that you need to install before you begin:

1. RPi.GPIO
2. tweepy

#####Installing Dependencies

Assuming Python is already installed. Install `pip` if you haven't already done so.

**Installing pip**

    sudo apt-get install python-dev
    curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    python get-pip.py

**Install Dependencies**

    sudo pip install RPi.GPIO
    sudo pip install tweepy

###Circuit Diagram

Here is the circuit diagram:
![Humbledoor Circuit Diagram](https://cdn.rawgit.com/naishe/humbledoor/master/humbledoor_bb.svg)

However, I have used a relay PCB with ULN2003 chip which is basically all the top right circuit built in. Here I have joined a couple of images to show what I mean. (Thanks to [Pixlr.com](http://pixlr.com) for free editing):
![The relay circuit](http://i.imgur.com/k6XJmnH.png)

Happy hacking!
