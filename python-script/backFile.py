#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''Author:David.Zhang
  Date:2014/02/26
  Function:backup directory and file.
'''

import sys, os, shutil, filecmp

MAXVERSIONS=100

def backup(tree_top, bakdir_name='bakdir'):
    for dir, subdirs, files in os.walk(tree_top):
        backup_dir = os.path.join(dir, bakdir_name)
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        subdirs[:] = [d for d in subdirs if d != bakdir_name]
        for file in files:
            filepath = os.path.join(dir, file)
            destpath = os.path.join(backup_dir, file)
            abspath = os.path.abspath(filepath)
            for index in xrange(MAXVERSIONS):
                backup = '%s.%2.2d' % (destpath, index)
                if not os.path.exists(backup):
                    break
                if index > 0:
                    old_backup = '%s.%2.2d' % (destpath, index-1)
                else:
                    old_backup = '%s.%2.2d' % (destpath, index)

            try:
                if os.path.isfile(old_backup) and filecmp.cmp(abspath, old_backup, shallow=False):
                    continue
            except:
                pass

            try:
                shutil.copy(filepath, backup)
            except OSError:
                pass

if __name__ == "__main__":
    try:
        tree_top = sys.argv[1]
    except IndexError:
        tree_top = '.'
    backup(tree_top)
