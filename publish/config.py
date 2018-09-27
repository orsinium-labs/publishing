import tomlkit


CONFIG_PATH = './config.toml'


def load():
    with open(CONFIG_PATH) as stream:
        return tomlkit.parse(stream.read())


def dump(config):
    with open(CONFIG_PATH, 'w') as stream:
        stream.write(tomlkit.dumps(config))
