import os
import urllib.request

from gphoto_scrapper import log

LOG = log.get_logger()

def check_download_dir(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)

    return path


def download_item(download_dir, url, filename, skip_existing=False):
    if not all([url, filename]):
        LOG.debug('url=%s; filename=%s', url, filename)
        raise Exception('Download failed. URL or filename not provided.')
    path = os.path.join(download_dir, filename)
    if os.path.exists(path) and skip_existing:
        LOG.warning("Skipping downloading item with name: %s. Already exists.",
                    filename)
        return

    try:
        urllib.request.urlretrieve(url, path)
    except Exception as ex:
        LOG.error('Error occurred while downloading %s from url: %s. '
                  'Error was: %s', filename, url, str(ex))
        raise ex

    return path
