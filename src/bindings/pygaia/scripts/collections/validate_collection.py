#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, yaml, glob
from os.path import join, exists, basename
from gaia2.classification import GroundTruth

def usage():
    print '%s base_dir' % sys.argv[0]
    sys.exit(1)


def validate(basedir):
    # let's start with some basic check
    print 'Checking basic directory layout...'
    if not exists(basedir):
        raise Exception('The specified base directory does not exist')

    # check required metadata files are there and that they're valid
    configFile = join(basedir, 'metadata', 'config.yaml')
    if not exists(configFile):
        raise Exception('config.yaml could not be found in the metadata/ folder')

    config = yaml.load(open(configFile).read())
    if 'version' not in config:
        raise Exception('config.yaml doesn\'t have a version number')


    # check that the specified audioFormats correspond to the audio/ subfolders
    print 'Checking available audio formats...'
    audioFormats = config['audioFormats']
    if not audioFormats:
        raise Exception('audioFormats not specified in config.yaml')

    audioFolders = [ basename(f) for f in glob.glob(join(basedir, 'audio', '*')) ]

    if len(audioFolders) != len(audioFormats):
        raise Exception('Some audio folders are not described in the audioFormats section of the config.yaml')

    print 'Found formats:', str(audioFolders)

    # check the audio formats are valid, in particular that they have a valid filelist
    for format, desc in audioFormats.items():
        print "\nChecking format '%s':" % format
        # TODO: at some point in the future we should also check for valid values in desc
        if not exists(join(basedir, 'audio', format)):
            raise Exception('%s is listed as an audio format, but doesn\'t appear in the audio/ folder' % format)

        if 'filelist' not in desc:
            raise Exception('Audio format "%s" does not define a filelist' % format)

        filelist = yaml.load(open(join(basedir, 'metadata', desc['filelist'])).read())
        print '  filelist OK, lists %d files' % len(filelist)

        for pid, filename in filelist.items():
            fullpath = join(basedir, 'audio', format, filename)
            if not exists(fullpath):
                raise Exception('For format "%s": file "%s" appears in filelist, however there is no corresponding "%s"' % (format, filename, fullpath))


    # check that the groundtruth files do actually exist if they are specified
    print '\nChecking groundtruth files...'
    groundTruth = config.get('groundTruth', {})
    print 'Found groundtruth files:', str(groundTruth.keys())
    for name, gtfile in groundTruth.items():
        print "\nChecking groundtruth '%s':" % name
        gt = GroundTruth('')
        gt.load(join(basedir, 'metadata', gtfile))
        # check that the IDs used in the groundtruth files exist in all the filelists
        for afname, af in audioFormats.items():
            flist = yaml.load(open(join(basedir, 'metadata', af['filelist'])).read()).keys()
            for gid in gt:
                if gid not in flist:
                    raise Exception("ID '%s' is in GroundTruth '%s', but could not be found in filelist for audio format '%s'" % (gid, gtfile, afname))
        print '  gt filelist OK, found classes:', str(sorted(set(gt.values())))

if __name__ == '__main__':
    try:
        basedir = sys.argv[1]
    except:
        usage()

    print '**** Checking collection directory: %s ****\n' % basedir

    validate(basedir)

    print '\nCollection validated!'
