import socket
import os

import tornado.gen
import tornado.ioloop
import tornado.iostream
import tornado.tcpserver
import tornado.web


class MessageBuffer(object):
    def __init__(self):
        self.waiters = set()
        self.cache = []
        self.cache_size = 200

    def wait_for_messages(self, callback):
        self.waiters.add(callback)

    def cancel_wait(self, callback):
        self.waiters.remove(callback)

    def new_messages(self, messages):
        print("Sending new message to %r listeners" % len(self.waiters))
        for callback in self.waiters:
            callback(messages)
        self.waiters = set()
        self.cache.extend(messages)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]

messages_buffer = MessageBuffer()


class SimpleTcpClient(object):
    client_id = 0

    def __init__(self, stream):
        super().__init__()
        SimpleTcpClient.client_id += 1
        self.id = SimpleTcpClient.client_id
        self.stream = stream

        self.stream.socket.setsockopt(
            socket.IPPROTO_TCP, socket.TCP_NODELAY, 1
        )
        self.stream.socket.setsockopt(
            socket.IPPROTO_TCP, socket.SO_KEEPALIVE, 1
        )
        self.stream.set_close_callback(self.on_disconnect)

    @tornado.gen.coroutine
    def on_disconnect(self):
        self.log('disconnected')
        yield []

    @tornado.gen.coroutine
    def dispatch_client(self):
        try:
            while True:
                data = yield self.stream.read_until_regex(b'End\r\n')
                print(data.decode('utf-8'))
                if 'Auth::' in data.decode('utf-8'):
                    messages_buffer.new_messages([data])
                    yield self.stream.write(data)
        except tornado.iostream.StreamClosedError:
            pass

    @tornado.gen.coroutine
    def on_connect(self):
        raddr = 'closed'
        try:
            raddr = '%s:%d' % self.stream.socket.getpeername()
        except Exception:
            pass
        self.log('new, %s' % raddr)

        yield self.dispatch_client()

    def log(self, msg, *args, **kwargs):
        print('[connection %d] %s' % (self.id, msg.format(*args, **kwargs)))


class SimpleTcpServer(tornado.tcpserver.TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        connection = SimpleTcpClient(stream)
        yield connection.on_connect()


class HTTPHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=messages_buffer.cache)


class MessageUpdatesHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        messages_buffer.wait_for_messages(self.on_new_messages)

    def on_new_messages(self, messages):
        # Closed client connection
        if self.request.connection.stream.closed():
            return
        lines = messages[0].decode('utf-8').split('\r\n')
        self.write(dict(lines=lines))
        self.finish()

    def on_connection_close(self):
        messages_buffer.cancel_wait(self.on_new_messages)


def main():
    host = '127.0.0.1'
    port = 8888

    server = SimpleTcpServer()
    server.listen(port, host)
    print("Listening on %s:%d..." % (host, port))

    app = tornado.web.Application(
        [
            (r"/", HTTPHandler),
            (r"/msg", MessageUpdatesHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    app.listen(8100)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
