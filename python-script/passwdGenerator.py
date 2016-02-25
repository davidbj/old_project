#!/usr/bin/env python
#-*- coding:utf-8 -*-
import random, string

class password(object):
    data = open("/usr/share/dict/words").read().lower()
    def renew(self, n, maxmem=3):
        self.chars = [ ]
       for i in range(n):
            randspot = random.randrange(len(self.data))
            self.data = self.data[randspot:] + self.data[:randspot]
            where = -1
            locate = ''.join(self.chars[-maxmem:])

            while where < 0 and locate:
                where = self.data.find(locate)
                locate = locate[1:]

            c = self.data[where+len(locate)+1]
            if not c.islower():
                c = random.choice(string.lowercase)
            self.chars.append(c)
        return ''.join(self.chars)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        dopass = int(sys.argv[1])
    else:
        dopass = 8

    if len(sys.argv) > 2:
        length = int(sys.argv[2])
    else:
        length = 10

    if len(sys.argv) > 3:
        memory = int(sys.argv[3])
    else:
        memory = 3

    onepass = password()
    for i in range(dopass):
        print onepass.renew(length, memory)
