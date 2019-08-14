# coding=utf-8
import time
import http.client
import sys
from re import search
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

import requests, re
from contextlib import closing

CHUNKSIZE = 1024

#Rewrite title name.
retitle = re.compile("<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
buffer = ""

#Open File and get the NUMBAH
ChapterFile = open("/PATH/TO/chapter.txt", "r+")
PreChapterFile = ChapterFile.read().split()
ChapterNumber = int(PreChapterFile[0])

#Split website URL for better merging with number chapter.
urlstart = "START OF THE URL"
urlrest = "REST OF THE URL"

#BECOME ONE
url = urlstart+str(ChapterNumber)+urlrest

htmlp = HTMLParser()
with closing(requests.get(url, stream=True)) as res:
    for chunk in res.iter_content(chunk_size=CHUNKSIZE, decode_unicode=True):
        buffer = "".join([buffer, chunk])
        match = retitle.search(buffer)
        url = urlstart+str(ChapterNumber)+urlrest
        print(url)
        if match:
            urltext = htmlp.unescape(match.group(1))
            if search("200", str(requests.get(url, stream=True))) == None:
                print("NOT UPDATED")
            else:
                #Punk ass message telling them to pay!
                message = ":exclamation: :exclamation: NEW CHAPTER :exclamation: :exclamation:\n\n"+url
                print("UPDATED")
                def send( message ):

                        #Where do I send the message captain?
                        webhookurl = "DISCORD CHANNEL WEBHOOK"
                        formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------:::BOUNDARY:::--"

                        #Connection being done
                        connection = http.client.HTTPSConnection("discordapp.com")
                        connection.request("POST", webhookurl, formdata, {
                            'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
                            'cache-control': "no-cache",
                            })
                        response = connection.getresponse()
                        result = response.read()
                        result.decode("utf-8")

                # send the messsage and print the response
                print(send(message))

                #Increment chapter number and save it to file.
                ChapterNumber = ChapterNumber + 1
                ChapterFile.seek(0)
                ChapterFile.write(str(ChapterNumber))
                ChapterFile.truncate()

            #Let's not overload the server
            time.sleep(10)

