from .main import run
from .STGIB import ST



def TR(data, width, height, groups):
        data = ST(data, groups, width, height)
        # for i in range(len(data['groups'])):
        #     data['groups'][i]['name'] = data['groups'][i]['id']
        # graph = json.load(open(path))
        return run(data, width, height)