
import sys
# Configuration imports
import argparse
from config import Config, ConfigError
# Migration imports
from subhost import Subhost
from migrater import Migrater

def createClient(hostConfig):
    return Subhost(
        hostConfig['host'],
        hostConfig['username'],
        hostConfig['password'],
        hostConfig['port'],
        hostConfig['legacy'])

def run(config):
    # Get clients for the source and targer servers
    source = createClient(config.source)
    target = createClient(config.target)
    # Init migrater
    migrater = Migrater(source, target, mock=config.mockMigration)
    # Migrate playlists if required
    if config.migratePlaylists:
        migrater.migratePlaylists()
    # Migrate starred songs
    if config.migrateStarred:
        migrater.migrateStarred()

# Main app
if __name__ == '__main__':
    # Get configuration file from args
    parser = argparse.ArgumentParser(description='Migrate from one Subsonic server to another')
    parser.add_argument('-c', '--config', default='./config.toml', type=str, help='Configuration filepath')
    args = parser.parse_args()
    # Parse configuration file
    try:
        c = Config(args.config)
    except ConfigError as e:
        print(e)
        sys.exit(1)
    # Run
    run(c)
    sys.exit(0)