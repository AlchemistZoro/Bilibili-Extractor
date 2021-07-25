from flask import Flask, jsonify, render_template
from flask_cors import CORS
import osapi

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

CORS(app, resources=r'/*')


@app.route('/list/<name>/')
def api_list(name):
    return jsonify(osapi.getFileList("/home/wzc/testcode/Bilibili-Extractor/data/%s" % name,'mp4'))


@app.route('/<ftype>/<name>/')
def api_video(name,ftype):
    return osapi.getBinaryFile("/home/wzc/testcode/Bilibili-Extractor/data/{}/{}".format(ftype,name))

# @app.route('/picture/<name>/')
# def api_pic(name):
#     return osapi.getBinaryFile("/home/wzc/testcode/factory/output/picture/%s" % name)

# @app.route('/audio/<name>/')
# def api_audio(name):
#     return osapi.getBinaryFile("/home/wzc/testcode/factory/output/audio/%s" % name)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5030, debug=True)
