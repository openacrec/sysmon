from flask import Flask, request, render_template

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'json'}
app.config["UPLOAD_FOLDER"] = "/images"


@app.route("/")
def sysmon():
    return render_template('index.html')


@app.route("/post", methods=['GET', 'POST'])
def json_handler():
    if request.method == 'POST':
        if request.is_json:
            req = request.get_json()
            print(req)
            return "Received!", 200
        else:
            return "Request was not JSON", 400
    else:
        return "<p>This site has no content. It's a endpoint for sysmon reports.</p>"


def receive_data():
    pass


with app.test_client() as test:
    req = test.post("/post", json={
        "machine_name": "asraphael",
        "cpu": [
            [
                "2021-05-23 18:45:54",
                17.8
            ]
        ],
        "memory": [
            71.2
        ],
        "gpu": [
            [
                {
                    "index": "0",
                    "type": "NVIDIA GeForce GTX 1660 Ti",
                    "uuid": "GPU-c7b2d3ec-8b29-796e-ed4b-2b295e80d270",
                    "mem_used": 1858,
                    "mem_total": 6144,
                    "mem_used_percent": 30.240885416666668
                }
            ]
        ],
    })
    print(req)
