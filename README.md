# How to make a BBS Web Application
Pythonを使ってウェブアプリケーションを作ってみよおう
インタープリタを使って試してみよおう

参考
* [Python標準ライブラリで簡易掲示板 | ヘキサ日記  | HEXADRIVE | スタッフが綴る、ヘキサなあれこれ](http://hexadrive.jp/hexablog/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0/7334/)
* and 42...

## HTTP Serverを立ち上げよおう
http.serverモジュールを使ってみよおう
[Official](http://docs.python.jp/3/library/http.server.html)

### Example

```python
import http.server
import socketserver

HOST = "localhost"
PORT = 8000

Handler = http.server.SimpleHTTPRequestHander

httpd = socketserver.TCPServer((HOST, PORT), Handler)

print("serving at port", PORT)
httpd.server_forever()
```

## Databaseを使って投稿を保存しよおう
sqlite3モジュールを使ってみよおう
[Official](http://docs.python.jp/3/library/sqlite3.html)

### Example

```python
import sqlite3
import time

# データベースへの接続の作成
conn = sqlite3.connect("example.db")

# テーブルの作成
c = conn.cursor()
c.execute('''CREATE TABLE products
              (id real, title text, actor text, maker_name text)''')

# 行の追加
c.execute("INSERT INTO products VALUES(1, 'グラビアアイドル初イキッ!!高橋しょう子', '高橋しょう子', 'ムーディーズ')")
c.execute("INSERT INTO products VALUES(2, '芸能人ANRI What a day!!', 'ANRI', 'MUTEKI')")

# 変更の確定
conn.commit()

# データベースの接続を閉じる(*忘れないでねぇ*)
conn.close()

# データベースへの接続の作成(前に作ったdbがあったらそのまま使えるよ)
conn = sqlite3.connect("example.db")

# データベースからデータを取得するよおう
c = conn.cursor()

# 取れた行いっぺんに出す
c.execute("SELECT title FROM products")
print(c.fetchall())

# 一個ずつ出す(イテレータ)
c.execute("SELECT title FROM products")
print(c.fetcone())
print(c.fetcone())
print(c.fetcone())

# 返り値を使う(イテレータ)
target = ('2',)
rows = c.execute("SELECT * FROM products WHERE id=?", target)
for row in rows:
  print(row)

```
