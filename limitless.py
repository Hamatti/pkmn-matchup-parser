from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

LIMITLESS_BASEURL = 'http://limitlesstcg.com/tournaments/?id='


def is_player_row(row):
    return len(row.find_all('td')) > 1


def parse_limitless(limitless_id):
    print(f'Fetching Limitless page for tournament {limitless_id}')
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.get(f'{LIMITLESS_BASEURL}{limitless_id}')
    dom = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()

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
