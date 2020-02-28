
# Running the bot
If you can't use [@auto_tweetcart](https://twitter.com/auto_tweetcart/), and
want to run / fork the project, follow these instructions.

Run the bot with `./twitter_bot.py`, provided the project is set up like this:
<pre>
OS: Ubuntu 18.04 (same with containers)

===== LXC CONTAINER 1 (NAME IRRELEVANT) =====
Note:
	Nesting Must be enabled for this container.

Requirements:
	- Python 3.7
	- Tweepy

autotweetcart/
├── GIF
│   └──            ← GIFs will automatically be extracted here
├── back_end.py    ← Code pre-processing (swear-filtering, etc.)
├── code_file      ← PICO-8 code is auto-pasted here before being pushed into p8 container
├── profanity.txt  ← Base64-encoded file filled with swears (for filtering purposes)
├── run.sh         ← Pastes code and pushes it to p8
└── twitter_bot.py ← Twitter logic

.autotweetcart/
└── keys.json      ← JSON file with Twitter keys (see twitter_bot.py and Twitter Docs)

===== LXC CONTAINER 2 (NAME ‘P8’) =====
Requirements:
	- Xvfb
	- Xdotool
	- Xclip
	- Gifsicle

root
├── atc
│   ├── GIF
│   │   ├── PICO-8_0.gif  ← These GIFs generated
│   │   └── PICO-opti.gif
│   └── p8.sh      ← The bulk of the PICO-8 stuff done here
├── pico8          ← Your PICO-8 binary & .dat file
└── pico8.dat
</pre>
