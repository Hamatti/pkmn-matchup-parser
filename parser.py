from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import os

from limitless import parse_limitless
from match import Winner, Match
from player import Player


class Parser:

    RK9_BASEURL = 'https://player.rk9labs.com'

    def __init__(self, rk9_id, limitless_id):
        self.rk9_id = rk9_id
        self.limitless_id = limitless_id
        self.players = {}
        self.limitless = {}
        self.matchups = []

    def run(self):
        self.fetch_limitless()
        self.fetch_rk9_pages()

        for page in self.pages:
            self.fetch_page(page)

        self.print_players(sort=True)
        self.write_json()

    def fetch_limitless(self):
        self.limitless, self.tournament = parse_limitless(self.limitless_id)

    def fetch_page(self, page):
        print(f'Parsing page {page}')
        round_nro = page.split('=')[-1]
        handle = urlopen(f'{self.RK9_BASEURL}{page}')
        match_dom = BeautifulSoup(handle, features='lxml')
        matches = match_dom.find_all('div', {'class': 'match'})
        for match_dom in matches:
            self.matchups.append(self.create_match(match_dom, round_nro))

    def fetch_rk9_pages(self):
        print(f'Fetching the main page')
        handle = urlopen(f'{self.RK9_BASEURL}/pairings/{self.rk9_id}?round=1')
        basepage = BeautifulSoup(handle, features='lxml')

        print(f'Parsing list of subpages')
        urls = basepage.find_all('a')
        self.pages = [url.attrs['href'] for url in urls if self.is_subpage_url(url)]

    def print_players(self, sort=False):
        print(f'Printing players in {"sorted" if sort else "unsorted"} order')
        players = sorted(self.players.items(),
                         key=lambda player: player[1].points(),
                         reverse=sort)

        for name, player in players:
            if(player.deck != '<unknown>'):
                print (f'{name}: {player.record()} /w {player.deck}')

    def is_subpage_url(self, url):
        return url.attrs['href'].startswith(f'/pairings/{self.rk9_id}?round=')

    def get_or_create_player(self, name):
        try:
            return self.players[name]
        except KeyError:
            player = Player(name)
            self.players[name] = player
            return player

    def get_from_limitless(self, name):
        try:
            return self.limitless[name]
        except KeyError:
            return '<unknown>'

    def create_match(self, match_dom, round_nro):
        player1 = self.get_or_create_player(
                            self.parse_name(
                                match_dom.find('div', {'class': 'player1'})
                            )
                  )
        player2 = self.get_or_create_player(
                            self.parse_name(
                                match_dom.find('div', {'class': 'player2'})
                            )
                  )
        if not player1.deck:
            player1.deck = self.get_from_limitless(player1.name)
        if not player2.deck:
            player2.deck = self.get_from_limitless(player2.name)
        winners = match_dom.find_all('div', {'class': 'winner'})
        if(len(winners) == 3):
            winner = Winner.TIE
            player1.ties += 1
            player2.ties += 1
        elif(len(winners) == 0):
            winner = Winner.BYE_OR_DQ
        elif 'player1' in winners[0].attrs['class']:
            player1.wins += 1
            player2.losses += 1
            winner = Winner.PLAYER1
        else:
            player2.wins += 1
            player1.losses += 1
            winner = Winner.PLAYER2

        match = Match(player1, player2, int(round_nro), winner)
        return match

    def parse_name(self, player_dom):
        try:
            parts = player_dom.text.split('\n')
            first = parts[1].strip().title()
            last = parts[2].strip().title()
            return f'{first} {last}'
        except IndexError as e:
            return None

    def write_json(self):
        if not os.path.exists('output'):
            os.makedirs('output')
        filename = f'output/{self.rk9_id}-{self.limitless_id}.json'
        tournament = {
            'name': self.tournament['name'],
            'date': self.tournament['date'],
            'rk9_id': self.rk9_id,
            'limitless_id': self.limitless_id
        }
        players = [player.serialize() for name, player in self.players.items()]
        matches = [match.serialize() for match in self.matchups]

        for match in matches:
            print(match)

        output = {
            'tournament': tournament,
            'players': players,
            'matches': matches
        }

        file_handle = open(filename, 'w')
        json.dump(output, file_handle)