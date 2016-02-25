#!/usr/bin/env python

from subprocess import PIPE, Popen

def hwInfo():
    ld = []
    '''get  hwconfig information.'''
    cmd = 'hwconfig 2>/dev/null | grep -v "^$"'
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    data = stdout.split('\n')
    for line in data[0:-1]:
        if line.startswith('\t'):
            ld[data.index(line)-1] = data[data.index(line)-1]+"& %s" % line
        else:
            ld.append(line)
    return ld

def parseInfo(data):
    dc = {}
    for line in data:
        k = line.split('\t')[0].split(':')[0]
        for l in line.split('\t')[1:]:
            if l:
                v = l
        dc[k]=l
    cpuInfo = cpuparse(dc['Processors'])
    return cpuInfo


def cpuparse():
    p_cmd = 'cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l'
    c_cmd = 'cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c'
    p1 = Popen(p_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    cpuPhyNum = p1.communicate()[0].split('\n')[0]
    
    p2 = Popen(c_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    cpuCoresNum = p2.communicate()[0]
    print cpuCoresNum

if __name__ == "__main__":
    #data = hwInfo()
    #print  parseInfo(data)
    print cpuparse()

