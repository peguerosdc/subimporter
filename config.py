import toml
from schema import Schema, SchemaError, Optional

class Config(object):

    """Parses the configuration from a filepath"""
    def __init__(self, path):
        # Read configuration file and check it is in a valid format
        try:
            rawConfig = toml.load(path)
            config = self.__validate__(rawConfig)
        except FileNotFoundError:
            raise ConfigError(f"Configuration file '{path}' not found")
        except (TypeError, toml.TomlDecodeError) as e:
            raise ConfigError(str(e))
        except SchemaError as e:
            raise ConfigError(f"Invalid configuration:\n{str(e)}")
        # Store into useful objects
        self.source = config["source"]
        self.target = config["target"]
        self.migratePlaylists = config["migratePlaylists"]
        self.migrateStarred = config["migrateStarred"]
        self.mockMigration = config["mockMigration"]

    def __validate__(self, config):
        # This is the expected template
        schema = Schema({
            Optional('migratePlaylists', default=True): bool,
            Optional('migrateStarred', default=True): bool,
            Optional('mockMigration', default=False): bool,
            'source': {
                'host': str,
                'port' : int,
                'username': str,
                'password': str,
                'legacy': bool,
            },
            'target': {
                'host': str,
                'port' : int,
                'username': str,
                'password': str,
                'legacy': bool,
            },
        })
        # Check that the provided config is valid
        return schema.validate(config)

        
class ConfigError(Exception):
    
    """Error when parsing a configuration file"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
