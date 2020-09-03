import requests
import json
import time
from model.flavor import Flavor
from model.image import Image
from model.instance import Instance

TOKEN = "gAAAAABfULh7e18NBpAYTD5-ruRcJwws5KOYtExACOCydVexZU3sbl1cJYsE2vj1KLs56Bgb7skcApNwJjwswIdqE6cVFA-7dTa3f8rhF0w9X4zqj1whR_Z5JGXMLWQOXj9OkreFFWgRH4Kmim3qDOK3hcEKnma3vbPKa9MMuViQVEP4ae1AqaM"
headers = {
    'Content-Type': 'application/json',
    'X-Auth-Token': TOKEN
}
ACTION_PARAM = {
    'restart': {
        "reboot": {
            "type": "HARD"
        }
    },
    'shutdown': {
        "os-stop": None
    },
    'start': {
        "os-start": None
    },
    'delete': {
        "forceDelete": None
    }
}


class OpenstackDriver(object):
    def __init__(self, registered_info):
        self.registered_info = registered_info
        self.cloud_identify = "OPENSTACK"

    def create_instance(self, inventory):
        create_instance_url = 'http://%s:8774/v2/servers' % self.registered_info['cloud_ip']
        data = {
            "server": {
                "name": inventory['name'],
                "block_device_mapping_v2": [{
                    "uuid": inventory['image_id'],
                    "source_type": "image",
                    "destination_type": "volume",
                    "boot_index": 0,
                    "delete_on_termination": "true"
                }],
                "flavorRef": inventory['flavor_id'],
                "networks": [
                    {
                        "uuid": "9a6f53f7-bea5-4d50-9dda-96043bc709aa"
                    }
                ]
            }
        }
        # 1.创建实例
        response = requests.post(create_instance_url, data=json.dumps(data), headers=headers)
        instance = json.loads(response.content.decode())
        instance_id = instance['server']['id']
        # 2.获取可用的浮动ip列表
        list_float_ip_url = 'http://%s:9696/v2.0/floatingips' % self.registered_info['cloud_ip']
        response = requests.get(list_float_ip_url, headers=headers)
        floatips = json.loads(response.content.decode())['floatingips']
        float_ip_address = float_ip_id = None
        for floatip in floatips:
            if not floatip['port_id']:
                float_ip_id = floatip['id']
                float_ip_address = floatip['floating_ip_address']
                break
        # TODO 没有可用的浮动IP
        # 3.获取实例网卡端口
        get_instance_port_url = 'http://%s:8774/v2.1/servers/%s/os-interface' % (self.registered_info['cloud_ip'], instance_id)
        retries = 5
        port_id = None
        while retries > 0:
            response = requests.get(get_instance_port_url, headers=headers)
            port_info = json.loads(response.content.decode())
            if port_info['interfaceAttachments']:
                port_id = port_info['interfaceAttachments'][0]['port_id']
                break
            retries -= 1
            time.sleep(2)
        # 4.绑定浮动ip到实例网卡端口
        assign_float_ip_to_port_url = 'http://%s:9696/v2.0/floatingips/%s' % (self.registered_info['cloud_ip'], float_ip_id)
        data = {
            "floatingip": {
                "port_id": port_id
            }
        }
        requests.put(assign_float_ip_to_port_url, data=json.dumps(data), headers=headers)
        instance = {
            'external_ip': float_ip_address,
            'instance_id': instance_id,
            'cloud_identify': self.cloud_identify
        }
        return True, instance

    def do_action(self, instance_id, action):
        do_action_url = 'http://%s:8774/v2.1/servers/%s/action' % (self.registered_info['cloud_ip'], instance_id)
        data = ACTION_PARAM[action]
        response = requests.post(do_action_url, data=json.dumps(data), headers=headers)

    def update_instance(self, inventory):
        pass

    def check_instance(self, instance_id):
        check_instance_url = 'http://%s:8774/v2.1/servers/%s' % (self.registered_info['cloud_ip'], instance_id)
        response = requests.get(check_instance_url, headers=headers)
        instance_detail = json.loads(response.content.decode())['server']
        state = 1 if instance_detail['status'] == 'ACTIVE' else 0
        result = Instance(instance_detail['id'], instance_detail['name'], None, None, None, 22, state, None)
        return result

    def list_flavor(self):
        result = []
        list_flavor_url = 'http://%s:8774/v2/flavors/detail' % self.registered_info['cloud_ip']
        response = requests.get(list_flavor_url, headers=headers)
        flavors = json.loads(response.content.decode())['flavors']
        for flavor in flavors:
            new_flavor = Flavor(flavor['name'], None, flavor['vcpus'], flavor['ram'], flavor['disk'], flavor['id'], None, None, None, None)
            result.append(new_flavor)
        return result

    def list_image(self):
        result = []
        list_image_url = 'http://%s:9292/v2/images' % self.registered_info['cloud_ip']
        response = requests.get(list_image_url, headers=headers)
        images = json.loads(response.content.decode())['images']
        for image in images:
            # TODO 操作系统类型和版本
            new_image = Image(image['id'], image['name'], None, 'centos', '7.4')
            result.append(new_image)
        return result

    def auth(self):
        pass


if __name__ == '__main__':
    registered_info = {
        "cloud_ip": "192.168.1.251",
        "cloud_username": "admin",
        "cloud_password": "admin",
        "cloud_identify": "openstack",
        "cloud_project_id": "69211395830a43cdbb7055c427f438a4"
    }
    od = OpenstackDriver(registered_info)
    inventory = {
        "name": "liyanqin",
        "image_id": "32e15fe0-5b38-4f6c-a02a-5414f94586fe",
        "flavor_id": "41a3d8a5-5ba5-454b-98a7-80b470550fd8",
        "volume_size": "10",
        "count": 1
    }
    print(od.create_instance(inventory))
