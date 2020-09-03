import json


class Dict(dict):
    def __init__(self, a, b, c):
        super().__init__()
        self['a'] = a
        self['b'] = b
        self['c'] = c


if __name__ == '__main__':
    d = Dict(1, 2, 3)
    print(json.dumps(d))
