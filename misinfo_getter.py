import re

import requests
import json
import os
from numpy import loadtxt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

api_key = "Secret"
misinformation_keywords = loadtxt("fakeness.dat", comments="#", delimiter=",", unpack=False, dtype='str')


class youtubeInfo:

    def __init__(self):
        self.video_title = None
        self.video_description = None
        self.comments = None
        self.misinformation_comments = None
        self.percentage = None
        self.isTitleMisinfo = None
        self.isDescriptionMisinfo = None

def token(input):

    return word_tokenize(input)



def scrape_youtube(video_id):
    # use to download metadata from YouTube
    url = 'https://www.googleapis.com/youtube/v3/videos?id=' + video_id + '&key=' + api_key + '&part=snippet,contentDetails,statistics,status'
    # https://www.googleapis.com/youtube/v3/commentThreads?key={your_api_key}&textFormat=plainText&part=snippet&videoId={video_id}&maxResults=100&pageToken={nextPageToken}

    response = requests.get(url)
    commentURL = 'https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=1000&moderationStatus=published&order=relevance&textFormat=plainText&videoId=' + video_id + '&key=' + api_key

    commentResponse = requests.get(commentURL)

    # parse the JSON data
    data = json.loads(response.text)
    commentData = json.loads(commentResponse.text)

    x = youtubeInfo()

    # extract info from data
    x.video_title = data['items'][0]['snippet']['title']
    x.video_description = data['items'][0]['snippet']['description']



    try:
        x.comments = commentData['items']
    except KeyError:
        x.comments = None

    # create an empty list to store flagged comments
    x.misinformation_comments = []

    # sort through comments and send through to find misinformation keywords
    if x.comments is not None:
        for comment in x.comments:
            com = comment['snippet']['topLevelComment']['snippet'][
                'textDisplay']
            identify_misinformation(com, x)

    # find percentage of comments that were flagged
    x.percentage = calculate_percentage(x)

    print(x.percentage)
    return x.percentage


def identify_misinformation(comment, info):
    # list of keywords to flag possible misinformation

    # check to see if keywords match comments, add to list if there is a match

    for keyword in misinformation_keywords:
        #print(len(keyword))
        if keyword[0] in comment:
            info.misinformation_comments.append(comment)
            return True
    return False


def calculate_percentage(youtubeInfo):
    # find the number of comments flagged
    number_misinformation_comments = len(youtubeInfo.misinformation_comments)
    # calculate percentage

    percentage = (number_misinformation_comments / 1000)
    # print(str(percentage) +"comments")
    tokenTitle = token(youtubeInfo.video_title)
    tokenDescription = token(youtubeInfo.video_description)

    #print(str(tokenTitle))
    #print(str(tokenDescription))
    break_out_flag = False

    for keyword in misinformation_keywords:
        for titleword in tokenTitle:
            if titleword in keyword[0]:
                #print(keyword[0])
                percentage += 0.25
                break_out_flag = True
                break

        if break_out_flag:
            break
    break_out_flag = False
    # print(str(percentage) + "title")
    for keyword in misinformation_keywords:
        for tokenword in tokenDescription:
            if tokenword in keyword[0] :
                #print(keyword[0])
                break_out_flag = True
                percentage += 0.25
                break
        if break_out_flag:
            break

    # print(str(percentage) + "description")
    print(len(misinformation_keywords))
    return percentage
