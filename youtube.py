"""
Module with functions related to finding and downloading videos from youtube.
"""
import urllib.request
import youtube_dl
from bs4 import BeautifulSoup
from pathlib import Path
import os


def get_video_title_url(video_name):
    """
    Searches for the video on youtube and returns the title and url of the first video found.

    :param video_name: The name of the video that we search for.
    :return: The title and URL of the first video found when searching for the given video name.
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
    video = soup.find(class_='yt-uix-tile-link')

    # Wrapping in a try-except to handle the rare cases where an error causes "video" to be None. Since the problem is
    # not correlated with the video name we simply call the function again with the same parameter.
    try:
        return video["title"], "https://www.youtube.com" + str(video["href"])
    except TypeError:
        print("Could not find a URL for: " + video_name + "\nTrying again")
        return get_video_title_url(video_name)


def download_mp3(url, save_folder):
    """
    Downloads the youtube video from the url as an mp3 file and saves it to the given folder. If the video already
    exists in the folder it is not re-downloaded.

    :param url: The youtube url of the video from which the audio will be downloaded.
    :param save_folder: The folder to which the mp3 file will be saved.
    :return: Returns the file name of the video that was downloaded.
    """
    # Creating the save folder if it does not already exist.
    Path(save_folder).mkdir(parents=True, exist_ok=True)

    # Setting the options for the youtube downloader.
    ydl_opts = {
        "format": "bestaudio/best",
        'noplaylist': True,
        'nocheckcertificate': True,
        'cachedir': False,
        "outtmpl": save_folder + "%(id)s.%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    # Downloading the audio from the given url using the above specified options.
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        filepath = save_folder + info["id"] + "." + info["title"] + ".mp3"

        # If the file does not already exist in the download folder we download it.
        if not os.path.isfile(filepath):
            ydl.download([url])

        return filepath


def get_youtube_video(video_name, save_folder):
    """
    Searches youtube for the video name and downloads the audio from the first video found.

    :param video_name: The search query that will be used to search for the video on youtube.
    :param save_folder: The folder to which the mp3 file will be saved.
    :return: Returns the file name of the video that was downloaded.
    """
    url = get_video_title_url(video_name)

    return download_mp3(url, save_folder)
