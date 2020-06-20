#!/usr/bin/env python3

import os, sys, pytube, re, subprocess
from urllib import parse

import fcntl, termios, struct
from downloadmp3.vars import path

def stripExtension( f ):
    return os.path.splitext( f )[0]

def convertToMp3( stream, handle ):
    print("Converting to mp3 and removing mp4...")
    file_path = str(handle)
    new_file_path = stripExtension( file_path ) + ".mp3"
    ffmpeg = ["ffmpeg", "-i", file_path, new_file_path]
    p = subprocess.Popen(ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    if p.returncode != 0:
        print("Error: converting to mp3 failed.")
    else:
        os.remove(file_path)
        print("Download completed successfully")
    

def printProgressBar(stream, chunk, bytes_remaining, decimals = 1, fill = '█', printEnd = "\r"):
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

    def terminal_size():
        h, w, hp, wp = struct.unpack('HHHH',
            fcntl.ioctl(0, termios.TIOCGWINSZ,
            struct.pack('HHHH', 0, 0, 0, 0)))
        return w, h

    w, h = terminal_size()
    total = stream.filesize
    value = total - bytes_remaining
    percent = ("{0:." + str(decimals) + "f}").format(100 * (value / float(total)))
    length = w - len(percent) - 5
    filledLength = int(length * value // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r|%s| %s%% ' % (bar, percent), end = printEnd)
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

def isPlaylistUrl( url ):
    query_def = parse.parse_qs( parse.urlparse( url).query )
    return 'list' in query_def


def downloadFirstStream( url ):
    if isPlaylistUrl( url ):
        print("Cannot download video from a playlist url. Please download from the individual video url instead")
        return
    yt = pytube.YouTube( url )
    title = yt.title.strip()
    yt.register_on_complete_callback(convertToMp3)
    yt.register_on_progress_callback(printProgressBar)
    stream = yt.streams.filter(only_audio=True).first()
    print("Downloading: %s" % title )
    stream.download(output_path=path, filename=title )
 
def downloadFirstStreamWithTitle( url, title ):
    if isPlaylistUrl( url ):
        print("Cannot download video from a playlist url. Please download from the individual video url instead")
        return
    yt = pytube.YouTube( url )
    yt.register_on_complete_callback(convertToMp3)
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