const dialogCallback = {}

function finishResponse(response) {
    console.log('jsbridge response:' + response.message)
}

function GenerateCourseEntry(course_title, course_desc, course_idx) {
    const entry = document.createElement('li');
    entry.setAttribute('class', 'entry');
    entry.setAttribute('onclick', 'activeEntry(this)');
    const courseTitle = document.createElement('div');
    courseTitle.setAttribute('class', 'course-title text-limited');
    courseTitle.innerText = course_title;
    const courseDesc = document.createElement('div');
    courseDesc.setAttribute('class', 'course-desc text-limited');
    courseDesc.innerText = course_desc;
    const entryContent = document.createElement('div');
    entryContent.setAttribute('class', 'entry-content');
    entryContent.appendChild(courseTitle);
    entryContent.appendChild(courseDesc);
    entry.setAttribute('idx', course_idx);
    entry.appendChild(entryContent);
    return entry;
}

function insertMyCourse(course_title, course_desc, course_idx) {
    const entry = GenerateCourseEntry(course_title, course_desc, course_idx);
    document.getElementById('local-courses').appendChild(entry);
}

function insertOnlineCourse(course_title, course_desc, course_idx) {
    const entry = GenerateCourseEntry(course_title, course_desc, course_idx);
    document.getElementById('online-courses').appendChild(entry);
}

function activeEntry(obj) {
    Array.from(
        document.getElementsByClassName('entry')
    ).forEach(
        function (element) {
            element.setAttribute('class', 'entry');
        }
    )
    pywebview.api.handle_entry_click(obj.parentNode.id, obj.getAttribute('idx')).then(
        () => {
            obj.setAttribute('class', 'entry entry-active')
        }
    );
}

function activeTab(obj) {
    const tabs = document.getElementById('tabs');
    if (tabs.getAttribute('state') === 'loading') {
        return;
    }
    tabs.setAttribute('state', 'loading');
    Array.from(
        document.getElementsByClassName('tab')
    ).forEach(
        function (element) {
            element.setAttribute('class', 'tab');
        }
    )
    obj.setAttribute('class', 'tab tab-active');
    pywebview.api.handle_tab_active(obj.id).then(() => tabs.removeAttribute('state'), (err) => showErrorMessage(err))
}

function showMessage(message_content, message_type) {
    const float = document.getElementById('float')
    const message = document.createElement('div');
    const messageId = message_type + '-' + parseInt((Math.random() * 100).toString());
    message.setAttribute('id', messageId);
    message.setAttribute('class', `message ${message_type}`);
    message.setAttribute('onclick', `hideMessage('${messageId}');`);
    message.innerText = message_content;
    float.appendChild(message);
    message.style.opacity = '1';
    message.style.transform = 'scaleY(1)';
    setTimeout(() => hideMessage(messageId), 3000);
}

function hideMessage(messageId) {
    const message = document.getElementById(messageId)
    message.style.opacity = '0';
    message.style.transform = 'scaleY(0)';
    setTimeout(() => {
        message.remove()
    }, 305);
}

function showErrorMessage(message) {
    console.error(message);
    showMessage(message, 'error-message');
}

function showInfoMessage(message) {
    console.log(message);
    showMessage(message, 'info-message');
}

function showSuccessMessage(message) {
    console.log(message);
    showMessage(message, 'success-message');
}

function clearOnlineCourse() {
    document.getElementById('online-courses').innerHTML = '';
}

function switchRandom(obj) {
    const tabs = document.getElementById('tabs');
    if (tabs.getAttribute('state') === 'loading') {
        return;
    }
    pywebview.api.handle_switch_random().then(
        (is_random) => {
            obj.innerText = is_random ? 'Random' : 'Popular';
            activeTab(document.getElementsByClassName('tab-active')[0]);
        }
    );
}

function fillInnerText(id, content) {
    document.getElementById(id).innerText = content;
}

function showDialog(title, content, yes_visible, yes_text, no_visible, no_text, dialog_callback_id) {
    delete dialogCallback[dialog_callback_id];
    document.getElementById('dialog-bg').style.visibility = 'visible';
    document.getElementById('dialog-box').style.opacity = '1';
    fillInnerText('dialog-title', title);
    fillInnerText('dialog-content', content);
    const button_yes = document.getElementById('dialog-button-yes');
    button_yes.setAttribute('onclick', `dialogButtonCallback(true, '${dialog_callback_id}');`)
    button_yes.setAttribute('callback-id', dialog_callback_id);
    const button_no = document.getElementById('dialog-button-no');
    button_no.setAttribute('onclick', `dialogButtonCallback(false, '${dialog_callback_id}');`)
    button_no.setAttribute('callback-id', dialog_callback_id);
    if (yes_visible) {
        button_yes.style.visibility = 'visible';
        button_yes.innerText = yes_text;
    } else {
        button_yes.style.visibility = 'hidden';
    }
    if (no_visible) {
        button_no.style.visibility = 'visible';
        button_no.innerText = no_text;
    } else {
        button_no.style.visibility = 'hidden';
    }
}

