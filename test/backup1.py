import os
import time

source = ['D:\\images']
target_dir = 'D:\\images'
today = target_dir + os.sep + time.strftime('%Y%m%d')
now = time.strftime('%H%M%S')
inputs = input('Enter a comment --> ')

if len(inputs)==0:
    target = today + os.sep + now + '.zip'
else:
    target = today + os.sep + now + '_' + inputs.replace(' ', '_') + '.zip'

if not os.path.exists(today):
    os.mkdir(today)
    print('Successfully created directory', today)
if not os.path.exists(target_dir):
    os.mkdir(target_dir)
zip_command = 'zip -r {0} {1}'.format(target, ' '.join(source))
print('Zip command is :')
print(zip_command)

if os.system(zip_command) == 0:
    print('Successful backup to', target)
else:
    print('backup Failed')
