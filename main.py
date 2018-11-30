import re
import sbis
import requests
from const import *

class NewsInfo:
    AuthorName = ''
    Title = ''
    Brief = ''
    DateTime = ''
    NewsLink = ''
    AuthorCallLink = ''
    AuthorUUID = ''

    def __init__(self, author_name='', title='', brief='', date_time='', news_link='', call_link='', author_uuid=''):
        self.AuthorName = author_name
        self.Title = title
        self.Brief = brief
        self.DateTime = date_time
        self.NewsLink = news_link
        self.AuthorCallLink = call_link
        self.AuthorUUID = author_uuid

    def get_json(self):
        return {
            'AuthorName': self.AuthorName,
            'Title': self.Title,
            'Brief': self.Brief,
            'DateTime': self.DateTime,
            'NewsLink': self.NewsLink,
            'AuthorCallLink': self.AuthorCallLink,
            'AuthorUUID': self.AuthorUUID
        }


class RecordFilter:

    filter_names_with_types = []
    filter_values = []

    def __init__(self, names_with_types=[], values=[]):
        self.filter_names_with_types = names_with_types
        self.filter_values = values
        # Добавим дефолтное поле, чтобы выбирать в определенной группе
        if ('Channel', 'string') not in self.filter_names_with_types:
            self.filter_names_with_types.append(('Channel', 'string'))
            self.filter_values.append(GROUP_ID)

    def get_names_with_types(self):
        return ' '.join([item[0] + ':' + item[1] for item in self.filter_names_with_types])

    def get_values(self):
        return self.filter_values


def get_str(event, key):
    return str(event[key]) if key in event and event[key] is not None else ''


def event_list(record_filter=RecordFilter()):

    events = sbis.rpc_return_recordset('service', 'Event.ListWallWithPosition', {
        'ДопПоля': [],
        'Фильтр': sbis.record(
            record_filter.get_names_with_types(),
            record_filter.get_values()),
        'Сортировка': None,
        'Навигация': sbis.navigation(0, 10, True)
    })
    return events

if __name__ == '__main__':
    # Залогинимся, под системным юзером
    sbis.login(BASE_URL, SYSTEM_LOGIN, SYSTEM_PASS)

    # Получим список новостей:
    news_list = event_list()
    news_list_json = []
    for news in news_list:
        news_list_json.append(
            NewsInfo(author_name=get_str(news, 'AuthorName'),
                     title=get_str(news['RecordNews'], 'Title'),
                     brief=re.sub(r'<.*?>', r'', get_str(news['RecordNews'], 'Brief')),
                     date_time=get_str(news, 'LentaDateTime'),
                     news_link=LINK_PREFIX.format(get_str(news, 'Object')),
                     call_link=CALL_LINK_PREFIX.format(get_str(news, 'Author')),
                     author_uuid=get_str(news, 'Author')
                     ).get_json()
        )

    print(news_list_json)
