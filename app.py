
import sys
# Configuration imports
import argparse
from config import Config, ConfigError

from subsonic import Subsonic

def should(text):
    value = input(text)
    return value.lower() == 'y'

def createClient(hostConfig):
    return Subsonic(
        hostConfig['host'],
        hostConfig['username'],
        hostConfig['password'], legacyAuth=hostConfig['legacy'])

def findSong(server, song):
    results = server.search3(query=song['name'], artistCount=0, albumCount=0)
    # Get closest song in the results
    for s in results['song']:
        if s['name'] == song['name'] and s['artist'] == song['artist'] and s['album'] == song['album']:
            return s
    return None

def migratePlaylists(source, target):
    print("Migrating playlists...")
    # Get all playlists
    playlists = source.getPlaylists()
    for playlist in playlists:
        # Ask if this playlist should be migrated
        if should(f"Migrate {playlist['name']} with {playlist['songCount']} songs Y/[N]?"):
            print(f"Migrating...")
            # Create a new playlist in the target server
            # TODO: what happens if that playlist already exists?
            targetPlaylist = target.createPlaylist(playlist['name'])
            # Add each song in this playlist to the new targetPlaylist
            playlist = source.getPlaylist(p["id"])
            for song in playlist['entry']:
                matchSong = findSong(target, song)
                target.updatePlaylist(playlistId=playlist['id'], songIdToAdd=matchSong['id'])

def migrateStarred(source, target):
    # TODO: support albums or artists too
    print("Migrating starred songs...")
    starred = source.getStarred2()
    # Migrate each song
    if starred['song']:
        for song in starred['song']:
            matchSong = findSong(target, song)
            target.star(sids=[matchSong['id']])

def run(config):
    # Get a client for the source server
    source = createClient(config['source'])
    # Get a client for the target server
    target = createClient(config['target'])
    # Migrate playlists if required
    if config.migratePlaylists:
        migratePlaylists(source, target)
    # Migrate starred songs
    if config.migrateStarred:
        migrateStarred(source, target)

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