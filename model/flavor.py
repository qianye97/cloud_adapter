class Flavor(dict):
    def __init__(self, name, desc, cpu_count, memory_size, storage_capacity, flavor_id, flavor_type, bandwidth, pps, gpu_type):
        super().__init__()
        self['name'] = name
        self['desc'] = desc
        self['cpu_count'] = cpu_count
        self['memory_size'] = memory_size
        self['storage_capacity'] = storage_capacity
        self['flavor_id'] = flavor_id
        self['flavor_type'] = flavor_type
        self['bandwidth'] = bandwidth
        self['pps'] = pps
        self['gpu_type'] = gpu_type