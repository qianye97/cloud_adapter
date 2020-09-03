class Instance(dict):
    def __init__(self, instance_id, instance_name, cpu_count, memory_size, storage_capacity, ssh_port, state, desc):
        super().__init__()
        self['instance_id'] = instance_id
        self['instance_name'] = instance_name
        self['cpu_count'] = cpu_count
        self['memory_size'] = memory_size
        self['storage_capacity'] = storage_capacity
        self['ssh_port'] = ssh_port
        self['state'] = state
        self['desc'] = desc

