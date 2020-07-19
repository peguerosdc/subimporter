
from utils import stringifySong
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

class Migrater(object):

    """Migrater"""
    def __init__(self, migrateFrom, migrateTo, mock=False):
        # Store clients
        self.source = migrateFrom
        self.target = migrateTo
        self.isMocked = mock
        logger.info(f"MOCK MIGRATION? {mock}")

    def migratePlaylists(self, interactive=True):
        # Wrapper to gather input from the user
        def should(text):
            value = input(text)
            return value.strip().lower() == 'y'
        # Core to migrate each playlist
        def migratePlaylist(playlist):
            # Create a new playlist in the target server with a unique name
            if not self.isMocked:
                targetPlaylist = self.target.createPlaylist(f"{playlist['name']} at {int(datetime.now().timestamp())}")
                logger.info(f"Target playlist: '{targetPlaylist['name']}'")
            # Add each song in this playlist to the new targetPlaylist
            playlist = self.source.getPlaylist(playlist["id"])
            for song in playlist['entry']:
                try:
                    matchSong = self.target.findClosestMatchToSong(song)
                    if matchSong:
                        logger.info(f"Migrating {stringifySong(song)} as {stringifySong(matchSong)}")
                        if not self.isMocked:
                            self.target.addSongToPlaylist(targetPlaylist['id'], matchSong['id'])
                    else:
                        logger.warning(f"No match to {stringifySong(song)}")
                except Exception as e:
                    logger.exception(f"Unable to migrate song {stringifySong(song)}")
        # Perform playlsts migration
        try:
            # Get all playlists
            playlists = self.source.getPlaylists()
            for playlist in playlists:
                # Ask if this playlist should be migrated only if running on interactive mode
                if not interactive or should(f"Migrate '{playlist['name']}' with {playlist['songCount']} songs Y/[N]? "):
                    logger.info(f"Migrating playlist '{playlist['name']} ({playlist['songCount']})'")
                    try:
                        migratePlaylist(playlist)
                    except Exception as e:
                        logger.exception(f"Unable to migrate playlist '{playlist['name']} ({playlist['songCount']})'")
        except Exception as e:
            logger.exception("Unable to migrate playlists")

    def migrateStarred(self):
        # TODO: support albums and artists too
        try:
            songs = self.source.getStarredSongs()
            # Migrate each song
            logger.info(f"{len(songs)} starred songs to migrate")
            for song in songs:
                try:
                    matchSong = self.target.findClosestMatchToSong(song)
                    if matchSong:
                        logger.info(f"Migrating {stringifySong(song)} as {stringifySong(matchSong)}")
                        if not self.isMocked:
                            self.target.starSong(matchSong['id'])
                    else:
                        logger.warning(f"No match to {stringifySong(song)}")
                except Exception as e:
                    logger.exception(f"Unable to star song {stringifySong(song)}")
        except Exception as e:
            logger.exception("Unable to migrate starred songs")
