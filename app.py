
import sys
# Configuration imports
import argparse
from config import Config, ConfigError
# Importer
import subimporter

def mapLogLevel(l):
    logs = {
        "info" : logging.INFO,
        "debug" : logging.DEBUG,
        "warn" : logging.WARNING,
        "no" : logging.NOTSET,
        "error" : logging.ERROR,
        "critical": logging.CRITICAL
    }
    default = logs["info"]
    return logs[l] if l in logs else default

if __name__ == '__main__':
    # Get configuration file from args
    parser = argparse.ArgumentParser(description='Migrate from one Subsonic server to another')
    parser.add_argument('-c', '--config', default='./config.toml', type=str, help='Configuration filepath')
    args = parser.parse_args()
    # Parse configuration file
    try:
        c = Config(args.config)
    except ConfigError as e:
        logger.error(e)
        sys.exit(1)
    # Set up logging
    import logging
    logging.basicConfig(stream=sys.stdout, format='[%(name)s] %(levelname)s: %(message)s', level=mapLogLevel(c.logLevel))
    logger = logging.getLogger(__name__)
    # Run
    try:
        subimporter.run(c)
        logger.info("DONE")
        sys.exit(0)
    except KeyboardInterrupt:
        logger.info("INTERRUPTED")
        sys.exit(1)