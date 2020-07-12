
def stringifySong(song):
    return f"<'{song['name']}' by '{song['artist']}' in '{song['album']}'>"

class Migrater(object):

    """Migrater"""
    def __init__(self, migrateFrom, migrateTo):
        super(Migrater, self).__init__()
        # Store clients
        self.source = migrateFrom
        self.target = migrateTo

    def migratePlaylists(self):
        print("Migrating playlists...")
        # Wrapper to gather input from the user
        def should(text):
            value = input(text)
            return value.lower() == 'y'
        # Get all playlists
        playlists = self.source.getPlaylists()
        for playlist in playlists:
            # Ask if this playlist should be migrated
            if should(f"Migrate {playlist['name']} with {playlist['songCount']} songs Y/[N]?"):
                print(f"Migrating...")
                # Create a new playlist in the target server
                # TODO: what happens if that playlist already exists?
                targetPlaylist = self.target.createPlaylist(playlist['name'])
                # Add each song in this playlist to the new targetPlaylist
                playlist = self.source.getPlaylist(p["id"])
                for song in playlist['entry']:
                    matchSong = self.target.findClosestMatchToSong(song)
                    if matchSong:
                        self.target.addSongToPlaylist(targetPlaylist['id'], matchSong['id'])
                    else:
                        print(f"No match to {stringifySong(song)}")

    def migrateStarred(self):
        # TODO: support albums or artists too
        print("Migrating starred songs...")
        songs = self.source.getStarredSongs()
        # Migrate each song
        for song in songs:
            matchSong = self.target.findClosestMatchToSong(song)
            if matchSong:
                self.target.starSong(matchSong['id'])
            else:
                print(f"No match to {stringifySong(song)}")
