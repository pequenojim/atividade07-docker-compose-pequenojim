import os

from flask import Flask, jsonify, render_template
from redis import Redis, RedisError


app = Flask(__name__)
redis_client = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


@app.get("/")
def pagina_inicial():
    try:
        visitas = redis_client.incr("pequenojim:visitas")
    except RedisError:
        return render_template("index.html", visitas=None), 503

    return render_template("index.html", visitas=visitas)


@app.get("/health")
def health():
    try:
        if redis_client.ping():
            return jsonify(status="ok", banco="redis"), 200
    except RedisError:
        pass

    return jsonify(status="indisponivel", banco="redis"), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
