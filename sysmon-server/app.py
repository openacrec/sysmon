from json import dump, load

from flask import Flask, request, render_template

app = Flask(__name__)

with open(f"{app.root_path}/static/machine_names.json", "w+") as names_file:
    names_json = {"names": []}
    dump(names_json, names_file)


@app.route("/")
def sysmon():
    with open(f"{app.root_path}/static/machine_names.json", "r") as in_file:
        machine_names = load(in_file)
        known_names = machine_names["names"]
    return render_template("index.html", hosts=known_names)


@app.route("/post", methods=['GET', 'POST'])
def json_handler():
    if request.method == 'POST':
        if request.is_json:
            req = request.get_json()
            static_dir = f"{app.root_path}/static"
            with open(f"{static_dir}/{req['machine_name']}.json", "w+") as out:
                dump(req, out)
            with open(f"{static_dir}/machine_names.json", "r") as in_file:
                machine_names = load(in_file)
                with open(f"{static_dir}/machine_names.json", "w") as out:
                    known_names = machine_names["names"]
                    new_name = req["machine_name"]
                    if new_name not in known_names:
                        known_names.append(new_name)
                        machine_names["names"] = known_names
                    dump(machine_names, out)
            return "Received!", 200
        else:
            return "Request was not JSON", 400
    else:
        return "<p>This site has no content. " \
               "It's a endpoint for sysmon reports.</p>"
