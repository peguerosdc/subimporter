import toml
from schema import Schema, SchemaError

class Config(object):

    """Parses the configuration from a filepath"""
    def __init__(self, path):
        # Read configuration file and check it is in a valid format
        try:
            config = toml.load(path)
            self.__check__(config)
        except FileNotFoundError:
            raise ConfigError(f"Configuration file '{path}' not found")
        except (TypeError, toml.TomlDecodeError) as e:
            raise ConfigError(str(e))
        except SchemaError as e:
            raise ConfigError(f"Invalid configuration:\n{str(e)}")
        # Store into useful objects
        self.source = config["source"]
        self.target = config["target"]

    def __check__(self, config):
        # This is the expected template
        schema = Schema({
            'source': {
                'host': str,
                'username': str,
                'password': str,
                'legacy': bool,
            },
            'target': {
                'host': str,
                'username': str,
                'password': str,
                'legacy': bool,
            },
        })
        # Check that the provided config is valid
        schema.validate(config)

        
class ConfigError(Exception):
    
    """Error when parsing a configuration file"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
