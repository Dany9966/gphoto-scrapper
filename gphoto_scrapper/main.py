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
                        choices=[25, 50, 100],
                        help='The number of items to download at once. '
                             'Default is 25. Maximum is 100')
    parser.add_argument('--skip-existing', default=False, action='store_true',
                        help='Skip already downloaded items')
    parser.add_argument('--log-file', type=str,
                        default='gphoto-scrapper.log',
                        help='The name of the log file')
    parser.add_argument('--debug', default=False, action='store_true',
                        help='Include DEBUG messages')
    parser.add_argument('--sort', default=False, action='store_true',
                        help='Sort photos and videos by creation month '
                             '(into "Y-M" dirs)')
    parser.add_argument('--skip-failing-downloads', default=False,
                        action='store_true',
                        help='Skip items that failed downloading')
    parser.add_argument('--update', default=False, action='store_true',
                        help="Update current media directory. Download stops"
                             "at first existing media found in selected dir.")
    args = parser.parse_args()

    log.configure_logging(args.log_file)
    LOG = log.get_logger()
    media_service = service.MediaService(args.secrets_file, SCOPES,
                                         download_path=args.download_dir)
    media_service.build_service()

    try:
        media_service.start(page_size=args.page_size,
                            skip_existing=args.skip_existing,
                            sort=args.sort, update_dir=args.update,
                            skip_failed_items=args.skip_failing_downloads)
    except (Exception, KeyboardInterrupt) as ex:
        LOG.warning('An error occurred. Stopping download process at %s',
                    media_service.last_downloaded_id)
        media_service.stop()
        raise ex


if __name__ == '__main__':
    main()
