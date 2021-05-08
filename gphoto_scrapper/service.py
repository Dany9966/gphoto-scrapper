from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from gphoto_scrapper import utils


class MediaService(object):
    API_SERVICE_NAME = 'photoslibrary'
    API_VERSION = 'v1'

    def __init__(self, secrets_file, api_scopes, last_downloaded_id='',
                 download_path='Downloads'):
        self._secrets_file = secrets_file
        self._api_scopes = api_scopes
        self._service = None
        self._last_downloaded_id = last_downloaded_id
        self._download_path = utils.check_download_dir(download_path)

    def build_service(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self._secrets_file, self._api_scopes)

        try:
            cred = flow.run_local_server()
        except Exception:
            cred = flow.run_console()

        try:
            service = build(self.API_SERVICE_NAME, self.API_VERSION,
                            credentials=cred, static_discovery=False)
            print("%s Service has been created successfully." % (
                self.API_SERVICE_NAME))
        except Exception as ex:
            print("Failed to create %s service." % self.API_SERVICE_NAME)
            raise ex

        self._service = service.mediaItems()

    def download_media_page(self, media_page_list, skip_existing=False):
        for item in media_page_list:
            utils.download_item(self._download_path, item,
                                skip_existing=skip_existing)
            self._last_downloaded_id = item.get('id')

    def start(self, page_size=25, skip_existing=False):
        print('Starting download process.')
        media_page = self.get_media_page(page_size=page_size)
        next_page_token = media_page.get('nextPageToken', '')
        # next_page_token = ''
        self.download_media_page(media_page.get('mediaItems', []),
                                 skip_existing=skip_existing)
        print("Finished downloading page (of %s items), next page token: %s" % (
            page_size, next_page_token))

        while next_page_token:
            media_page = self.get_media_page(page_size, next_page_token)
            next_page_token = media_page.get('nextPageToken', '')
            self.download_media_page(media_page.get('mediaItems', []),
                                     skip_existing=skip_existing)
            print("Finished downloading page (of %s items), next page token: "
                  "%s" % (page_size, next_page_token))

    def stop(self):
        print('An error occured. Stopping download process at %s' % (
            self._last_downloaded_id))

    def get_media_page(self, page_size=25, next_page_token=''):
        try:
            media_page = self._service.list(
                pageSize=page_size, pageToken=next_page_token).execute()
        except Exception as ex:
            print('Failed to fetch media page.')
            raise ex

        return media_page
