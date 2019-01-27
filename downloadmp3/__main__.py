#!/usr/bin/env python3

import os, sys, pytube
from downloadmp3.vars import path

def main():

    """
    Main function.
    @param argv: list of arguments (argv[0]=<youtube link> [, argv[1]=<filename>])
    """
    
    if (len(sys.argv) is not 3) :
        print("Usage: downloadmp3 <url> <filename>")
    else :    
        yt = pytube.YouTube(sys.argv[1])
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path=path, filename=sys.argv[2])
    

if __name__ == '__main__':
    main()
