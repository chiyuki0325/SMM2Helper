from dataclasses import dataclass
import requests

from config import TGRCODE_API, VERSION

USER_AGENT = f'SMM2Helper/{VERSION} HiddenSuperStar/0.0.4'

__all__ = ['TGRCodeAPIBaseException', 'TGRCodeAPIException', 'TGRCodeAPICourseIDException',
           'Maker', 'Course',
           'prettify_course_id', 'normalize_course_id',
           'search_popular', 'search_endless_mode',
           'user_info', 'level_info', 'level_data_dataid']


class TGRCodeAPIBaseException(BaseException):
    pass


class TGRCodeAPIException(TGRCodeAPIBaseException):
    pass


class TGRCodeAPICourseIDException(TGRCodeAPIBaseException):
    pass


@dataclass
class Maker:
    name: str
    region: str
    maker_id: str
    country: str
    last_active: str
    mii_image_url: str
    pose_name: str
    hat_name: str
    shirt_name: str
    pants_name: str
    courses_played: int
    courses_attempted: int
    courses_cleared: int
    courses_deaths: int
    likes: int
    maker_points: int
    easy_highscore: int
    normal_highscore: int
    expert_highscore: int
    super_expert_highscore: int
    versus_rating: int
    versus_rank: str
    versus_plays: int
    versus_won: int
    versus_lost: int
    versus_disconnected: int
    coop_clears: int
    coop_plays: int
    versus_kills: int
    versus_killed_by_others: int
    uploaded_levels: int
    first_clears: int
    world_records: int
    super_world_clears: int
    super_world_id: str


@dataclass
class Course:
    name: str
    description: str
    uploaded_date: str
    data_id: str
    course_id: str
    game_style: str
    theme: str
    difficulty: str
    tag_1: str
    tag_2: str
    world_record: str
    upload_time: str
    clears: int
    attempts: int
    clear_rate: str
    likes: int
    boos: int
    maker: Maker
    record_holder: Maker


def prettify_course_id(course_id: str) -> str:
    course_id = course_id.strip()
    return f'{course_id[0:3]}-{course_id[3:6]}-{course_id[6:9]}'.upper()


def normalize_course_id(course_id: str) -> str:
    ret: str = course_id.translate(dict.fromkeys(map(ord, '-_ '), None)).upper()
    if len(ret) != 9:
        raise TGRCodeAPICourseIDException('Invalid course ID.')
    return ret


def deserialize_course(course: dict) -> Course:
    if 'world_record_pretty' not in course:
        course['world_record_pretty'] = '0'
    return Course(
        name=course['name'],
        description=course['description'],
        uploaded_date=course['uploaded_pretty'],
        course_id=course['course_id'],
        data_id=course['data_id'],
        game_style=course['game_style_name'],
        theme=course['theme_name'],
        difficulty=course['difficulty_name'],
        tag_1=course['tags_name'][0],
        tag_2=course['tags_name'][1],
        world_record=course['world_record_pretty'],
        upload_time=course['upload_time_pretty'],
        clears=course['clears'],
        attempts=course['attempts'],
        clear_rate=course['clear_rate_pretty'],
        likes=course['likes'],
        boos=course['boos'],
        maker=deserialize_maker(course['uploader']),
        record_holder=deserialize_maker(course['record_holder'])
    )


