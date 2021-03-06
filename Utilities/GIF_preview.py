from __future__ import division

import PIL.Image as Image
import sys
import os
import tempfile
import shutil

def makePreview(inFile,outFile=None):
    '''Make an animated .gif preview of an image for the Bemis100'''
    if outFile is None:
        outFile = 'preview_'+inFile
    tempFolder = tempfile.mkdtemp()
    im = Image.open(inFile)
    (width,height) = im.size
    for i in range(min(height,150)):
        out = im.crop([0,i,width,i+1])
        out.resize((150,1),Image.ANTIALIAS).save(os.path.join(tempFolder,format(i,'05d')+'.gif'))
    command ='convert '+'-delay 5 -loop 0 '+os.path.join(tempFolder,'*.gif')+' ' + outFile
    print(command)
    os.system(command)
    shutil.rmtree(tempFolder)

if __name__=='__main__':
    inFile = sys.argv[1]
    outFile = sys.argv[2]
    makePreview(inFile, outFile)
