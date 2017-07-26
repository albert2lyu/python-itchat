import re

test = 'bill.gates@microsoft.com,bill.gates@microsoft.com'
r = re.findall(r'([\w\.]+@+[\w]+.com)', test)
print(r)
