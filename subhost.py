
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
        # return self.client.star(sids=[songId])
        pass

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
        #return self.client.updatePlaylist(playlistId=playlistId, songIdToAdd=songId)
        pass

    def searchSong(self, title):
        return self.client.search3(query=title, artistCount=0, albumCount=0)

    def findClosestMatchToSong(self, song):
        results = self.client.search3(query=song['title'], artistCount=0, albumCount=0)
        # Get closest song in the results
        if 'song' in results:
            for s in results['song']:
                if s['title'] == song['title'] and s['artist'] == song['artist'] and s['album'] == song['album']:
                    #print(f"Closest song to\n  {stringifySong(song)} is\n  {stringifySong(s)}")
                    return s
        return None

