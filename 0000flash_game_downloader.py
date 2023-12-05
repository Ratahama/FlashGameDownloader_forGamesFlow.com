import os
import re
import requests   # pip install requests
# from bs4 import BeautifulSoup   # pip install beautifulsoup4


# WARNING!!! make sure the game you are trying to download IS indeed an .swf format file!!!
# Otherwise, won't download. Usually old school(before 2013) flash games download just fine.
# Enter game url from gamesflow.com--> For Example:
url = 'https://www.gamesflow.com/jeux.php?id=6180'
# url = input("Enter flash url: ")


# GET SOURCE CODE:
response = requests.get(url)
if response.status_code == 200:
    page_source_code = response.text
    print(page_source_code)
else:
    print(f"Failed to retrieve the source code. Error code: {response.status_code}")
    exit()
# # CODE COULD BE MORE STABLE WITH BEAUTIFULSOUP
# soup = BeautifulSoup(page_source_code, 'html.parser')
# title_tag = soup.find('title')
# flash_game_title = title_tag.text.split('Play ')[1].split(' game - Gamesflow.com')[0] if title_tag else "unnamed_flash_game"


pattern = r'(?<=(src="))(jeux)(.*)(.swf)(?=")'
matches = re.finditer(pattern, page_source_code)

for match in matches:
    download_link = "https://www.gamesflow.com/" + match[0]
    print(f"Downloading game from link: {download_link}")

    downloading = requests.get(download_link)
    if downloading.status_code == 200:
        # Specify the local file path where you want to save the .swf file
        folder = "downloaded_swf_files"
        os.makedirs(folder, exist_ok=True)  # Create directory if it doesn't exist

        # FINDING THE NAME OF THE GAME:
        flash_game_title_pattern = r"(<title>Play )(.*?)( game - Gamesflow.com)"
        found_text = re.search(flash_game_title_pattern, page_source_code)
        if found_text:
            flash_game_title = found_text.group(2)
        else:
            flash_game_title = "unnamed_flash_game"

        # CREATING UNIQUE FILE NAME:
        filename = f"{flash_game_title}.swf"
        file_path = os.path.join(folder, filename)
        counter = 0
        while os.path.exists(file_path):  # until a unique filename is made
            filename = f"{flash_game_title}({counter}).swf"
            file_path = os.path.join(folder, filename)
            counter += 1  # flash_game, flash_game(0), flash_game(1), flash_game(2), flash_game(3)

        # SAVING the downloaded .swf file to the local machine
        with open(file_path, 'wb') as swf_file:
            swf_file.write(downloading.content)

        print(f"Download complete. Saved to: {file_path}")
        break
    else:
        print(f"Failed to download. Error code: {downloading.status_code}")


# This code is site specific. Download from gamesflow until it exists.
# In order to play your downloaded games you need to drag and drop
# the .swf file into the opened window of a FlashGamePlayer(NewGrounds player i strongly recommend)
# Have fun!


# # BASIC IDEA:
# link = ''
# response = requests.get(link)
# if requests.get(link).status_code == 200:
#     with open('downloaded_swf_files/igra.swf', 'wb') as game_file:
#         game_file.write(requests.get(link).content)


