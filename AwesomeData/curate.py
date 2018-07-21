#!/usr/bin/python

import datetime
import json

import requests

import utils_github
import utils_markdown

the_awesome_url = 'https://github.com/sindresorhus/awesome'


#https://mathiasbynens.be/demo/url-regex
#validate
#github with urlparse

_, commit_hash, raw_url = utils_github.github_shortname_commit_hash_raw_url_from_awesome_url(the_awesome_url)

r = requests.get(raw_url)
assert r.encoding == 'utf-8'
assert r.status_code == 200
the_awesome_content = r.text

utils_markdown.md_print_test(the_awesome_content)

# awesome_data = {}
# awesome_data['links'] = utils_markdown.getListOfGithubLinksfromString(the_awesome_content)
# awesome_data['commit_hash'] = commit_hash
# awesome_data['datetime'] = datetime.datetime.now().isoformat()

# with open('data.json', 'w') as outfile:
#     json.dump(awesome_data, outfile, indent=4, ensure_ascii=False,sort_keys=False)
