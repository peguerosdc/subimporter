
from utils import stringifySong
from datetime import datetime

class Migrater(object):

    """Migrater"""
    def __init__(self, migrateFrom, migrateTo, mock=False):
        super(Migrater, self).__init__()
        # Store clients
        self.source = migrateFrom
        self.target = migrateTo
        self.isMocked = mock

    def migratePlaylists(self, interactive=True):
        print("Migrating playlists...")
        # Wrapper to gather input from the user
        def should(text):
            value = input(text)
            return value.strip().lower() == 'y'
        # Get all playlists
        playlists = self.source.getPlaylists()
        for playlist in playlists:
            # Ask if this playlist should be migrated only if running on interactive mode
            if not interactive or should(f"Migrate '{playlist['name']}' with {playlist['songCount']} songs Y/[N]? "):
                print(f"Migrating...")
                # Create a new playlist in the target server with a unique name
                if not self.isMocked:
                    targetPlaylist = self.target.createPlaylist(f"{playlist['name']} at {int(datetime.now().timestamp())}")
                # Add each song in this playlist to the new targetPlaylist
                playlist = self.source.getPlaylist(playlist["id"])
                for song in playlist['entry']:
                    matchSong = self.target.findClosestMatchToSong(song)
                    if matchSong:
                        if not self.isMocked:
                            self.target.addSongToPlaylist(targetPlaylist['id'], matchSong['id'])
                    else:
                        print(f"No match to {stringifySong(song)}")

    def migrateStarred(self):
        # TODO: support albums and artists too
        print("Migrating starred songs...")
        songs = self.source.getStarredSongs()
        # Migrate each song
        for song in songs:
            matchSong = self.target.findClosestMatchToSong(song)
            if matchSong:
                if not self.isMocked:
                    self.target.starSong(matchSong['id'])
            else:
                print(f"No match to {stringifySong(song)}")
