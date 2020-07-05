# Mikrotwitter

It's really **mikro**-client:

- No API usage/limit
- No authentication
- No ads
- No tweets with pictures/videos
- No tweets with links anywhere else
- No tweets you've already read
- No javascript
- No autotests
- 126 LoC for CSS, HTML Template and Python app

All you need is:

1. Clone repo: `git clone https://github.com/strizhechenko/mikrotwitter`
2. Install dependencies: `cd mikrotwitter; pip install -r requirements.txt`
3. Fill plaintext file `./config` with user names of people who you want to read.
4. Run app: `python3 -m flask run`
