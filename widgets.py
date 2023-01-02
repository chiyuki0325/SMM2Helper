from webview import Window
from urllib.parse import quote


def quote_vars(*args):
    return map(quote, args)


# ----

def insert_my_course(window: Window, course_title: str, course_desc: str, idx: int):
    course_title, course_desc = quote_vars(course_title, course_desc)
    window.evaluate_js(f"insertMyCourse(decodeURIComponent('{course_title}'),"
                       f"decodeURIComponent('{course_desc}'),"
                       f"{idx});")


def insert_online_course(window: Window, course_title: str, course_desc: str, idx: int):
    course_title, course_desc = quote_vars(course_title, course_desc)
    window.evaluate_js(f"insertOnlineCourse(decodeURIComponent('{course_title}'),"
                       f"decodeURIComponent('{course_desc}'),"
                       f"{idx});")


def clear_online_course(window: Window):
    window.evaluate_js("clearOnlineCourse();")


def clear_tabs_state(window: Window):
    window.evaluate_js("document.getElementById('tabs').removeAttribute('state');")


def show_error_message(window: Window, error_message: str):
    window.evaluate_js(f"showErrorMessage('{error_message}')")


def show_dialog(window: Window,
                title: str, content: str, yes_visible: bool = True,
                yes_text: str = "Yes", no_visible: bool = True, no_text: str = "No",
                dialog_callback_id: str = 'default'):
    title, content, yes_text, no_text = quote_vars(title, content, yes_text, no_text)
    window.evaluate_js(f"showDialog(decodeURIComponent('{title}'),"
                       f"decodeURIComponent('{content}'),"
                       f"'{str(yes_visible).lower()}',"
                       f"decodeURIComponent('{yes_text}'),"
                       f"'{str(no_visible).lower()}',"
                       f"decodeURIComponent('{no_text}'),"
                       f"{dialog_callback_id};")
