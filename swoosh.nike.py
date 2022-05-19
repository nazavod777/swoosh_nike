# -*- coding: utf8 -*-
from requests import Session
from pyuseragents import random as random_useragent
from random import randint
from concurrent.futures import ThreadPoolExecutor
from ctypes import windll
from urllib3 import disable_warnings
from loguru import logger
from sys import stderr, exit
from os import system
from msvcrt import getch

disable_warnings()
def clear(): return system('cls')


logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white>"
                          " | <level>{level: <8}</level>"
                          " | <cyan>{line}</cyan>"
                          " - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('swoosh nike Auto Reger | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')


class Wrong_Response(BaseException):
    pass


def random_tor_proxy():
    proxy_auth = str(randint(1, 0x7fffffff))\
         + ':' + str(randint(1, 0x7fffffff))
    proxies = {
        'http': 'socks5://{}@localhost:9150'.format(proxy_auth),
        'https': 'socks5://{}@localhost:9150'.format(proxy_auth)}
    return(proxies)


def take_proxies(length):
    proxies = []

    while len(proxies) < length:
        with open('proxies.txt') as file:
            for row in file:
                proxies.append(row.strip())

    return(proxies[:length])


def mainth(email, proxy):
    for _ in range(10):
        try:
            session = Session()
            session.headers.update({
                'user-agent': random_useragent(),
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7',
                'origin': 'https://www.swoosh.nike',
                'referer': 'https://www.swoosh.nike',
                'content-type': 'application/json'})

            if use_proxy == 'y':
                if proxy_source == 2:
                    session.proxies.update({
                        'http': f'{proxy_type}://{proxy}',
                        'https': f'{proxy_type}://{proxy}'})

                else:
                    session.proxies.update(random_tor_proxy())

            r = session.post('https://6ntsotoqbe.execute-api.us-west-2.amazonaws.com/Prod/register',
                             json={"email": email,
                                   "context": "teaser"})

            if r.text != 'OK':
                raise Wrong_Response('')

        except Wrong_Response:
            logger.error(f'{email} | Wrong response, status code: '
                         f'{r.status_code}, response text: {r.text}')

        except Exception as error:
            logger.error(f'{email} | Unexpected error: {error}')

        else:
            logger.success(f'{email} | The account has been successfully registered')

            with open('registered.txt', 'a') as file:
                file.write(f'{email}\n')

            return

    with open('unregistered.txt', 'a') as file:
        file.write(f'{email}\n')


if __name__ == '__main__':
    threads = int(input('Threads: '))
    emails_folder = input('Drop .txt with emails: ')
    use_proxy = input('Use Proxies? (y/N): ').lower()

    with open(emails_folder, 'r') as file:
        emails = [row.strip() for row in file]

    proxies = [None for _ in range(len(emails))]

    if use_proxy == 'y':
        proxy_source = int(input('How take proxies? (1 - tor proxies; 2 - from file): '))

        if proxy_source == 2:
            proxy_type = str(input('Enter proxy type (http; https; socks4; socks5): '))
            proxy_folder = str(input('Drag and drop file with proxies (ip:port; user:pass@ip:port): '))

            proxies = take_proxies(len(emails))

    clear()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(mainth, emails, proxies)

    logger.success('Работа успешно завершена')
    print('\nPress Any Key To Exit..')
    getch()
    exit()
