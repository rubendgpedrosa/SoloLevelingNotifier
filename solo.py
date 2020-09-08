import requests
import time
import http.client

#Open File and get the NUMBAH
ChapterFile = open("./chapter.txt", "r+")
PreChapterFile = ChapterFile.read().split()
ChapterNumber = int(PreChapterFile[0])
url = "URL"+str(ChapterNumber)
response = requests.get(url)
i = 1
while i:
    if ("This is an Upcoming Post." in response.text) or ("Oops! That page can" in response.text):
        print('NOT UPDATED YET')
    else:
        #Punk ass message telling them to pay!
        message = ":exclamation: :exclamation: NEW CHAPTER :exclamation: :exclamation:\n\n"+url
        print("UPDATED")
        def send( message ):
            #Where do I send the message captain?
            webhookurl = "WEBHOOK URL"
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
        i = 0
    #Let's not overload the server
    time.sleep(10)
