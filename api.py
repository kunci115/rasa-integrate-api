import subprocess

import flask
from flask import request, jsonify, Response
from sanic.exceptions import abort
import json
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = 1


def subprocess_cmd(command):
    try:
        process = os.popen(command).read()
        return process
    except Exception as ex:
        return Response({"message": json.dumps(ex)})
    """except subprocess.CalledProcessError as e:
        return Response({"message": json.dumps(e)})"""


@app.route('/data', methods=['POST', 'GET'])
def upload_data():
    if request.method == 'GET':
        return jsonify(status=200)
    try:
        train_type = request.json['train_type']
        data = request.json['data']
        data_type = request.json['data_type']
        bot_name = request.json['bot_name']
        group = request.json['group_name']
        if data_type == "md":
            filename = train_type + ".md"
        elif data_type == "json":
            filename = train_type + ".json"
        else:
            return jsonify(status=401)
        if train_type == "nlu":
            language = request.json['language']
            path = "/home/ubuntu/userdata" + '/'+ group + '/' + bot_name+ "/data/bot/nlu/" + language
        elif train_type == "core":
            path = "/home/ubuntu/userdata" + '/' + group + '/' + bot_name + "/data/bot/core/"
        create = subprocess_cmd('cd ' + path + '; touch ' + filename)
        if data_type == "json":
            f = open(path + "/" + filename, "w")
            result = json.dumps(data)
            final = result[2:-2].replace('\\','')
            f.write("{")
            f.write(final)
            f.write("}")
            f.close()
        elif data_type == "md":
            f = open(path + "/" + filename, "w")
            f.write(data)
            f.close()
        return jsonify(status=200)
    except ValueError as e:
        return jsonify(error=e,
            status=500)


@app.route('/train', methods=['POST'])
def train_data():
    if request.method == "GET":
        return jsonify(status=401)
    try:
        train_type = request.json['train_type']
        bot_name = request.json['bot_name']
        group = request.json['group']
        if train_type == "nlu":
            language = request.json['language']
            train_nlu = subprocess_cmd(
                'cd /home/ubuntu/userdata/'+group+'/'+bot_name+';'
                'python3 -m bl_core.nlu_train '+'--name '+bot_name + '--lang ' + language)
            return jsonify(status=200)

        elif train_type == "core":
            train_core = subprocess_cmd(
                'cd /home/ubuntu/userdata/'+group+'/'+bot_name+';'
                'rasa train core --fixed-model-name core/core')
            return jsonify(status=200)
    except ValueError as e:
        return jsonify(error=e, status=500)


@app.route('/run', methods=['POST'])
def run_bot():
    if request.method == "GET":
        return jsonify(status=401)
    try:
        bot_name = request.json['bot_name']
        group = request.json['group']

        """connection_interface2 = subprocess_cmd("cd /home/ubuntu/userdata/" + group + ";" + "cd " + bot_name + "; python3 -m "
                                                                           "bl_core.nlg -p "
                                                                           "5006")"""

        connection_interface1 = subprocess_cmd("cd /home/ubuntu/userdata    " + group + ";" + "cd " + bot_name +
                                        "; python3 -m bl_core.nlg -p 5006 & python3 -m bl_core.connection_interface & rasa run actions --actions actions &")

        """connection_interface3 = subprocess_cmd("cd /home/ubuntu/userdata/" + group + ";" + "cd " + bot_name + "; rasa run "
                                                                                                     "actions "
                                                                                                     "--actions "
                                                                                                     "actions")"""
        return jsonify(status=200)
    except ValueError as e:
        return jsonify(error=e, status=500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)

