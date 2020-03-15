#!/usr/bin/env python3

import os, sys, pytube
from downloadmp3.vars import path
import re

def stripExtension( f ):
    return os.path.splitext( f )[0]

def renameToMp3( stream, handle ):
    file_path = handle.name
    file_name = os.path.basename( file_path )
    new_file_path = stripExtension( file_path ) + ".mp3"
    os.rename(file_path, new_file_path)
    

def printProgressBar(stream, chunk, handle, bytes_remaining, suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        value   - Required  : current value(Int)
        total       - Required  : total iterations (Int)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = stream.filesize
    value = total - bytes_remaining
    percent = ("{0:." + str(decimals) + "f}").format(100 * (value / float(total)))
    filledLength = int(length * value // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r|%s| %s%% %s' % (bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if value == total: 
        print()


def search( substr ):
    allfiles = os.listdir(path)
    print("Searching " + str(len(allfiles)) +  " file(s)...")
    matchingFiles = [f for f in allfiles if re.search( substr, f, re.IGNORECASE) ]
    print("Found " + str(len(matchingFiles)) +  " file(s)")
    for i, f in enumerate(matchingFiles):
        print("{}. {}".format(i + 1,f))


def downloadFirstStream( url ):
    yt = pytube.YouTube( url )
    title = yt.title.strip()
    yt.register_on_complete_callback(renameToMp3)
    yt.register_on_progress_callback(printProgressBar)
    stream = yt.streams.filter(only_audio=True).first()
    print("Downloading: %s" % title )
    stream.download(output_path=path, filename=title )
 
def downloadFirstStreamWithTitle( url, title ):
    yt = pytube.YouTube( url )
    yt.register_on_complete_callback(renameToMp3)
    yt.register_on_progress_callback(printProgressBar)
    stream = yt.streams.filter(only_audio=True).first()
    print("Downloading: %s" % title.strip() )
    stream.download(output_path=path, filename=title.strip() )


def main():

    """
    Main function.
    """
    
    if len(sys.argv) is 3 and sys.argv[1] == "search":
        search( sys.argv[2] )
    elif (len(sys.argv) is 3) :
        downloadFirstStreamWithTitle( sys.argv[1], sys.argv[2] )
    elif len(sys.argv) is 2:
        downloadFirstStream( sys.argv[1] )
    else:
        print('Usage: downloadmp3 search <regex>|[url] <file_name>')
    
if __name__ == '__main__':
    main()
