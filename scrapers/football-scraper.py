from bs4 import BeautifulSoup
import requests
import json
import re

url = "https://www.youtube.com/feeds/videos.xml?user=NFL"
html = requests.get(url)
soup = BeautifulSoup(html.text, "lxml")

videos = []

for entry in soup.find_all("entry"):
    video = {}
    for title in entry.find_all("title"):
        video_name = title.text
        video["name"] = video_name
    for link in entry.find_all("link"):
        # Get the video ID from the query parameter
        link = link['href']
        video["url"] = link
        
        video_id = link.split('v=')[1]
        video['youtubeId'] = video_id

    for name in entry.find_all("name"):
        video["author"] = name.text
        # print(name.text)
    for pub in entry.find_all("published"):
        video["published"] = pub.text
        # print(pub.text)
    for description_tag in entry.find_all("media:description"):
        description_text = description_tag.text.replace('\n', ' ')
        description_text = description_text.replace("Never miss a moment with the latest news, trending stories and highlights to bring you closer to your favorite players and teams. Download now: https://app.link.nba.com/NBAapp", "")
        description_text = description_text.strip()
        video["description"] = description_text
    video['sport'] = 'Basketball'
    # print('video=', video)

    videos.append(video)


with open("football.json", "w") as json_file:
    json.dump(videos, json_file, indent=2)


