"""
Module with functions related to finding and downloading videos from youtube.
"""
import urllib.request
import youtube_dl
from bs4 import BeautifulSoup
from pathlib import Path


def get_video_url(video_name):
    """
    Searches for the video on youtube and returns the url of the first video found.

    :param video_name: The name of the video that we search for.
    :return: The URL of the first video found when searching for the given video name.
    """

    # Parsing the given video name into a youtube search URL.
    query = urllib.parse.quote(video_name)
    url = "https://www.youtube.com/results?search_query=" + query

    # Requesting and saving the html from the page given when opening the above URL.
    response = urllib.request.urlopen(url)
    html = response.read()

    # Creating a html parser we can use to parse through the html code from the youtube page.
    soup = BeautifulSoup(html, 'html.parser')

    # Parsing through the html and searching for the first video element on the search result page, signified by the
    # CSS class "yt-uix-tile-link".
    return f"https://www.youtube.com{soup.find(class_='yt-uix-tile-link')['href']}"


def download_mp3(url, save_folder):
    """
    Downloads the youtube video from the url as an mp3 file and saves it to the given folder.

    :param url: The youtube url of the video from which the audio will be downloaded.
    :param save_folder: The folder to which the mp3 file will be saved.
    :return: None
    """
    # Creating the save folder if it does not already exist.
    Path(save_folder).mkdir(parents=True, exist_ok=True)

    # Setting the options for the youtube downloader.
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": save_folder + "%(id)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    # Downloading the audio from the given url using the above specified options.
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


download_mp3(get_video_url("hello world"), "audio_files/")