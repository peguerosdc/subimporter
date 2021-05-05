import libsonic

class Subsonic(object):

    """Wrapper for libsonic"""
    def __init__(self, *args, **kwargs):
        self.client = libsonic.Connection(*args, **kwargs)

    def getStarred2(self):
        response = self.client.getStarred2()

        return response["starred2"]

    def star(self, *args, **kwargs):
        response = self.client.star(*args, **kwargs)
        return True

    def getPlaylists(self):
        response = self.client.getPlaylists()
        return response["playlists"]["playlist"]

    def getPlaylist(self, *args, **kwargs):
        response = self.client.getPlaylist(*args, **kwargs)
        return response["playlist"]

    def createPlaylist(self, name):
        response = self.client.createPlaylist(name=name)
        return True

    def updatePlaylist(self, *args, **kwargs):
        response = self.client.updatePlaylist(*args, **kwargs)
        return True

    def search3(self, *args, **kwargs):
        response = self.client.search3(*args, **kwargs)
        return response["searchResult3"]
