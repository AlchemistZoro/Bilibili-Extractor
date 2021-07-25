# 远程视频批量播放

## Description

客户端显示服务端某目录下的所有视频文件，可播放。

## Solution

后端提供两个接口，一个返回目录下的所有文件名，一个返回视频数据。

``` python
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import osapi

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

CORS(app, resources=r'/*')


@app.route('/list/')
def api_list():
    return jsonify(osapi.getFileList("resource"))


@app.route('/video/<name>/')
def api_video(name):
    return osapi.getBinaryFile("resource/%s" % name)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

```

需要一些辅助

``` python
import os
def getFileList(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


def getBinaryFile(filename):
	f = open(filename, "rb")
	data = f.read()
	f.close()
	return data
```

前端 JS 获取并通过修改 DOM 内容来展示

``` html
<div id="list"> </div>

<script>
    var httpRequest = new XMLHttpRequest();
    httpRequest.open('GET', 'http://10.203.172.202:5000/list/', true);
    httpRequest.send();

    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = JSON.parse(httpRequest.responseText);
            for (var item in json) {
                var filename = json[item];
                var tmp = document.getElementById("list").innerHTML;
                document.getElementById("list").innerHTML += filename + "<br/><video width=\"320\" height=\"240\" controls><source src=\"http://10.203.172.202:5000/video/" + filename + "/\" type=\"video/mp4\"> </video> <br/> <br/>";
                console.log(filename);
            }
        }
    };
</script>
```



