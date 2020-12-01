from flask import Flask, Response, request
from bot import get_bot


app = Flask(__name__)


@app.route("/", methods=["POST"])
def prime_num():
    bot.action(request.get_json())
    return Response("success!")


port_number = 3000
if __name__ == '__main__':
    bot = get_bot()
    app.run(port=port_number)
