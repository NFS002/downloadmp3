#!/usr/bin/env python3

"""
Download mp3. Extract a wav or mp3 file from a youtube video url

Usage:
  dp3 download <url> --dir=<download_path> [--name=<download_file_name>] [--format=<format>]
  dp3 search <search_string> --dir=<search_path>
  dp3 -h | --help
  dp3 --version

Options:
  -h --help                     Show this screen.
  --version                     Show version.
  --dir=<path>                  Path to output directory where file is saved
  --name=<download_file_name>   The name of the downloaded file. Defaults to the title of the video
  --format=<format>             Format of output file, wav, mp4, or mp3. [default: mp3]
"""

import os, sys, pytube, re, subprocess
from urllib import parse
from docopt import docopt

import fcntl, termios, struct
from version import VERSION

def stripExtension( f ):
    return os.path.splitext( f )[0]

def convert( stream, handle, format ):
    if format != 'mp4':
        print(f"Converting to {format} and removing mp4...")
        file_path = str(handle)
        new_file_path = stripExtension( file_path ) + '.' + format
        ffmpeg = ["ffmpeg", "-i", file_path, new_file_path]
        p = subprocess.Popen(ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_data, stderr_data = p.communicate()
        if p.returncode != 0:
            print(f"Converting to {format} failed: ", str(stdout_data), str(stderr_data))
        else:
            os.remove(file_path)
    print("Download complete")
    

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


def search( path, substr ):
    allfiles = os.listdir(path)
    print("Searching " + str(len(allfiles)) +  " file(s)...")
    matchingFiles = [f for f in allfiles if re.search( substr, f, re.IGNORECASE) ]
    print("Found " + str(len(matchingFiles)) +  " file(s)")
    for i, f in enumerate(matchingFiles):
        print("{}. {}".format(i + 1,f))

def isPlaylistUrl( url ):
    query_def = parse.parse_qs( parse.urlparse( url).query )
    return 'list' in query_def


def downloadFirstStream( url, path, title, format):
    if isPlaylistUrl( url ):
        print("Cannot download video from a playlist url. Please download from the individual video url instead")
        return
    if title is None:
        title = yt.title
    yt = pytube.YouTube( url )
    yt.register_on_complete_callback(lambda s, h: convert(s, h, format) )
    yt.register_on_progress_callback(printProgressBar)
    stream = yt.streams.filter(only_audio=True).first()
    print("Downloading: %s" % title.strip() )
    stream.download(output_path=path, filename=title.strip() )


def main():
    args = docopt(__doc__, version=VERSION)
    if args['search'] is True:
        search( args['--dir'], args['<search_string>'] )
    elif args['download'] is True:
        downloadFirstStream( args['<url>'], args['--dir'], args['--name'], args['--format'] )
    
if __name__ == '__main__':
    main()