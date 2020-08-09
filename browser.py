import os
import re
import requests
from colorama import init, Fore, Style
from bs4 import BeautifulSoup
from sys import argv
from collections import deque


init()  # A function initializing colorama library

buttons: list = ['exit', 'back', 'clear history']

tags: list = ['a', 'p', 'ul', 'ol', 'li']

history: deque = deque()


def create_directory(argument):
    if argv[1]:
        try:
            os.mkdir(str(argument))
            print("Directory named {} created!".format(str(argument)))
        except FileExistsError:
            print("Directory named: {} already exists.".format(argument))


def browser(user_input, domain):
    try:
        if not domain:
            if user_input in buttons:
                if user_input == 'exit':
                    exit()
                if user_input == 'back':
                    if len(history) > 0:
                        previous_site = history.pop()
                        with open(argv[1] + '\\' + previous_site[8:] + '.txt', 'r', encoding='utf-8') as f:
                            site = f.read()
                            print(site)
                            f.close()
                        history.append(previous_site)
                    else:
                        print("History is clear.")
                if user_input == 'clear history':
                    history.clear()
                    print("Your browsing history has been cleared now.")
            else:
                print('''
                Error: This is not a valid URL! 
                An URL should end with '.com'
                ''')
        elif os.path.isfile(argv[1] + '\\' + user_input + '.txt'):
                f = open(argv[1] + '\\' + user_input + '.txt', 'r', encoding='utf-8')
                print(f.read())
                f.close()
                history.append(user_input)
        else:
            if not re.findall(r'(?<=https://)', user_input):
                user_input: str = 'https://' + user_input
            if re.findall(r'(?<=https://)\w+\.(?=\w{,4})', user_input):
                f = open(argv[1] + '\\' + user_input[8:] + '.txt', "w+", encoding="utf-8")
                r_content: bytes = requests.get(user_input).content
                soup = BeautifulSoup(r_content, 'html.parser')
                content_to_write: list = []
                for tag in soup.find_all(tags):
                    if tag.name == 'a':
                        content_to_write.append(Fore.BLUE + tag.text)
                        f.write(Fore.BLUE + tag.text)
                    else:
                        content_to_write.append(Style.RESET_ALL + tag.text)
                        f.write(Style.RESET_ALL + tag.text)
                for content in content_to_write:
                    print(content)
                f.close()
                history.append(user_input)
                content_to_write.clear()
    except Exception as error:
        print("Invalid command." + error)


create_directory(argv[1])

while True:
    user_input: str = input()
    domain = re.findall(r'\w+(?=\.)(?=\w{,4})', user_input)
    browser(user_input, domain)
