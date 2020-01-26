#!/usr/bin/env python3

import os, sys, pytube
from downloadmp3.vars import path

def stripExtension( t ):
   return os.path.splitext( t )[0] 


def format( s ):
    return s.strip()

def renameAll(  ):
    for f in os.listdir(path):
        if f.endswith('.mp4'):
            src = path + f
            dst = path + stripExtension(f) + '.mp3'
            os.rename(src, dst)
 
def main():

    """
    Main function.
    """
    
    if (len(sys.argv) is 3) :
        yt = pytube.YouTube(sys.argv[1])
        fname = stripExtension(sys.argv[2])
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path=path, filename=fname)
    elif len(sys.argv) is 2 and sys.argv[1] == "rename":
        renameAll()
    elif len(sys.argv) is 2:
        yt = pytube.YouTube(sys.argv[1])
        fname = format(yt.title)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path=path, filename=fname)
    else:
        print('Usage: downloadmp3 "rename"|<url> <file_name>')
    
if __name__ == '__main__':
    main()
