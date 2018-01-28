import os
import re
import platform

PATTERN_RE = '^[^\._][^\.]+\.(gif|png|jpg|jpeg|tiff|bmp)$'

def find_patterns(d):
    patterns = []

    for root, dirs, files in os.walk(d):
        disp_root = os.path.relpath(root, d)
        if disp_root == '.':
            disp_root = ''
        p = []
        for f in files:
            if re.match(PATTERN_RE, f, re.I):
                name = os.path.join(disp_root, f)
                thumb = os.path.join(d, name)
                preview = os.path.join(d.replace('thumbs', 'previews'), re.sub('\.[^\.]*$','.gif',name))
                p.append({'name':name,'preview':preview,'thumb':thumb})
        patterns.append({'name':disp_root, 'patterns':p})

    # patterns[:1] = patterns[0][1]    # Don't return relpath for root dir
    # patterns = patterns[1:]
    return patterns

def find_patterns_flat(d):
    patterns = []
    print d
    for root, dirs, files in os.walk(d):
        for f in files:
            if re.match(PATTERN_RE, f, re.I):
                patterns.append(os.path.join(root, f))
    return patterns
