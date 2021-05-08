import os
import urllib.request


def check_download_dir(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)

    return path

def download_item(download_path, item, skip_existing=False):
    url = item.get('baseUrl')
    filename = item.get('filename', '')
    if not all([url, filename]):
        print('url=%s; filename=%s' % (url, filename))
        raise Exception('Download failed. URL or filename not provided.')
    path = os.path.join(download_path, filename)
    if os.path.exists(path) and skip_existing:
        print("Skipping downloading item with name: %s. Already exists." % (
            filename))
        return
    urllib.request.urlretrieve(url, path)
    print('Downloaded item with ID: %s to path: %s' % (item.get('id'), path))
