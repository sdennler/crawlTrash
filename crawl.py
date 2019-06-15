#!/usr/bin/env python3
from lxml import html
import requests
from datetime import datetime
import locale
import re
import json

def crawlThunstetten():
    url = "http://www.thunstetten.ch/de/politikuverwaltung/verwaltung/abfall/abfalldaten/?print=print"
    page = requests.get(url)
    tree = html.fromstring(page.content)
    tableRows = tree.xpath('/html/body/table/tr/td/table')[0].iter('tr')

    events = []
    next(tableRows)
    for row in tableRows:
        event = {}
        event['url'] = 'http://www.thunstetten.ch/de' + row.xpath('td[1]//a/@href')[0].replace('../../../..', '')
        event['topic'] = row.xpath('td[2]//text()[1]')[0]
        event['location'] = row.xpath('td[3]//text()[1]')[0]
        event['contact'] = row.xpath('td[4]')[0].text_content().strip()
        event['time'] = row.xpath('td[1]//a/text()[2]')[0].strip()

        date = thunstettenDate(row.xpath('td[1]//a/text()[1]')[0])
        times = re.findall(r'(([0-9]{2})\.([0-9]{2}))', event['time'])
        if len(times) <= 0:
            event['dateStart'] = date
        if len(times) > 0:
            event['dateStart'] = date.replace(hour=int(times[0][1]), minute=int(times[0][2]))
        if len(times) > 1:
            event['dateEnd'] = date.replace(hour=int(times[1][1]), minute=int(times[1][2]))
        events.append(event)

    return events

def thunstettenDate(trash):
    trash = trash.replace('März', 'Mär.')
    trash = trash.replace('April', 'Apr.')
    trash = trash.replace('Juni', 'Jun.')
    trash = trash.replace('Juli', 'Jul.')
    trash = trash.replace('Sept.', 'Sep.')
    locale.setlocale(locale.LC_ALL, 'de_CH.utf8')
    return datetime.strptime(trash, '%d. %b. %Y')

def makeJson(events):
    return json.dumps(events, sort_keys=True, indent=4, default=str)


if __name__ == '__main__':
    print(makeJson(crawlThunstetten()))
