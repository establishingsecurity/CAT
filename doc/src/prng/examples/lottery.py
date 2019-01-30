from functools import reduce
from http.server import BaseHTTPRequestHandler, HTTPServer
from secrets import randbelow

# Define rng parameters
STATE_SIZE = 64
MODULUS = 2 ** STATE_SIZE

MULTIPLIER = 0x5DEECE66D ** 2
INCREMENT = 0xB ** 2
SHIFT = STATE_SIZE - 8

STATE = [randbelow(2 ** STATE_SIZE) for _ in range(9)]

HOST = "127.0.0.1"
PORT = 8080


def next_states(state):
    return [(MULTIPLIER * s + INCREMENT) % MODULUS for s in STATE]


class LotteryHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        global STATE
        STATE = next_states(STATE)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = """
        <!doctype html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <title>New Lottery Numbers</title>
        <meta name="description" content="The HTML5 Herald">
        <meta name="author" content="SitePoint">
        <style type="text/css">
            body {
                margin: 0 auto;
                max-width: 480px;
                line-height: 1.6;
                font-size: 18px;
                background: black;
                padding: 0;
            }
            main {
                color: white;
                height: 100vh;
                width: 480px;
                display: flex;
                justify-content: center;
                flex-direction: column;
            }
            h1,h2,h3 { line-height:1.2 }
            .number {
                color: #12ff12;
                font-size: 30px;
                font-family: monospace, monospace;
                margin-right: 10px;
            }
            </style>
        </head>

        <body>
            <main>
                <h1>New Lottery Numbers</h1>
                <div>
        """ + "\n".join(
            ['<span class="number">{:02X}</span>'.format(x >> SHIFT) for x in STATE]
        )
        """
                </div>
            </main>
        </body>
        </html>
        """
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


if __name__ == "__main__":
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, LotteryHandler)
    print("running server on http://{}:{}/ ...".format(HOST, PORT))
    httpd.serve_forever()
