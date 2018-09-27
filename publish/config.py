import tomlkit


CONFIG_PATH = './config.toml'

with open(CONFIG_PATH) as stream:
    config = tomlkit.parse(stream.read())
