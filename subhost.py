
from subsonic import Subsonic
from utils import stringifySong

class Subhost(object):

    """Host wrapper for subsonic clients"""
    def __init__(self, host, username, password, port, isLegacy):
        self.client = Subsonic(
            host,
            username,
            password,
            port=port, legacyAuth=isLegacy)

    def getStarredSongs(self):
        response = self.client.getStarred2()
        return response['song'] if response['song'] else []

    def starSong(self, songId):
        return self.client.star(sids=[songId])

    def getPlaylists(self):
        return self.client.getPlaylists()

    def getPlaylist(self, playlistId):
        return self.client.getPlaylist(playlistId)

    def createPlaylist(self, playlistName):
        response = self.client.createPlaylist(name=playlistName)
        # Reload playlists to find this element
        playlists = self.client.getPlaylists()
        for p in playlists:
            if p['name'] == playlistName:
                return p

    def addSongToPlaylist(self, playlistId, songId):
        return self.client.updatePlaylist(playlistId=playlistId, songIdToAdd=songId)

    def searchSong(self, title):
        return self.client.search3(query=title, artistCount=0, albumCount=0)

    def findClosestMatchToSong(self, song):
        # Wrapper for pagination
        def getPaginatedSongs(query, count, offset):
            results = self.client.search3(query=query, songCount=count, artistCount=0, albumCount=0, songOffset=offset)
            return results['song'] if 'song' in results else []
        # Heuristic to compare songs
        def areEqual(song1, song2):
            # Check if they are strictly equal tag by tag
            exactlyEqual = song1['title'].lower() == song2['title'].lower() and song1['artist'].lower() == song2['artist'].lower() and song1['album'].lower() == song2['album'].lower()
            # Check if they are somehow equal
            somehowEqual = song1['title'].lower() == song2['title'].lower() and song1['duration'] == song2['duration']
            return exactlyEqual or somehowEqual
        # Look for the closest song in this server
        songOffset = 0
        songCount = 20
        candidates = getPaginatedSongs(song['title'], songCount, songOffset)
        while candidates:
            # Get closest song in the results
            for candidate in candidates:
                if areEqual(song, candidate):
                    #print(f"Closest song to\n  {stringifySong(song)} is\n  {stringifySong(s)}")
                    return candidate
            # Query again if the song was not present in this batch
            songOffset += songCount
            candidates = getPaginatedSongs(song['title'], songCount, songOffset)
        return None

