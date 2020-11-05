#==> https://blog.gtwang.org/programming/python-md5-sha-hash-functions-tutorial-examples/

import hashlib

# 建立 SHA1 物件
s = hashlib.sha384()

data = b'asdasdas'
s.update(data)
h = s.hexdigest()
print(h)

name = '12345'
name = name.encode('utf-8')
