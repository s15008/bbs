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
            conn.execute("create table if not exists entry (id integer primary key, message text, date real);")
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()

    def post(self, message):
        conn = sqlite3.connect(self.path, isolation_level='DEFERRED')
        try:
            conn.execute("insert into entry(message, date) values(?, ?);", (message, time.time()))
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
            result = [x for x in conn.execute("select id, message, date from entry;")]
        finally:
            conn.close()

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
            response += '<section class="panel"><header>Post from:</header><main><form method="GET" action="/post"><input type="text" name="message" placeholder="message"><input type="submit" value="送信"></form></main></section>'
            # 投稿内容を表示
            for e in sorted(db.get(), key=lambda e: e[2], reverse=True):
                response += '<section class="panel"><header>{0}</header><main>{1}</main></section>'.format(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(e[2])), e[1])

        elif request == '/post':
            if not 'message' in params:
                response += '<h1>Invalid Post</h1>'
            else:
                db.post(params['message'])
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

