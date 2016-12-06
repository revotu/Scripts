import os.path
import urllib

import openpyxl
from openpyxl.reader.excel import load_workbook

def checkVideoLink(videoLink):
    videoID = videoLink.split('/')[-1]
    videoThumbnail = 'https://i.ytimg.com/vi/%s/maxresdefault.jpg' % (videoID)
    response = urllib.urlopen(videoThumbnail)
    status = response.getcode()
    if status == 200:
        return True
    else:
        return False

if __name__ == "__main__":
    wb = load_workbook('enki-video.xlsx')
    ws = wb.active
    for index in range(1,ws.get_highest_row() + 1):
        videoLink = ws.cell(row = index,column = 2).value
        ws.cell(row = index,column = 3).value = checkVideoLink(videoLink)
        print index,videoLink
        wb.save('enki-video.xlsx')