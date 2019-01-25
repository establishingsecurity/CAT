import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

from gmpy2 import mpz, next_prime

# Define rng parameters
STATE_SIZE = 8192
MODULUS = int(next_prime(2 ** STATE_SIZE))
MULTIPLIER = int(next_prime(2 ** (STATE_SIZE // 2)))
INCREMENT = int(next_prime(2 ** (STATE_SIZE // 4)))
# Chosen by fair dice roll
STATE = int(1234551291201209370912059721430) % MODULUS
SHIFT = STATE_SIZE // 2

PORT = 8080


def next_number(state):
    return (MULTIPLIER * state + INCREMENT) % MODULUS


class LotteryHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        global STATE
        STATE = next_number(STATE)
        logging.warning('Current State: {}'.format(STATE))

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = """
        <!doctype html>
        <html lang="en">
        <head>
        <meta charset="utf-8">

        <title>New Lottery Numbers</title>
        <meta name="description" content="The HTML5 Herald">
        <meta name="author" content="SitePoint">
        </head>

        <body>{}</body>
        </html>
        """.format(STATE >> SHIFT)
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


if __name__ == "__main__":
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, LotteryHandler)
    print('running server...')
    httpd.serve_forever()
