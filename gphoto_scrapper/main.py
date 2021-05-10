import argparse
from gphoto_scrapper import log
from gphoto_scrapper import service

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


def main():
    parser = argparse.ArgumentParser(
        description='Download your photos and videos from Google Photos using '
                    'the photoslibrary API')
    parser.add_argument(
        'download_dir', type=str,
        help='Directory to which the download occurs')
    parser.add_argument('--secrets-file', type=str, required=True,
                        help='Path to JSON file containing the API secrets')
    parser.add_argument('--page-size', type=int, default=25,
                        help='The number of items to download at once. '
                             'Default is 25')
    parser.add_argument('--skip-existing', default=False, action='store_true',
                        help='Skip already downloaded items. Default is false')
    parser.add_argument('--log-file', type=str,
                        default='gphoto-scrapper.log',
                        help='The name of the log file')
    parser.add_argument('--debug', default=False, action='store_true',
                        help='Include DEBUG messages')
    args = parser.parse_args()

    log.configure_logging(args.log_file)
    media_service = service.MediaService(args.secrets_file, SCOPES,
                                         download_path=args.download_dir)
    media_service.build_service()

    try:
        media_service.start(page_size=args.page_size,
                            skip_existing=args.skip_existing)
    except Exception as ex:
        media_service.stop()
        raise ex


if __name__ == '__main__':
    main()
