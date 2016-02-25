import random
import string
import sys


smailar_chars='0o1ilLIOPp'
upper="".join(set(string.uppercase)-set(smailar_chars))
lower="".join(set(string.lowercase)-set(smailar_chars))
symbols='#$%&\()+_=:;#@!~'
chars=lower+upper
#numbers=string.digits
numbers='23456789'
groups=(lower,upper,numbers,symbols)

def genpass(length=8):
	pw=[random.choice(i) for i in groups]
	con = ''.join(groups)
	for i in range(length-len(pw)):
		pw.append(random.choice(con))
	random.shuffle(pw)
	return ''.join(pw)

print genpass(int(sys.argv[1]))
