import requests
import concurrent.futures
import time
import json
import utils_github

with open('data.json') as json_data:
    d = json.load(json_data)

awesome_urls = [link['url'] for link in d['links']]

# Time requests running in threads
then = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    awesome_infos = list(executor.map(utils_github.github_shortname_commit_hash_raw_url_from_awesome_url, awesome_urls))
print("Threadpool done in {:f}".format(time.time()-then))

max_awesome_url_len = len(max(awesome_urls, key=len))
max_shortname_len = max(len(awesome_info[0]) for awesome_info in awesome_infos)
max_commit_hash_len = max(len(awesome_info[1]) for awesome_info in awesome_infos)
max_raw_url = max(len(awesome_info[2]) for awesome_info in awesome_infos)

for link, awesome_info in zip(awesome_urls,awesome_infos):
    print('{awesome_url:{max_awesome_url_len}}:{shortname:{max_shortname_len}}-{commit_hash:{max_commit_hash_len}}-{raw_url:{max_raw_url}}'
          .format(
                  awesome_url = link,
                  shortname = awesome_info[0],
                  commit_hash = awesome_info[1],
                  raw_url = awesome_info[2],
                  max_awesome_url_len = max_awesome_url_len,
                  max_shortname_len = max_shortname_len,
                  max_commit_hash_len = max_commit_hash_len,
                  max_raw_url = max_raw_url)
        )

    # 

    # r = requests.get(url)
    # if (r.status_code != 200):
    #     raise Exception(shortname + ": " + r.status_code)

    # if (r.encoding != 'utf-8'):
    #     raise Exception(shortname + ": " + r.encoding)

    # content = r.text
    
    # if (content is None):
    #     raise Exception(shortname + ": content == None")


    # return content