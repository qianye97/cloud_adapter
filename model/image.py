class Image(dict):
    def __init__(self, image_id, name, desc, system_type, system_version):
        super().__init__()
        self['image_id'] = image_id
        self['name'] = name
        self['desc'] = desc
        self['system_type'] = system_type
        self['system_version'] = system_version
