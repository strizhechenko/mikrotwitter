# coding: utf-8
from requests import get
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect
from functools import reduce
from operator import add
from flask_classful import FlaskView
import logging

app = Flask(__name__)


class MikroTwitterView(FlaskView):
    """ Class-based view/app """
    route_base = '/'
    tweets_prev = set()

    def __init__(self):

        self.authors = [a.replace('@', '') for a in open('./config').read().split('\n') if a and not a.startswith("#")]
        self.cur_author = None

    def _no_shit(self, t):
        """ Filter from things I don't like: links, retweets, replies and pictures """
        for patter in 'pic', 'http', '.com/', '.ru/', '.org', 'ift.tt':
            if patter in t.text:
                return False
        if 'retweeted' in t.parent.parent.parent.text:
            return False
        if 'Replying to' in t.parent.text:
            if len(t.parent.find_all('a')) > 1:
                return False
            if t.parent.find('a').text != '@' + self.cur_author:
                return False
        return t.text.capitalize() not in self.tweets_prev

    def reset(self):
        """ Clean current cache, so you will see all the tweets again. Also re-reads config. """
        logging.warning("cleanup!")
        self.authors = [a.replace('@', '') for a in open('./config').read().split('\n') if a and not a.startswith("#")]
        self.tweets_prev.clear()
        return redirect('/')

    def _fetch(self, author):
        """ Fetch all author tweets """
        url = "https://mobile.twitter.com/{0}".format(author)
        req = get(url)
        if req.status_code != 200:
            print(url, req.status_code, req.content)
        print(url, req.status_code)
        soup = BeautifulSoup(req.content, "html.parser")
        self.cur_author = author
        return [t.text.capitalize() for t in
                filter(self._no_shit, soup.find_all('div', attrs={'class': 'tweet-text'}))]

    def post(self):
        """ Marks all tweets as read """
        tweets = {author: self._fetch(author) for author in self.authors}
        logging.warning("post1: marked as read: %d", len(self.tweets_prev))
        self.tweets_prev |= set(reduce(add, tweets.values()))
        logging.warning("post2: marked as read: %d", len(self.tweets_prev))
        return self.index()

    def index(self):
        """ Just show all unread tweets """
        logging.warning("marked as read: %d", len(self.tweets_prev))
        tweets = {author: self._fetch(author) for author in self.authors}
        page = render_template("index.html", tweets=tweets, tweets_prev=self.tweets_prev)
        return page


MikroTwitterView().register(app)
app.templates_auto_reload = True

if __name__ == '__main__':
    app.run()
