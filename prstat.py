#! /usr/bin/env python
import pprint
import json
import argparse
import getpass
from collections import defaultdict


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="username for authentication")
    parser.add_argument("--repo", "-r", default='devops_lab', help="repo for statistic")
    parser.add_argument("--poolrequestperday", action="store_true", help="show pool request per day")
    parser.add_argument("--userwhoopen", action="store_true", help="show users who opened pool requests")
    parser.add_argument('--version', '-v', action='version', version='My test util v.0.0.1')
    global args
    args = parser.parse_args()


def make_request(username, repo):
    import requests
    passw = getpass.getpass(prompt='Enter password for your account in github... ')
    payload = {'per_page': 100}
    p = 1
    res = []
    urllink = "https://api.github.com/repos/alenaPy/{0}/pulls".format(repo)
    while True:
        payload['page'] = p
        r = requests.get(urllink, auth=(username, passw),
                         params=payload)
        js = r.json()
        if js != []:
            for el in js:
                res.append(el)
        else:
            break
        p += 1
    return res


class PoolRequestStat:
    '''class stored info about pool requests'''

    def __init__(self, poolrequestresult):
        self.poolrequestresult = poolrequestresult

    def pr_in_day(self):
        count_dict = {}
        for i in range(len(self.poolrequestresult)):
            key = self.poolrequestresult[i]['head']['repo']['pushed_at'][:10]
            if key not in count_dict:
                count_dict[key] = 1
            else:
                count_dict[key] += 1
        for k, v in count_dict.items():
            print(k,v)

    def usr_opened(self):
        for i in range(len(self.poolrequestresult)):
            key = self.poolrequestresult[i]['user']['login']
            val = self.poolrequestresult[i]['number']
            print("{} opened pool request number {}".format(key, val))



parse_argument()
prs = PoolRequestStat(make_request(args.username, args.repo))

if args.poolrequestperday:
    prs.pr_in_day()
if args.userwhoopen:
    prs.usr_opened()


print(1)
