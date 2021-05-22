from flask import Flask, render_template, Response, request
import cv2
import  camerahelper 
import predictEmo

app = Flask(__name__)


def gen():  # generate frame by frame from camera
    while True:
        data= camerahelper.gen_frames()

        frame=data[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



@app.route('/')
def hello():
    return render_template("index2.html")

@app.route('/', methods = ['POST'])
def cap():
    if request.method == 'POST':
        f = request.files['userfile']
        path = "./static/{}".format(f.filename)
        f.save(path)

    emo = predictEmo.predictImg(path)
    result_dic = {
        'image':path,
        'emotion': emo
    }

    return render_template("index2.html", your_result = result_dic )       

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cam')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)