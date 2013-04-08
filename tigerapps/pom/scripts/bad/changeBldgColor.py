"""
April 8 2013 - joshchen@
Change the color of bldgs by:
    - reading in bldgs with representative colors
    - changing those colors
This didn't work because it's too hard to segment a building image
by color and choose the correct pixels to change.  Furthermore, it's not clear
what color those pixels should be changed to, because we need a gradient of colors
and not just a single value.
"""
import glob, sys, math
from PIL import Image
import numpy
import clustering

BLDGS_DIR = "../../static/pom/img/bldgs/"
#type, good fname, kmeans cluster choice
#THESE ARE VERY SPECIFIC TO THE FILE AND KMEANS PARAMETERS
REP_FNAMES = (
    ('bldg', BLDGS_DIR+"4-JADWG.png",2),
    ('field',BLDGS_DIR+"4-FINNE.png",2),
)

def detect_color():
    """
    Figure out the colors we need to replace...
    very hacky, because it just does a clustering of colors in a representative
    building image, and picks a color we feel looks like the color we need
    to replace
    """
    other_colors = []
    repl_colors = {}
    for name,fname,choice in REP_FNAMES:
        print name
        centers = clustering.colorz(fname, 4)
        centers = sorted(centers, key = lambda x: x[2])
        for center in centers:
            print "\t%s %s (%d)" % center
        repl_colors[name] = centers[choice][0]
        centers.pop(choice)
        other_colors += [center[0] for center in centers]
    return repl_colors['bldg'], repl_colors['field'], other_colors

OTHER = 0
BLDG = 1
FIELD = 2
def change_color(bldg_old, field_old, bldg_new, field_new, others, ext):
    print clustering.rtoh(bldg_old)
    print clustering.rtoh(field_old)
    fnames = [f for f in glob.glob(BLDGS_DIR + "*.png") if '-' not in f[-7:]]
    repls = ((bldg_old,BLDG), (field_old, FIELD))
    for fname in fnames:
        im = Image.open(fname)
        w,h = im.size
        arr = numpy.array(im)
        for row in arr:
            for pt in row:
                asgn = closest_point(repls, others, pt)
                if asgn == BLDG:
                    print 'bldg'
                    pt[:3] = bldg_new
                elif asgn == FIELD:
                    print 'field'
                    pt[:3] = field_new
        im2 = Image.fromarray(arr)
        fname_new = fname[:-4] + ext + fname[-4:]
        im2.save(fname_new)
        print fname_new
        break

                
def closest_point(repls, others, pt):
    min_dist = float('Inf')
    asgn = OTHER
    for o in others:
        #3 is for the rgb (omit alpha channel in assignment to cluster)
        dist = euclidean(o, pt[:3])
        if dist < min_dist:
            min_dist = dist
    for color,val in repls:
        dist = euclidean(color, pt[:3])
        if dist < min_dist:
            min_dist = dist
            asgn = val
    return asgn

def euclidean(p1, p2):
    return math.sqrt((sum(p1 - p2))**2)

def hexToArr(color):
    """convert html color to rgb tuple"""
    r = color[-6:-4]
    g = color[-4:-2]
    b = color[-2:]
    return tuple(int(channel,16) for channel in (r,g,b))

if __name__ == "__main__":
    bldg_old, field_old, others = detect_color()
    if len(sys.argv) == 4:
        ext = sys.argv[1]
        bldg_new = hexToArr(sys.argv[2])
        field_new = hexToArr(sys.argv[3])
        change_color(bldg_old, field_old, bldg_new, field_new, others, ext)
    else:
        print "Not changing colors"


