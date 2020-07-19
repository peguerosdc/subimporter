# Migration imports
from subhost import Subhost
from migrater import Migrater

import logging
logger = logging.getLogger(__name__)

def createClient(hostConfig):
    return Subhost(
        hostConfig['host'],
        hostConfig['username'],
        hostConfig['password'],
        hostConfig['port'],
        hostConfig['legacy'])

def run(config):
    # Get clients for the source and targer servers
    source = createClient(config.source)
    target = createClient(config.target)
    logger.info(f"Migrating from {source} to {target}")
    # Init migrater
    migrater = Migrater(source, target, mock=config.mockMigration)
    # Migrate playlists if required
    logger.info(f"Migrate playlists? {config.migratePlaylists}")
    if config.migratePlaylists:
        migrater.migratePlaylists(interactive=config.migratePlaylistsInteractive)
    # Migrate starred songs
    logger.info(f"Migrate starred items? {config.migrateStarred}")
    if config.migrateStarred:
        migrater.migrateStarred()