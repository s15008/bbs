# How to make a BBS Web Application

## HTTP Serverの立ち上げよおう
```Python
import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHander

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.server_forever()
```

## Databaseを使って投稿を保存しよおう
SQLiteを使ってみよおう

```Python
import sqlite3
import time
```
