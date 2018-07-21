import git
import re
import requests

# read: http://www.zverovich.net/2016/06/16/rst-vs-markdown.html

# https://www.debuggex.com/r/H4kRw1G0YPyBFjfm
# ex: https://github.com/shlomi-noach/awesome-mysql/blob/gh-pages/index.md
# ex: https://github.com/numetriclabz/awesome-db
GITHUB_REPO_URL_PATTERN = r"""
    https?://github\.com/
    (?P<shortname>[A-Za-z0-9\-_.]+/[A-Za-z0-9\-_.]+)
    (?:/blob/(?P<symref>[^/\s]+)/(?P<path>\S+))?      #Optional non-capturing group
    """
GITHUB_REPO_URL_RE = re.compile(GITHUB_REPO_URL_PATTERN, re.X)

# ex: href="/emacs-tw/awesome-emacs/blob/master/README.org">
# <h3>
#   <svg class="octicon octicon-book" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true">
#     <path fill-rule="evenodd" d="M3 5h4v1H3V5zm0 3h4V7H3v1zm0 2h4V9H3v1zm11-5h-4v1h4V5zm0 2h-4v1h4V7zm0 2h-4v1h4V9zm2-6v9c0 .55-.45 1-1 1H9.5l-1 1-1-1H2c-.55 0-1-.45-1-1V3c0-.55.45-1 1-1h5.5l1 1 1-1H15c.55 0 1 .45 1 1zm-8 .5L7.5 3H2v9h6V3.5zm7-.5H9.5l-.5.5V12h6V3z">
#     </path>
#   </svg>
#   README.md
# </h3>
def _github_find_readme_filename_in_awesome_url_html_content(content, shortname):
    GITHUB_README_FILENAME_IN_AWESOME_URL_CONTENT_PATTERN = r"""<h3>\s*.*<svg class="octicon octicon-book".*</svg>\s*(?P<path>\S+)\s*</h3>"""
    match = re.search(GITHUB_README_FILENAME_IN_AWESOME_URL_CONTENT_PATTERN, content)
    
    if (match is None):
        raise Exception(shortname + "!!!!!" + content)
    return match.group('path')

# https://stackoverflow.com/a/12093994
GITHUB_HEAD_LSREMOTE_PATTERN = r"""
    refs/heads/(?P<symref>\S+)
    """
GITHUB_HEAD_LSREMOTE_RE = re.compile(GITHUB_HEAD_LSREMOTE_PATTERN, re.X)

def github_shortname_commit_hash_raw_url_from_awesome_url(awesome_url):
    shortname, _path = github_shortname_and_path_from_awesome_url(awesome_url)
    git_url = github_git_URL_from_shortname(shortname)
    _symref, commit_hash = github_HEAD_symref_and_commit_hash_for_git_URL(git_url)
    raw_url = github_raw_url_from_shortname_symref_path(shortname, _symref, _path)
    print('.', end='', flush=True)
    return shortname, commit_hash, raw_url

# git ls-remote --symref <url> HEAD
def github_HEAD_symref_and_commit_hash_for_git_URL(git_url):
    result = git.cmd.Git().ls_remote("--symref", git_url, 'HEAD')
    symref = None
    commit_hash = None

    for ref in result.split('\n'):
        hash_ref_list = ref.split('\t')
        # symref = GITHUB_HEAD_LSREMOTE_RE.search(ref).group("symref")
        symref_match = GITHUB_HEAD_LSREMOTE_RE.search(ref)
        if (symref_match):
            symref = symref_match.group("symref")
        elif (hash_ref_list[1] == 'HEAD'):
            commit_hash = hash_ref_list[0]
        
        if (symref is not None and commit_hash is not None):
            break

    return symref, commit_hash

# returns None if not a github repo url
# ex: "https://github.com/phanan/htaccess" => "phanan/htaccess"
# ex: "google.com" => None
def github_shortname_and_path_from_awesome_url(awesome_url):
    match = GITHUB_REPO_URL_RE.match(awesome_url)
    if (not match):
        return None

    shortname = match.group("shortname")
    path = match.group("path")
    
    if (path is None):
        r = requests.get(awesome_url)
        assert r.status_code == 200
        assert r.encoding == 'utf-8'
        path = _github_find_readme_filename_in_awesome_url_html_content(r.text, shortname)

    return shortname, path

def github_git_URL_from_shortname(shortname):
    return 'https://github.com/'+ shortname +'.git'

def github_raw_url_from_shortname_symref_path(shortname, symref, path):
    return 'https://raw.githubusercontent.com/'+ shortname + '/' + symref + '/' + path