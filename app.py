from flask import Flask, render_template, request, jsonify
from storage import append_json_line

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/api/echo")
def echo():
    data = request.get_json(silent=True) or {}
    append_json_line(data)
    return jsonify({"testing": 123}), 200


if __name__ == "__main__":
    app.run()