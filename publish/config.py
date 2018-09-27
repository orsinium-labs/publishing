import tomlkit


CONFIG_PATH = './config.toml'


def load(path=CONFIG_PATH):
    with open(path) as stream:
        return tomlkit.parse(stream.read())


def dump(config, path=CONFIG_PATH):
    with open(path, 'w') as stream:
        stream.write(tomlkit.dumps(config))