function dialogButtonCallback(is_yes_button, dialog_callback_id) {
    document.getElementById('dialog-bg').style.visibility = 'hidden';
    document.getElementById('dialog-box').style.opacity = '0';
    dialogCallback[dialog_callback_id] = is_yes_button;
}

function showOnlineCourseDetails(idx, name, description, uploaded_date, course_id, data_id, game_style, theme,
                                 difficulty, tag_1, tag_2, world_record, upload_time, clears, attempts, clear_rate,
                                 likes, boos, maker_name, maker_id, record_holder, record_holder_id, small_img_url,
                                 full_img_url) {
    const onlineCourses = document.getElementById('online-courses');
    onlineCourses.style.opacity = '0';
    onlineCourses.style.height = '0';
    setTimeout(() => {
        onlineCourses.style.visibility = 'hidden';
    }, 200);
    const onlineCourse = document.getElementById('online-course');
    onlineCourse.setAttribute('idx', idx);
    onlineCourse.setAttribute('data-id', data_id);
    fillInnerText('details-course-title', name);
    fillInnerText('details-course-description', description);
    document.getElementById('details-course-description').setAttribute('title', description);
    fillInnerText('details-course-maker', maker_name);
    document.getElementById('details-course-maker').setAttribute('title', maker_id);
    fillInnerText('details-course-maker-time', upload_time);
    fillInnerText('details-course-upload-time', uploaded_date);
    fillInnerText('details-course-id', course_id);
    fillInnerText('details-course-game-style', game_style);
    fillInnerText('details-course-theme-name', theme);
    fillInnerText('details-course-difficulty', difficulty);
    fillInnerText('details-course-clear-rate', clear_rate);
    fillInnerText('details-course-clears', clears);
    fillInnerText('details-course-attempts', attempts);
    fillInnerText('details-course-likes', likes);
    fillInnerText('details-course-boos', boos);
    fillInnerText('details-course-record-holder', record_holder);
    document.getElementById('details-course-record-holder').setAttribute('title', record_holder_id);
    fillInnerText('details-course-record-time', world_record);
    fillInnerText('details-course-tag-1', tag_1);
    fillInnerText('details-course-tag-2', tag_2);
    document.getElementById('details-img').setAttribute('src', small_img_url);
    document.getElementById('details-img-full').setAttribute('src', full_img_url);
    onlineCourse.style.visibility = 'visible';
    onlineCourse.style.height = '';
    onlineCourse.style.opacity = '1';
}

function copyText(text) {
    pywebview.api.handle_copy_text(text).then(() => console.log('Copy ' + text), (err) => showErrorMessage(err))
}

function openLink(link) {
    pywebview.api.handle_open_link(link).then(() => console.log('Opened link ' + text), (err) => showErrorMessage(err))
}

function backToOnlineCourseList() {
    const onlineCourses = document.getElementById('online-courses');
    const onlineCourse = document.getElementById('online-course');
    onlineCourse.style.opacity = '0';
    onlineCourse.style.height = '0';
    setTimeout(() => {
        onlineCourse.style.visibility = 'hidden';
    }, 200);
    onlineCourses.style.visibility = 'visible';
    onlineCourses.style.height = '';
    onlineCourses.style.opacity = '1';
}

async function downloadCourseToSlot() {
    let idx, slotTitle;
    try {
        const activeSlot = document.getElementById('local-courses').getElementsByClassName('entry-active')[0];
        idx = activeSlot.getAttribute('idx');
        slotTitle = activeSlot.firstChild.firstChild.innerText;
        if (slotTitle === '(Empty Slot)') {
            showErrorMessage('Cannot download to empty slot. You can only replace existing courses.');
            return
        }
    } catch {
        showErrorMessage('Please select a local slot first.');
        return
    }
    const dataId = document.getElementById('online-course').getAttribute('data-id');
    showDialog('Download Course',
        `Download "${document.getElementById('details-course-title').innerText}" (${document.getElementById('details-course-id').innerText}) ` +
        `to slot #${idx} and replace "${slotTitle}"？`, true, 'Yes', true, 'No', 'download-course'
    )
    while (dialogCallback.hasOwnProperty('download-course')) {
        await null;
    }
    if (dialogCallback['download-course'] === true) {
        pywebview.api.handle_download_course_to_slot(idx, dataId).then(
            () => console.log(`Downloading ${dataId} to slot ${idx}`),
            (err) => showErrorMessage(err)
        )
    }
    delete dialogCallback['download-course']
}