import webview
from urllib.parse import quote


def insert_my_course(window: webview.Window, course_title: str, course_desc: str):
    course_title = quote(course_title)
    course_desc = quote(course_desc)
    window.evaluate_js(f"insertMyCourse(decodeURIComponent('{course_title}'),"
                       f"decodeURIComponent('{course_desc}'));")


def insert_online_course(window: webview.Window, course_title: str, course_desc: str):
    course_title = quote(course_title)
    course_desc = quote(course_desc)
    window.evaluate_js(f"insertOnlineCourse(decodeURIComponent('{course_title}'),"
                       f"decodeURIComponent('{course_desc}'));")


def clear_online_course(window: webview.Window):
    window.evaluate_js("clearOnlineCourse();")
