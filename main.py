"""
    This file is a single-run script that will take in an url for rk9labs pairings page
    and parse all the matchups and their results
"""

import sys, time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


RK9_BASEURL = 'https://player.rk9labs.com'
LIMITLESS_BASEURL = 'http://limitlesstcg.com/tournaments/?id='

@dataclass
class Match:
    player1: str
    player2: str
    round: int
    winner: int

@dataclass
class Player:
    name: str
    deck: str = ''
    wins: int = 0
    losses: int = 0
    ties: int = 0

    def record(self):
        return f'{self.wins}-{self.losses}-{self.ties}'

    def points(self):
        return self.wins * 3 + self.ties

    def __gt__(self, other):
        return self.points() > other.points()


def get_name(player_dom):
    try:
        parts = player_dom.text.split('\n')
        first = parts[1].strip().title()
        last = parts[2].strip().title()
        return f'{first} {last}'
    except IndexError as e:
        return None

def get_or_create_player(name):
    try:
        return players[name]
    except KeyError:
        player = Player(name)
        players[name] = player
        return player

def create_match_class(match_dom, round_nro):
    player1 = get_or_create_player(get_name(match_dom.find('div', { 'class': 'player1'})))
    player2 = get_or_create_player(get_name(match_dom.find('div', { 'class': 'player2'})))
    player1.deck = get_from_limitless(player1.name)
    player2.deck = get_from_limitless(player2.name)
    winners = match_dom.find_all('div', { 'class': 'winner' })
    if(len(winners) == 3):
        winner = 0 # it was a tie
        player1.ties += 1
        player2.ties += 1
    elif(len(winners) == 0):
        winner = -1
    elif 'player1' in winners[0].attrs['class']:
        player1.wins += 1
        player2.losses += 1
        winner = 1
    else:
        player2.wins += 1
        player1.losses += 1
        winner = 2

    match = Match(player1, player2, int(round_nro), winner)
    return match

def is_player_row(row):
    return len(row.find_all('td')) > 1

def get_from_limitless(name):
    try:
        return limitless_data[name]
    except KeyError:
        return '<unknown>'

def parse_limitless(limitless_id):
    print(f'Fetching Limitless page for tournament {limitless_id}')
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.get(f'{LIMITLESS_BASEURL}{limitless_id}')
    dom = BeautifulSoup(driver.page_source, 'lxml')

    ranking = dom.find('table', {'class': 'rankingtable'})
    limitless_data = {}
    for row in ranking.find_all('tr'):
        if not is_player_row(row):
            continue

        cells = row.find_all('td')
        player_name = cells[1].a.string
        deck_name = cells[3].span.attrs['data-original-title']
        limitless_data[player_name] = deck_name

    return limitless_data

if __name__ == '__main__':
    try:
        rk9_id = sys.argv[1]
        limitless_id = sys.argv[2]
    except IndexError as e:
        print(f'Usage: python {__file__} <rk9__id> <limitless_id>')
        sys.exit(1)

    limitless_data = parse_limitless(limitless_id)

    print(f'Fetching the main page')
    basepage = BeautifulSoup(urlopen(f'{RK9_BASEURL}/pairings/{rk9_id}?round=1'), features='lxml')

    print(f'Parsing list of subpages')
    urls = basepage.find_all('a')
    pages = [url.attrs['href'] for url in urls if url.attrs['href'].startswith(f'/pairings/{rk9_id}?round=')]

    matchups = []
    players = {}
    for page in pages:
        print(f'Parsing page {page}')
        round_nro = page.split('=')[-1]
        match_dom = BeautifulSoup(urlopen(f'{RK9_BASEURL}{page}'), features='lxml')
        matches = match_dom.find_all('div', { 'class': 'match' })
        for match_dom in matches:
            matchups.append(create_match_class(match_dom, round_nro))

    # TODO: Last round
    for name, player in players.items():
        if(player.deck != '<unknown>'):
            print (f'{name}: {player.record()} /w {player.deck}')


