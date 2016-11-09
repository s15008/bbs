import random

import http.server
import socketserver
import urllib.parse

import sqlite3
import time

class database():
    def __init__(self, path):
        self.path = path
        self.create()

    def create(self):
        conn = sqlite3.connect(self.path, isolation_level='EXCLUSIVE')
        try:
            conn.execute("create table if not exists entry (id integer primary key, name text, message text, date real, color text);")
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()

    def post(self, name, message, color):
        conn = sqlite3.connect(self.path, isolation_level='DEFERRED')
        try:
            conn.execute("insert into entry(name, message, date, color) values(?, ?, ?, ?);", (name, message, time.time(), color))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()

    def get(self):
        result = []
        conn = sqlite3.connect(self.path)
        try:
            result = [x for x in conn.execute("select id, name, message, date, color from entry;")]
        finally:
            conn.close()

        print(result)
        return result

class HttpHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # リクエスト内容をパース
        request = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(request.query))

        # レスポンスを生成
        body = self.body(request.path, params)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)
    
    def body(self, request, params):
        # ヘッダー
        response = '<html><header> <link rel="stylesheet" href="https://cdn.rawgit.com/alexanderGugel/papier/master/dist/papier-1.0.0.min.css"></header><body class="bg-subtle"><div style="width:50%;margin:0 auto">'

        # 本文
        if request == '/get':
            # 投稿用フォームを挿入
            response += '<section class="panel"><header class="bg-blue">Post from:</header><main><form method="GET" action="/post"><input type="text" name="name_" placeholder="name"><input type="text" name="message" placeholder="message"><button class="bg-indigo" type="submit" value="send">送信</button></form></main></section>'
            # 投稿内容を表示
            for e in sorted(db.get(), key=lambda e: e[3], reverse=True):
                response += '<section class="panel {3}"><header><strong>{0}</strong> {1}</header><main>{2}</main></section>'.format(e[1], time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(e[3])), e[2], e[4])

        elif request == '/post':
            if not 'message' in params or not 'name_' in params:
                response += '<h1>Invalid Post</h1>'
            else:
                color_list = ["bg-white", "bg-red", "bg-pink", "bg-purple", "bg-deep-purple", "bg-indigo"]
                color = random.choice(color_list)
                print(params, params['message'], params['name_'], color)
                db.post(params['name_'], params['message'], color)
                response += '<meta http-equiv="REFRESH" content="1;URL=/get"><h1>Post Successed.</h1>'
        else:
            response += '<h1>Invalid Post</h1>'

        # フッター
        response += '</div></body></html>'

        return response.encode('utf-8')

if __name__ == '__main__':
    HOST = "localhost"
    PORT = 8000
    db = database("entry.db")

    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer((HOST, PORT), HttpHandler)
    print("serving at port", PORT)
    print("CTRL+c to stop server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        httpd.socket.close()

