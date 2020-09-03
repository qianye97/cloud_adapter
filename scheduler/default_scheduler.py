from driver.openstack_driver import OpenstackDriver
from model.response import ResponseData
import json
import time
from util.ping import can_ping


class DefaultScheduler(object):
    def filter(self, cloud_list):
        return cloud_list

    def list_registered_cloud_platform(self):
        return [
            {
                "cloud_ip": "192.168.1.251",
                "cloud_username": "admin",
                "cloud_password": "admin",
                "cloud_identify": "OPENSTACK",
                "cloud_project_id": "69211395830a43cdbb7055c427f438a4"
            }
        ]

    def create_instance(self, inventory):
        cloud_list = self.filter(self.list_registered_cloud_platform())
        choose, created, target = 0, 0, inventory['count']
        result = []
        name = inventory['name']
        while created < target and choose < len(cloud_list):
            od = self.get_driver(cloud_list[choose])
            inventory['name'] = "%s-%d" % (name, created)
            ans = od.create_instance(inventory)
            print(ans)
            if ans[0]:
                created += 1
                result.append(ans[1])
            else:
                choose += 1
        return result

    def sync_create_instance(self, inventory):
        instance_list = self.create_instance(inventory)
        result = []
        for instance in instance_list:
            # 检测云主机是否能ping通，策略：每15s检查一次，总共检查20次
            retries = 20
            while retries > 0:
                if can_ping(instance['external_ip']):
                    result.append(instance)
                retries -= 1
                time.sleep(15)
        message = "target: %s, created: %s" % (inventory['count'], len(result))
        response_data = ResponseData(200, message, result)
        return json.dumps(response_data)

    def rsync_create_instance(self, inventory):
        result = self.create_instance(inventory)
        print(result)
        message = "target: %s, created: %s" % (inventory['count'], len(result))
        response_data = ResponseData(200, message, result)
        return json.dumps(response_data)

    def get_driver(self, registered_info):
        if registered_info['cloud_identify'] == 'OPENSTACK':
            return OpenstackDriver(registered_info)
        return None

    def list_flavor(self):
        flavors = []
        cloud_list = self.list_registered_cloud_platform()
        for i in range(0, len(cloud_list)):
            od = self.get_driver(cloud_list[i])
            flavors.extend(od.list_flavor())
        response_data = ResponseData(200, None, flavors)
        return json.dumps(response_data)

    def list_image(self):
        images = []
        cloud_list = self.list_registered_cloud_platform()
        for i in range(0, len(cloud_list)):
            od = self.get_driver(cloud_list[i])
            images.extend(od.list_image())
        response_data = ResponseData(200, None, images)
        return json.dumps(response_data)

    def delete_instance(self, instance_id, cloud_identify):
        cloud_list = self.filter(self.list_registered_cloud_platform())
        od = None
        for registered_info in cloud_list:
            if registered_info['cloud_identify'] == cloud_identify:
                od = self.get_driver(registered_info)
                break
        od.do_action(instance_id, 'delete')
        response_data = ResponseData(200, '删除成功!', None)
        return response_data

    def check_instance(self, instance_id, cloud_identify):
        cloud_list = self.filter(self.list_registered_cloud_platform())
        od = None
        for registered_info in cloud_list:
            if registered_info['cloud_identify'] == cloud_identify:
                od = self.get_driver(registered_info)
                break
        response_data = ResponseData(200, None, od.check_instance(instance_id))
        return json.dumps(response_data)
