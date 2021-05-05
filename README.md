# Subsonic Importer
Tool to migrate from one Subsonic server to another

## Running
To install the required dependencies:
```
$ pip install -r requirements.txt
```
To run:
```
$ python app.py
usage: app.py [-h] [-c CONFIG]

Migrate from one Subsonic server to another

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Configuration filepath

```

## Configuration

```toml
# Should playlists be migrated?
migratePlaylists = true

# When set to true, confirmation is asked before migrating every playlist.
# If false, every playlist is migrated.
migratePlaylistsInteractive = true

# Should starred songs be migrated?
migrateStarred = true

# When set to true, no INSERT operations are performed in the target host.
# This is suggested to be set to 'true' in the first run to check that
# all your songs are going to be properly migrated.
mockMigration = false

# Defines the log level. If not set, the default is 'info'.
log = "info"

# Configuration of the source host (the host to be migrated).
[source]
host = "http://localhost"
port = 8080
username = "user"
password = "pass"
# Set to 'true' if the host is using Subsonic's hex-encoded authentication
# (< 1.13.0). If 'false', then the host is using md5(password + salt)
# authentication (>= 1.13.0).
legacy = true
version="1.15.0"

# Configuration of the target host (the host where the songs are going to
# be migrated).
[target]
host = "http://localhost"
port = 8080
username = "user"
password = "pass"
legacy = false
version="1.15.0"
```

For a sample, check `config.toml`.

## Disclaimer

I wrote this script for my personal usage to migrate my Subsonic instance from [spl0k/supysonic](https://github.com/spl0k/supysonic) to [deluan/navidrome](https://github.com/deluan/navidrome) and had almost a 100% of success. Songs that were not able to be migrated automatically was because of how Navidrome tries to expose my songs with their information (title, artist, album, etc) "corrected" when they are not pretty tagged while Supysonic exposes them "as is".
If you find this software doesn't work as you expect, you can try changing the heuristic I use to match songs between servers which is found at `subhost.findClosestMatchToSong.areEqual`. Actually it is pretty simple as in my case both libraries (source and target) were populated with the exact same files, so almost all songs preserved the same tags between servers, but this could vary depending on your instance (as I mentioned with Navidrome).

## License

Licensed under the [MIT License](https://github.com/peguerosdc/subimporter/blob/master/LICENSE).
