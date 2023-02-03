import yaml

_config = yaml.safe_load(open('config.yml', 'r', encoding='utf-8'))

VERSION: str = '1.4'
SAVE_DIR: str = _config['save_dir']
TGRCODE_API: str = _config['tgrcode_api']
DEBUG: bool = _config['debug']
TGRCODE_API_COURSE_COUNT: int = _config['tgrcode_api_course_count']
SHOW_EMPTY_SLOT: bool = _config['show_empty_slot']
LOAD_ONLINE_ON_START: bool = _config['load_online_on_start']
SHOW_THUMBNAILS: bool = _config['show_thumbnails']
