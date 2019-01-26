from functools import reduce
from secrets import randbelow
from http.server import BaseHTTPRequestHandler, HTTPServer

# Define rng parameters
STATE_SIZE = 64
MODULUS = 2 ** STATE_SIZE

MULTIPLIER = 0x5DEECE66D**2
INCREMENT = 0xB**2
SHIFT = STATE_SIZE - 8

STATE = [randbelow(2 ** STATE_SIZE) for _ in range(9)]

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
                margin:40px auto;
                max-width:650px;
                line-height:1.6;
                font-size:18px;
                color:#444;
                padding:0 10px
            }
            h1,h2,h3 { line-height:1.2 }
            .number {
                font-size: 30px;
                padding: 0 10px;
                font-family: monospace, monospace;
            }
            </style>
        </head>

        <body>
            <h1>New Lottery Numbers</h1>
        """ + "\n".join(['<span class="number">{:02X}</span>'.format(x >> SHIFT) for x in STATE])
        """
        </body>
        </html>
        """
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


if __name__ == "__main__":
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, LotteryHandler)
    print("running server...")
    httpd.serve_forever()
    httpd.serve_forever()
    httpd.serve_forever()
