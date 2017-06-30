import sys
import os

print(os.getcwd())
print('the command line arguements are:')

for i in sys.argv:
    print(i)

print('the python path is {}'.format(sys.path))
