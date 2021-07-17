import sys
sys.path.append("..")

import os
import re
import json

import network.myhtml as myhtml



def getMP4ByBid(video_id, ffmpeg_config="-c:v copy -c:a aac -strict experimental"):
    pageUrl = "https://www.bilibili.com/video/" + video_id
    htmlText = myhtml.getRequestsText(pageUrl, pageUrl)
    urlJson = json.loads(re.findall(
        '<script>window\.__playinfo__=(.*?)</script>', htmlText)[0])

    videoUrl = urlJson['data']['dash']['video'][0]['backupUrl'][0]
    audioUrl = urlJson['data']['dash']['audio'][0]['backupUrl'][0]

    print("Downloading...")

    audioFile = myhtml.getRequestsContent(audioUrl, pageUrl)
    with open('../../tmp/audio_'+video_id+'.mp3', 'wb') as f:
        f.write(audioFile)
    videoFile = myhtml.getRequestsContent(videoUrl, pageUrl)
    with open('../../tmp/video_'+video_id+'.mp4', 'wb') as f:
        f.write(videoFile)

    os.system('ffmpeg -y -i ../../tmp/video_'+video_id+'.mp4 -i ../../tmp/audio_' +
              video_id+'.mp3 ' + ffmpeg_config + ' ../../data/media/'+video_id+'.mp4')
    print("Succeed! :)")

    # 此处还应当删除临时文件

if __name__ == "__main__":  
    getMP4ByBid("BV1sk4y1k73b")
