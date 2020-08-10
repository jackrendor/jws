# Jack Web Scraper
JWS it's a tool that allows you to extract the text from a web page to later use it for password cracking / bruteforcing.
# Configure
Run the `configure.sh` script to create a virtualenv and install the dependencies
```bash
./configure.sh
```
# Usage
```
usage: jws.py [-h] -u URL [-js] [-l LINKS] [-e] [-H HEADER] [-o OUTPUT] [-d DEPTH]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Url of the target.
  -js, --javascript     Execute javascript when loading webpage.
  -l LINKS, --links LINKS
                        Save links into a file.
  -e, --external-links  Follow urls external to the specified domain
  -H HEADER, --header HEADER
                        Set headers separated by a semicolon
  -o OUTPUT, --output OUTPUT
                        Write the result in a file. If not set, ir redirects to stdin.
  -d DEPTH, --depth DEPTH
                        How much deep the scraper should go.

```