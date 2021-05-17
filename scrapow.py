# Author: Pratyaksha Beri
# Github: https://github.com/Shad0wMazt3r
# Version: 2.0
import requests
import os
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re
import pickle
import time
import socket
import subprocess
# Setting the Logo and printing it
logo = """ 
 ___   ___  ____    __    ____  _____  _    _ 
/ __) / __)(  _ \  /__\  (  _ \(  _  )( \/\/ )
\__ \( (__  )   / /(__)\  )___/ )(_)(  )    ( 
(___/ \___)(_)\_)(__)(__)(__)  (_____)(__/\__)
"""
print(logo)
# inputting the url for scraping
website = input("Enter a URL:")

def website_url_formatting(website):
    # This function formats the URL and sets up the proxy
    # .onion websites can be accessed at clear net by adding .ws at the end of the url
    # .onion.ws is a proxy which allows you to access dark web without connecting to it via tor
    if website.endswith("/"):
        website = website[:-1]
    if website.endswith(".ws"):
        pass
    elif website.endswith(".onion"):
        scrape_command = "curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s "+website
        r = subprocess.check_output(scrape_command, shell=True)
        # print(r)
        source = r.decode()
        page_soup = soup(r, "html.parser")
        # Getting title of the website
        title = page_soup.title
        title = str(title)
        # Removing the Title tags to just get the Main title
        # for example: <title>Hello World</title>
        # would get reduced to "Hello World"
        title = title.replace("<title>", "")
        title = title.replace("</title>", "")
        # Exracting the description of the webpage
        desc = page_soup.description
        desc = str(desc)
        #checks if title and/or description is empty
        if title == "":
            print("No Title Could Be Found!")
        else:
            print(title)
        if desc == "None":
            print("No Description Could Be Found!")
        else:
            print(desc)
        # Finds all urls
        urls = re.findall(b'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r)
        # saves urls to links.txt
        with open('links.txt', mode="w+") as file_object:
            print(*urls , sep="\n", file=file_object)
        # uses pickle to save file as CSV file
        with open('list.csv', 'wb') as filehandle:
            pickle.dump(urls, filehandle)
        print("Links saved to links.txt and to list.csv")
        # tries Checks for website's purpose by finding certain keywords in text
        if "search" in source:
            print("Search engine")
        else:
            pass
        if "buy" in source:
            print("Selling")
        else:
            pass
        if "hacking" in source:
            print("Hacking")
        else:
            pass
        if "hire" in source:
            print("Hiring services")
        else:
            pass
    if website.startswith("http://") or website.startswith("https://"):
        pass
    if not website.startswith("https://") or not website.startswith("http://"):
        website = "https://"+website
website_url_formatting(website)
def scrape(website):
    # This function scrapes the website and does the main thing
    # Sets the user agent. User agent is basically browser info. 
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    # Opens links.txt in read and write mode, creates if doesn't exist already
    # file_object is the variable name assigned to it
    with open('links.txt', mode="w+") as file_object:
        # Makes a request to the website and sends the user agent as header
        try:
            r = requests.get(website, headers={'User-Agent':user_agent})
            r2 = uReq(website)
        except:
            website = "https://"+website
            r = requests.get(website, headers={'User-Agent':user_agent})
            r2 = uReq(website)
        page_html = r2.read()
        # Souping the website using beautiful soup.
        page_soup = soup(page_html, "html.parser")
        # Getting title of the website
        title = page_soup.title
        title = str(title)
        # Removing the Title tags to just get the Main title
        # for example: <title>Hello World</title>
        # would get reduced to "Hello World"
        title = title.replace("<title>", "")
        title = title.replace("</title>", "")
        # Exracting the description of the webpage
        desc = page_soup.description
        desc = str(desc)
        #checks if title and/or description is empty
        if title == "":
            print("No Title Could Be Found!")
        else:
            print(title)
        if desc == "None":
            print("No Description Could Be Found!")
        else:
            print(desc)
        # Finds all urls
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r.text)
        # saves urls to links.txt
        print(*urls , sep="\n", file=file_object)
        # uses pickle to save file as CSV file
        with open('list.csv', 'wb') as filehandle:
            pickle.dump(urls, filehandle)
        print("Links saved to links.txt and to list.csv")
        # tries Checks for website's purpose by finding certain keywords in text
        if "search" in r.text:
            print("Search engine")
        else:
            pass
        if "buy" in r.text:
            print("Selling")
        else:
            pass
        if "hacking" in r.text:
            print("Hacking")
        else:
            pass
        if "hire" in r.text:
            print("Hiring services")
        else:
            pass
scrape(website)

def autoscan(website):
    # This is one of the older scripts that I wrote to automate the Recon Process
    # You can find it as autoscan in my github
    # It first saves the website as site.html for future reference
    cmd = ('curl -oL site.html '+website)
    os.system(cmd)
    def clear():
        # This is a simple function to clear the terminal
        cmd2 = ('clear')
        os.system(cmd2)
    clear()
    print("site saved as site.html")
    print("Doing reverse DNS lookup")
    # nslookup in Kali is a tool to simplify the reverse DNS lookup
    cmd3 = ('nslookup '+website)
    os.system(cmd3)
    def wait():
        # Simple function for waiting for the user's input and asking for continuation
        # userip is the user input
        userip = input("Should we continue? (y/n):")
        if userip == "y":
            pass
        else:
            exit()
    wait()
    clear()
    cmd5 = ('nmap -O '+website+' | grep OS')
    os.system(cmd5)
    wait()
    clear()
    # Doing some nmap and whois lookup
    cmd6 = ('nmap -p- '+website)
    os.system(cmd6)
    wait()
    clear()
    cmd7 = ('nmap --script=http-title '+website)
    os.system(cmd7)
    wait()
    clear()
    cmd8 = ('whois '+website)
    os.system(cmd8)
scan = input("Would You Like to Do a basic scan (y/n)? (Kali Linux only) (Clearnet Sites only) :")   
if scan =="y":
    autoscan(website)
else:
    exit()
