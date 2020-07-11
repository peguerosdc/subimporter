
import sys
# Configuration imports
import argparse
from config import Config, ConfigError

from subsonic import Subsonic


def run(configuration):
    # Test a connection
    client = Subsonic('host' , 'user' , 'pass' , port=8080, legacyAuth=True)
    # Get all playlists
    playlists = client.getPlaylists()
    for p in playlists:
        # Retrieve songs
        playlist = client.getPlaylist(p["id"])
        print(f"Migrating {playlist['name']} with {playlist['songCount']} songs")

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