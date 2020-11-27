from __future__ import division

import PIL.Image as Image
import sys
import itertools

def makeShuffleThumb(inFiles, outFile):
    im = Image.new('RGB', (150,150))
    file_iter = itertools.cycle(inFiles)
    for row in range(3):
        for col in range(3):
            im.paste(Image.open(next(file_iter)).resize((50,50), Image.ANTIALIAS), [col*50, row*50, (col+1)*50, (row+1)*50])
    im.save(outFile)

if __name__ == '__main__':
    outFile = sys.argv[1]
    inFiles = sys.argv[2:]
    makeShuffleThumb(inFiles, outFile)
