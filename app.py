# coding: utf-8
from requests import get
from bs4 import BeautifulSoup
from flask import Flask, render_template
from functools import reduce
from operator import add
from flask_classful import FlaskView

app = Flask(__name__)


class MikroTwitterView(FlaskView):
    route_base = '/'

    def __init__(self):
        self.tweets_prev = set()
        self.authors = [a.replace('@', '') for a in open('./config').read().split() if not a.startswith("#")]

    def _no_shit(self, t):
        return 'pic' not in t.text and 'http' not in t.text and t.text.capitalize() not in self.tweets_prev

    def _fetch(self, author):
        req = get(f"https://twitter.com/{author}")
        if req.status_code != 200:
            print(req.status_code, req.content)
        soup = BeautifulSoup(req.content, "lxml")
        return [t.text.capitalize() for t in
                filter(self._no_shit, soup.find_all('p', attrs={'class': 'TweetTextSize'}))]

    def index(self):
        tweets = {author: self._fetch(author) for author in self.authors}
        page = render_template("index.html", tweets=tweets, tweets_prev=self.tweets_prev)
        self.tweets_prev |= set(reduce(add, tweets.values()))
        return page


MikroTwitterView().register(app)
app.templates_auto_reload = True

if __name__ == '__main__':
    app.run()
