from functools import reduce
from secrets import randbelow
from http.server import BaseHTTPRequestHandler, HTTPServer

# Define rng parameters
STATE_SIZE = 512
MODULUS = 2 ** STATE_SIZE

MULTIPLIER = reduce(lambda a, x: a * x, [
    111868394042609032323385573096424085839,
    281691314538379734849988413722506999470,
    38865202901255411182762865052694722337,
    240295848810064394069370812797612347769
])
INCREMENT = 225978269326188702280723738608360289365
SHIFT = STATE_SIZE - 128
# Chosen by fair dice roll
STATE = randbelow(2**STATE_SIZE)
SHIFT = STATE_SIZE - 64

PORT = 8080


def next_number(state):
    return (MULTIPLIER * state + INCREMENT) % MODULUS


class LotteryHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        global STATE
        STATE = next_number(STATE)

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
        </head>

        <body>{}</body>
        </html>
        """.format(
            STATE >> SHIFT
        )
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


if __name__ == "__main__":
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, LotteryHandler)
    print("running server...")
    httpd.serve_forever()
    httpd.serve_forever()
