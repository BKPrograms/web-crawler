# This program will be used to discover subdomains on a web server/application
# It'll also recursively attempt to map the whole site from a general domain/starting point
import requests
import re
import argparse
import urllib.parse


def takeOptions():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--domain", dest="domain",
                        help="General domain to crawl on (Ex. google.com, http://10.0.2.6/mutillidae/).")

    results = parser.parse_args()

    if not results.domain:
        parser.error("Please enter a domain!")
    elif "http://" not in results.domain:
        results.domain = "http://" + results.domain

    return results


def extractLinksFromHrefs(url):
    # HTTP response status code of GET request to target, ex. 200 OK, 404 FNF, or 301 redirect and etc.
    response = requests.get(url)

    # HTML of the target URL stored as a string because by default it's bytes.
    # The errors="ignore" parameter essentially means ignore any errors. This actually works for us because
    # we aren't looking for the html code to be our output but rather the url itself
    htmlContent = response.content.decode(errors="ignore")

    # Since we're looking for any subdomains, links, directories, files and etc, we need to look for every href
    # part of every anchor tag to see where the links could potentially take us.
    return re.findall('(?:href=")(.*?)"', htmlContent)  # Returns all href links, but the href=" is non marking



uniqueLinks = []  # List to hold unique links and not to constantly print repeated ones


def crawl(urlToStartCrawlingFrom):
    hrefLinks = extractLinksFromHrefs(urlToStartCrawlingFrom)  # List of all href tags found in targetURL

    for currLink in hrefLinks:
        # Some of the href content won't be full links but rather relative or partial links like ./index.php or favicon.ico
        # So we can use urljoin, a built in python function, to piece together a full URL for use to use
        # If the urljoin function detects an already complete URL it won't modify it.
        currLink = urllib.parse.urljoin(base=urlToStartCrawlingFrom, url=currLink)

        # In a html page, a # does not indicate a diff webpage but rather a way to load different parts of the same webpage
        # Ex: Additional Information tab or other tabs on shopping site item pages
        if "#" in currLink:  # This helps us filter out links and really optimize our uniqueness checker
            currLink = currLink.split("#")[
                0]  # Storing everything BEFORE the hash, aka our actual link not including the #

        # This is just to filter out additional hrefs like to facebook, twitter, linkedin, etc. Essentially anything
        # that isn't part of my target url's general domain and is on a completely diff domain
        # Also checks if it isn't part of unique links
        if targetUrl in currLink and currLink not in uniqueLinks:
            uniqueLinks.append(currLink)  # Append it so it doesn't get repeatedly printed again in future
            print(currLink)  # Print the URL
            crawl(currLink)  # Recursively crawl every unique link to effectively map the whole website


if __name__ == '__main__':
    options = takeOptions()  # Take user options

    # General domain we want to crawl on
    # NOTE: Keep a / at the end to prevent runtime issues
    targetUrl = options.domain

    crawl(targetUrl)
