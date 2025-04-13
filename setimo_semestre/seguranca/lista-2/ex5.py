from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def serve_image():
    return send_file('image.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
