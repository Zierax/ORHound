#!/usr/bin/env python

# Open Redirect Hound (ORHound)
# This script is distributed under the GNU GPL v3 license.

import sys
import requests
import random
from bs4 import BeautifulSoup

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    print(Colors.WARNING + """
 ___  ____  _   _                       _ 
 / _ \|  _ \| | | | ___  _   _ _ __   __| |
| | | | |_) | |_| |/ _ \| | | | '_ \ / _` |
| |_| |  _ <|  _  | (_) | |_| | | | | (_| |
 \___/|_| \_\_| |_|\___/ \__,_|_| |_|\__,_|
""" + Colors.ENDC)
    print(Colors.OKGREEN + "ORHound v1.1 - Open Source Project\nAuthor: Robotshell\nGithub: https://github.com/robotshell\n" + Colors.ENDC)

def dork(domain, enable_save):
    """Performs Google Dork scraping to find Open Redirects for a given domain."""
    print(Colors.OKCYAN + "Starting Google Dork scraping to find Open Redirects for " + Colors.FAIL + domain + Colors.ENDC)
    
    with open("user_agent.txt") as ua:
        user_agents = ua.readlines()
    
    query = f'inurl%3A%3D%253dhttp+site%3A{domain}'
    url = f"https://google.com/search?q={query}"
    headers = {"user-agent": random.choice(user_agents).strip()}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                print(Colors.WARNING + link + Colors.ENDC)
                if enable_save:
                    save_to_file(domain, link)
    else:
        print(Colors.FAIL + "Request failed for " + domain + Colors.ENDC)

def save_to_file(domain, link):
    """Saves the found link to a file named after the domain."""
    filename = f"{domain}_results.txt"
    with open(filename, 'a') as f:
        f.write(link + '\n')
    print(Colors.OKGREEN + f"Saved result to {filename}" + Colors.ENDC)

def process_domains(domains, enable_save):
    """Processes each domain from the list."""
    for domain in domains:
        domain = domain.strip()
        if domain:
            dork(domain, enable_save)

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print(Colors.FAIL + "ERROR: No domain or parameters found" + Colors.ENDC)
        return
    
    enable_save = False
    domains = []

    # Argument handling
    for arg in sys.argv[1:]:
        if arg in ("-h", "--help"):
            print(Colors.BOLD + "HELP SECTION:" + Colors.ENDC)
            print("Usage:" + Colors.OKCYAN + "\torhound.py <domain> OR -f <file>" + Colors.ENDC)
            print("-h, --help" + Colors.OKCYAN + "\tDisplay this help message" + Colors.ENDC)
            print("-v, --version" + Colors.OKCYAN + "\tShow version" + Colors.ENDC)
            print("-s, --save" + Colors.OKCYAN + "\tEnable save output to file" + Colors.ENDC)
            print("-f, --file <path>" + Colors.OKCYAN + "\tSpecify a file containing multiple domains" + Colors.ENDC)
            return
        elif arg in ("-v", "--version"):
            print("ORHound v1.1")
            return
        elif arg in ("-s", "--save"):
            enable_save = True
        elif arg in ("-f", "--file"):
            try:
                filepath = sys.argv[sys.argv.index(arg) + 1]
                with open(filepath, 'r') as f:
                    domains = f.readlines()
            except (IndexError, FileNotFoundError):
                print(Colors.FAIL + "ERROR: File not specified or not found." + Colors.ENDC)
                return
        else:
            domains.append(arg)
    
    if domains:
        process_domains(domains, enable_save)
    else:
        print(Colors.FAIL + "ERROR: No domains found to process" + Colors.ENDC)

if __name__ == "__main__":
    main()
