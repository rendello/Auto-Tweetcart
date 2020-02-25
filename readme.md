
![Auto Tweetcart Cover](artwork/cover-gitlab.png "Auto Tweetcart Cover")

# Synopsis
[@auto_tweetcart](https://twitter.com/auto_tweetcart) is Twitter bot that runs
[PICO-8](https://www.lexaloffle.com/pico-8.php) code and responds with a video
of the results!

Inspired by the lovely [@bbcmicrobot](https://twitter.com/bbcmicrobot).

# Development
Development is done by [@rendello\_](https://twitter.com/rendello_), but help
and forking is accepted! Build intructions are specific, [see the readme in the
source directory](autotweetcart/readme.md).

## Contributing
Please get in touch before putting in a PR or stress-testing the bot.

This project uses:
- [Semantic versioning](https://semver.org),
- [Vincent Driessen's branching model](https://nvie.com/posts/a-successful-git-branching-model/),
- [PEP-8 style guide](https://www.python.org/dev/peps/pep-0008/) + [Black formatter](https://github.com/psf/black),
- [Google-style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html), when needed.

## Roadmap
- Separate Twitter code from back end,
- Create Discord bot with same back end,
- Allow for calling bot from further child tweet of code,
- Add multiple-tweet-per-cart support, for things like [#TweetTweetJam](https://twitter.com/hashtag/TweetTweetJam),
- Add checks against tweets to see what parts, if any, contain code,
- Add DM support.
