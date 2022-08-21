import os
import time

from flask import Flask, request

from model import inference

app = Flask(__name__)

src_dir = "./src"
save_dir = "./res"
if not os.path.exists(src_dir):
    os.mkdir(src_dir)

if not os.path.exists(save_dir):
    os.mkdir(save_dir)


@app.route("/matting", methods=["POST"])
def matting():
    file = request.files["file"]
    file_name = "{}.png".format(time.time())
    src_path = os.path.join(src_dir, file_name)
    save_path = os.path.join(save_dir, file_name)

    file.save(src_path)
    url = inference(src_path, save_path)
    return url


if __name__ == '__main__':
    app.run( port=os.getenv("PORT", default=5000))
