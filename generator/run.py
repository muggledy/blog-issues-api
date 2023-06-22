# -*- coding: utf-8 -*-
# author: https://github.com/Zfour
import json

import yaml
from bs4 import BeautifulSoup

from request_data import request

data_pool = []


def load_config():
    f = open('_config.yml', 'r', encoding='utf-8')
    ystr = f.read()
    ymllist = yaml.load(ystr, Loader=yaml.FullLoader)
    return ymllist


def github_issuse():
    print('\n')
    print('------- github issues start ----------')
    baselink = 'https://github.com/'
    config = load_config()
    try:
        for number in range(1, 100):
            '''
            if config['issues']['label']:
                label_plus = '+label%3A' + config['issues']['label']
            else:
                label_plus = ''
            gh_issue_api_link = f"https://github.com/{config['issues']['repo']}/issues?q=is%3A{config['issues']['state']}{str(label_plus)}&page={str(number)}"'''
            gh_issue_api_link = f"https://api.github.com/repos/{config['issues']['repo']}/issues?sort=updated&state={config['issues']['state']}&page={str(number)}&per_page=100&labels={config['issues']['label']}"
            github = request.get_data(gh_issue_api_link)
            if github == '[]':
                break
            print(gh_issue_api_link)
            gh_issue_data = json.loads(github)
            print(gh_issue_data)
            data_pool.extend(gh_issue_data)
            if len(gh_issue_data) < 100:
                break
            '''soup = BeautifulSoup(github, 'html.parser')
            main_content = soup.find_all('div', {'aria-label': 'Issues'})
            linklist = main_content[0].find_all('a', {'class': 'Link--primary'})
            if len(linklist) == 0:
                print('> end')
                break
            print(gh_issue_api_link)
            for item in linklist:
                issueslink = baselink + item['href']
                issues_page = request.get_data(issueslink)
                issues_soup = BeautifulSoup(issues_page, 'html.parser')
                try:
                    issues_linklist = issues_soup.find_all('pre')
                    source = issues_linklist[0].text
                    if "{" in source:
                        source = json.loads(source)
                        print(source)
                        data_pool.append(source)
                except:
                    continue
            '''
    except:
        print('> end')

    print('------- github issues end ----------')
    print('\n')


# 友链规则
github_issuse()
filename = 'generator/output/v1/data.json'
with open(filename, 'w', encoding='utf-8') as file_obj:
    json.dump(data_pool, file_obj, ensure_ascii=False)
