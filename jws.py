#!/usr/bin/env python3
from requests_html import HTMLSession
from sys import stderr
import argparse
from bs4 import BeautifulSoup, Comment
import string

MAIN_DOMAIN = ""
analyzed_links = []


def parse_them_all():
    def depth_level(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
        return ivalue
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Url of the target.", required=True)
    parser.add_argument("-js", "--javascript", help="Execute javascript when loading webpage.", action='store_true')
    parser.add_argument("-l", "--links", help="Save links into a file.")
    parser.add_argument("-e", "--external-links", help="Follow urls external to the specified domain",
                        action='store_true', default=False)
    parser.add_argument("-H", "--header", help="Set headers separated by a semicolon")
    parser.add_argument("-o", "--output", help="Write the result in a file. If not set, ir redirects to stdin.")
    parser.add_argument("-d", "--depth", help="How much deep the scraper should go.", type=depth_level, default=1)
    return parser.parse_args()


def extract_text(data):
    soup = BeautifulSoup(data, "html.parser")  # create a new bs4 object from the html data loaded
    [x.decompose() for x in soup.find_all('script')]
    [x.decompose() for x in soup.find_all('style')]
    [x.decompose() for x in soup.find_all('meta')]
    [x.decompose() for x in soup.find_all('noscript')]
    [x.decompose() for x in soup.find_all(text=lambda text: isinstance(text, Comment))]
    result = soup.get_text()
    return result


def clean_string(data):
    for char in string.punctuation:
        data = data.replace(char, " ")
    data = " ".join(data.split())
    return data


def set_header(arg):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/58.0.3029.110 Safari/537.36'}
    if not arg:
        return headers
    for header in arg.split(";"):
        var_name, var_data = header.split(":")
        headers[var_name] = var_data
    return headers


def scrape_this(session, url, headers, javascript, external):
    if not url.startswith("https://") and not url.startswith("http://"):
        return None, None
    if not external:
        if not url.startswith("https://"+MAIN_DOMAIN) and not url.startswith("http://"+MAIN_DOMAIN):
            return None, None
    r = session.get(url, headers=headers)
    print("Scraping", url, file=stderr)
    if javascript:
        r.html.render()

    result = r.html.text
    collected_links = list(r.html.absolute_links)

    result = extract_text(result)
    result = clean_string(result)
    return result, collected_links


def remove_duplicates(data):
    data = "\n".join(set(data.split(" ")))
    data = "\n".join([ll.rstrip() for ll in data.splitlines() if ll.strip()])
    return data


def recursive_scrape(session, url, headers, javascript, depth, external):
    data, links = scrape_this(session, url, headers, javascript, external)
    if depth == 1:
        return data, links
    data_return = ""
    list_return = []
    if not links:
        return "", []
    for link in links:
        global analyzed_links
        if link in analyzed_links or link is None:
            continue
        analyzed_links += [link]
        for_data, for_list = recursive_scrape(session, link, headers, javascript, depth-1, external)
        data_return += for_data + " " if for_data else ""
        list_return += for_list if for_list else []
    return data + " " + data_return, links + list_return


def main():
    args = parse_them_all()
    session = HTMLSession()
    headers = set_header(args.header)
    print("Following external links:", args.external_links, file=stderr)
    global MAIN_DOMAIN
    MAIN_DOMAIN = args.url.replace("https://", "").replace("http://", "")
    if "/" in args.url:
        MAIN_DOMAIN = MAIN_DOMAIN.split("/")[0]

    data, links = recursive_scrape(session=session, url=args.url, headers=headers,
                                   javascript=args.javascript, depth=args.depth, external=args.external_links)

    data = remove_duplicates(data)

    if args.output:
        with open(args.output + ".wordlist", "w") as f:
            f.write(data)
    else:
        print(data)

    if args.links:
        with open(args.links + ".urls", "w") as f:
            for link in links:
                f.write(link+"\n")

if __name__ == "__main__":
    main()
