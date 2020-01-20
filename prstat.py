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

parse_argument()
prs = PoolRequestStat(make_request(args.username, args.repo))
prs.pr_in_day()

# parse_argument()
# mr = make_request(args.username, args.repo)
# print(mr)

# pp = pprint.PrettyPrinter()
# pp.pprint(make_request(args.username, args.repo)[1])

print(1)
