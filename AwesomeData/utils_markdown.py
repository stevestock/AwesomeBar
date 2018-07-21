import re
import utils_github
import concurrent.futures
import mistune

#from https://stackoverflow.com/a/9268827
MD_LINK_PATTERN = r"""
    (?<!!)          #not an image
    \[                        # Literal opening bracket
        (?P<text>[^\[\]]+)    # One or more characters other than close bracket
    \]                        # Literal closing bracket
    \(
        \s*                   # Literal opening parenthesis
        (?P<url>\S+(?=[\)"])) # One or more characters other than close parenthesis
        \s*
        (?P<title>".*")?
        \s*
    \)                        # Literal closing parenthesis
    """

MD_LINK_RE = re.compile(MD_LINK_PATTERN, re.X)

def md_print_test(md_content):
    markdown = mistune.Markdown()
    print(markdown(md_content))

def getListOfGithubLinksfromString(s):
    links = []

    for match in MD_LINK_RE.finditer(s):
        url = match.group("url")
        print(url)
        isRefLink = url.startswith("#")
        shortNameOrNone = utils_github.github_shortname_and_path_from_awesome_url(url)
        if (not isRefLink and shortNameOrNone):
            groupdict = match.groupdict()
            groupdict["shortname"] = shortNameOrNone
            links.append(groupdict)
    return links