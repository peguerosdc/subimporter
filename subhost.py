
from subsonic import Subsonic

class Subhost(object):

    """Host wrapper for subsonic clients"""
    def __init__(self, host, username, password, isLegacy):
        self.client = Subsonic(
            host,
            username,
            password, legacyAuth=isLegacy)

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
            if p['name'] == name:
                return p

    def addSongToPlaylist(self, playlistId, songId):
        return self.client.updatePlaylist(playlistId=playlistId, songIdToAdd=songId)

    def searchSong(self, name):
        return self.client.search3(query=name, artistCount=0, albumCount=0)

    def findClosestMatchToSong(self, song):
        results = self.client.search3(query=song['name'], artistCount=0, albumCount=0)
        # Get closest song in the results
        for s in results['song']:
            if s['name'] == song['name'] and s['artist'] == song['artist'] and s['album'] == song['album']:
                return s
        return None
