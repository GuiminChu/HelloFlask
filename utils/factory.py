import yaml


def read_yaml(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    cf = yaml.safe_load(data)
    return cf


# conf = read_yaml('../resources/application.yml')
# print(conf)
# print(conf['redis']['host'])
