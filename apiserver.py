from flask import Flask
from flask import request
from scheduler.default_scheduler import DefaultScheduler

app = Flask(__name__)
default_scheduler = DefaultScheduler()


@app.route("/createInstance", methods=['POST'])
def create_instance():
    return default_scheduler.sync_create_instance(request.get_json())


@app.route("/rsync/createInstance", methods=['POST'])
def rsync_create_instance():
    return default_scheduler.rsync_create_instance(request.get_json())


@app.route("/instance/action/delete")
def delete_instance():
    instance_id = request.args.get("instance_id")
    cloud_identify = request.args.get("cloud_identify")
    return default_scheduler.delete_instance(instance_id, cloud_identify)


@app.route("/updateInstance/", methods=['POST'])
def update_instance():
    pass


@app.route("/flavors")
def list_flavor():
    return default_scheduler.list_flavor()


@app.route("/images")
def list_image():
    return default_scheduler.list_image()


@app.route("/regions")
def list_region():
    pass


@app.route("/instance/detail")
def get_instance_detail():
    instance_id = request.args.get("instance_id")
    cloud_identify = request.args.get("cloud_identify")
    return default_scheduler.check_instance(instance_id, cloud_identify)


@app.route("/batch/instance/detail")
def get_batch_instance_detail():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0')