def deserialize_maker(maker: dict) -> Maker:
    return Maker(
        region=maker['region_name'],
        maker_id=maker['code'],
        name=maker['name'],
        country=maker['country'],
        last_active=maker['last_active_pretty'],
        mii_image_url=maker['mii_image'],
        pose_name=maker['pose_name'],
        hat_name=maker['hat_name'],
        shirt_name=maker['shirt_name'],
        pants_name=maker['pants_name'],
        courses_attempted=maker['courses_attempted'],
        courses_played=maker['courses_played'],
        courses_cleared=maker['courses_cleared'],
        courses_deaths=maker['courses_deaths'],
        likes=maker['likes'],
        maker_points=maker['maker_points'],
        easy_highscore=maker['easy_highscore'],
        normal_highscore=maker['normal_highscore'],
        expert_highscore=maker['expert_highscore'],
        super_expert_highscore=maker['super_expert_highscore'],
        versus_rating=maker['versus_rating'],
        versus_rank=maker['versus_rank_name'],
        versus_won=maker['versus_won'],
        versus_lost=maker['versus_lost'],
        versus_disconnected=maker['versus_disconnected'],
        coop_clears=maker['coop_clears'],
        coop_plays=maker['coop_plays'],
        versus_plays=maker['versus_plays'],
        versus_kills=maker['versus_kills'],
        versus_killed_by_others=maker['versus_killed_by_others'],
        uploaded_levels=maker['uploaded_levels'],
        first_clears=maker['first_clears'],
        world_records=maker['world_records'],
        super_world_clears=maker['unique_super_world_clears'],
        super_world_id=maker['super_world_id']
    )


def search_multiple_levels(api: str, count: int = 10, difficulty_id: str = 'e') -> list[Course]:
    try:
        response = requests.get(
            url=f'{TGRCODE_API}/{api}?difficulty={difficulty_id}&count={count}',
            headers={'User-Agent': USER_AGENT}
        )
    except ConnectionError as ex:
        raise TGRCodeAPIException(ex)
    try:
        courses = response.json()['courses']
    except requests.exceptions.JSONDecodeError:
        raise TGRCodeAPIException(response.text)
    ret: list[Course] = []
    for course in courses:
        ret.append(deserialize_course(course))
    return ret


def search_endless_mode(count: int = 10, difficulty_id: str = 'e') -> list[Course]:
    try:
        return search_multiple_levels('search_endless_mode', count, difficulty_id)
    except TGRCodeAPIException as ex:  # pass exception
        raise TGRCodeAPIException(ex)


def search_popular(count: int = 10, difficulty_id: str = 'e') -> list[Course]:
    try:
        return search_multiple_levels('search_popular', count, difficulty_id)
    except TGRCodeAPIException as ex:  # pass exception
        raise TGRCodeAPIException(ex)


def level_data_dataid(data_id: int) -> bytes:
    try:
        response = requests.get(
            url=f'{TGRCODE_API}/level_data_dataid/{data_id}',
            headers={'User-Agent': USER_AGENT}
        )
        if response.status_code == 200:
            return response.content
        else:
            raise TGRCodeAPIException(response.text)
    except Exception as ex:  # pass exception
        raise TGRCodeAPIException(ex)


def level_info(course_id: str) -> Course:
    try:
        response = requests.get(
            url=f'{TGRCODE_API}/level_info/{normalize_course_id(course_id)}',
            headers={'User-Agent': USER_AGENT}
        )
        response_json = response.json()
        if 'error' in response_json:
            raise TGRCodeAPIException(response_json['error'])
        return deserialize_course(response_json)
    except (TGRCodeAPIException, ConnectionError) as ex:  # pass exception
        raise TGRCodeAPIException(ex)


def user_info(maker_id: str) -> Maker:
    try:
        response = requests.get(
            url=f'{TGRCODE_API}/user_info/{normalize_course_id(maker_id)}',
            headers={'User-Agent': USER_AGENT}
        )
        response_json = response.json()
        if 'error' in response_json:
            raise TGRCodeAPIException(response_json['error'])
        return deserialize_maker(response_json)
    except (TGRCodeAPIException, ConnectionError) as ex:  # pass exception
        raise TGRCodeAPIException(ex)


def super_world(super_world_id: str) -> list[Course]:
    response = requests.get(
        url=f'{TGRCODE_API}/super_world/{super_world_id}',
        headers={'User-Agent': USER_AGENT}
    )
    try:
        courses = response.json()['courses']
    except requests.exceptions.JSONDecodeError:
        raise TGRCodeAPIException(response.text)
    ret: list[Course] = []
    for course in courses:
        ret.append(deserialize_course(course))
    return ret
