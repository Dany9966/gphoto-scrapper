import functools
import os
import time
import traceback
import urllib.request

from gphoto_scrapper import log

LOG = log.get_logger()

def check_download_dir(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)

    return path


def download_item(download_dir, url, filename, skip_existing=False,
                  skip_failed_items=False):
    if not all([url, filename]):
        LOG.debug('url=%s; filename=%s', url, filename)
        raise Exception('Download failed. URL or filename not provided.')
    path = os.path.join(download_dir, filename)
    if os.path.exists(path) and skip_existing:
        LOG.warning("Skipping downloading item with name: %s. Already exists.",
                    filename)
        return

    try:
        retry_request()(urllib.request.urlretrieve)(url, path)
        return path
    except Exception as ex:
        LOG.error('Error occurred while downloading %s from url: %s. '
                  'Error was: %s', filename, url, str(ex))
        if not skip_failed_items:
            raise


def retry_request(max_retries=5, retry_interval=3):
    def _retry_request(func):
        @functools.wraps(func)
        def _exec_retry(*args, **kwargs):
            i = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except KeyboardInterrupt as ex:
                    LOG.info('Operation cancelled, skip retrying')
                    LOG.exception(ex)
                    raise
                except Exception as ex:
                    i += 1
                    if i < max_retries:
                        LOG.warning(
                            "Exception occurred, retrying (%d/%d):\n%s",
                            i, max_retries, traceback.format_exc())
                        time.sleep(retry_interval)
                    else:
                        raise
        return _exec_retry
    return _retry_request
