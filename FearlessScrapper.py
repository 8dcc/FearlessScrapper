# https://github.com/r4v10l1/FearlessScrapper

import requests
from colorama import Fore, Style
from bs4 import BeautifulSoup

#######################
ListOnly = False      # Boolean. Will download files if false
Debug = False         # Boolean. Will display aditional information if true
#######################

def InfoInput(text):
    return input(f"{Style.RESET_ALL} {Style.BRIGHT}[{Fore.BLUE}i{Style.RESET_ALL}{Style.BRIGHT}] {Fore.BLUE}{text}{Style.RESET_ALL}")
def SuccessText(text1, text2):
    print(f"{Style.RESET_ALL} {Style.BRIGHT}[{Fore.GREEN}+{Style.RESET_ALL}{Style.BRIGHT}] {Fore.GREEN}{text1}{Style.RESET_ALL}{Style.BRIGHT}{text2}{Style.RESET_ALL}")

def main():
    # Define some variables
    title_old = ""
    page_count = 0
    download_count = 1
    download_identifier = "./download/file.php?id="

    user_url = InfoInput(" URL: ")
    print()

    # Check if the user input contains "&start=" (Not the main page)
    if "&start=" in user_url:
        user_url = user_url.split("&start=")[0]

    while True:     # Loop until you reach the last page
        URL = user_url + "&start=" + str(page_count * 15)       # The URL counts posts, not pages, so you multiply the page * 15 posts per page.
        r = requests.get(URL, allow_redirects=False)            # Get request
        soup = BeautifulSoup(r.text, features="html.parser")    # For the title

        title = soup.title
        if title_old == title:      # If two titles are the same, there are no pages left
            print()
            SuccessText("Done! Exiting...", "")
            exit(1)
        title_old = title

        if Debug:
            print(" URL: " + URL)
            print(" TITLE: " + title)

        for line in r.text.split("\n"):
            # Found an attachment
            if download_identifier in line:
                result = "https://fearlessrevolution.com" + line.split("href=\".")[1].split("&")[0]
                SuccessText("Result found: ", result)
                
                # If you want to download it
                if not ListOnly:
                    downloader = requests.get(result, allow_redirects=False)                # Get the file
                    with open(str(download_count) + ".ct", "w", encoding="utf-8") as w:     # Write the file with encoding
                        w.write(downloader.text)
                    download_count += 1     # For the file names

        page_count += 1

main()
