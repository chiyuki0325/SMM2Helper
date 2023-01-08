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
    entry.setAttribute('data-idx', course_idx);
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
    pywebview.api.handle_entry_click(obj.parentNode.id, obj.getAttribute('data-idx')).then(
        () => {
            obj.setAttribute('class', 'entry entry-active')
        }
    );
}

function activeTab(obj) {
    const tabs = document.getElementById('tabs');
    if (tabs.getAttribute('data-state') === 'loading') {
        return;
    }
    tabs.setAttribute('data-state', 'loading');
    Array.from(
        document.getElementsByClassName('tab')
    ).forEach(
        function (element) {
            element.setAttribute('class', 'tab');
        }
    )
    obj.setAttribute('class', 'tab tab-active');
    pywebview.api.handle_tab_active(obj.id).then(() => tabs.removeAttribute('data-state'), (err) => showErrorMessage(err))
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
    tabs.removeAttribute('data-state');
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

function clearLocalCourse() {
    document.getElementById('local-courses').innerHTML = '';
}

function switchRandom(obj) {
    const tabs = document.getElementById('tabs');
    if (tabs.getAttribute('data-state') === 'loading') {
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

function showDialog(title, content, yes_visible, yes_text, no_visible, no_text, dialog_callback_id, dialog_callback_object) {
    document.getElementById('dialog-bg').style.visibility = 'visible';
    document.getElementById('dialog-box').style.opacity = '1';
    fillInnerText('dialog-title', title);
    fillInnerText('dialog-content', content);
    const button_yes = document.getElementById('dialog-button-yes');
    const onclick_function = `dialogButtonCallback(true, '${dialog_callback_id}', '${encodeURIComponent(JSON.stringify(dialog_callback_object))}');`;
    button_yes.setAttribute('onclick', onclick_function)
    const button_no = document.getElementById('dialog-button-no');
    button_no.setAttribute('onclick', onclick_function)
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

function dialogButtonCallback(value, dialog_callback_id, dialog_callback_object) {
    const callback = JSON.parse(decodeURIComponent(dialog_callback_object))
    document.getElementById('dialog-bg').style.visibility = 'hidden';
    document.getElementById('dialog-box').style.opacity = '0';
    switch (dialog_callback_id) {
        case 'download-course':
            if (value === true) {
                pywebview.api.handle_download_course_to_slot(callback.data_id, callback.idx).then(
                    () => console.log(`Downloading ${callback.data_id} to slot ${callback.idx}`),
                    (err) => showErrorMessage(err)
                )
            }
            break;
    }
}

function showOnlineCourseDetails(idx, name, description, uploaded_date, course_id, data_id, game_style, theme,
                                 difficulty, tag_1, tag_2, world_record, upload_time, clears, attempts, clear_rate,
                                 likes, boos, maker_name, maker_id, record_holder, record_holder_id, small_img_url,
                                 full_img_url) {
    document.getElementById('details-img').setAttribute('src', '');
    document.getElementById('details-img-full').setAttribute('src', '');
    const tabs = document.getElementById('tabs');
    tabs.setAttribute('data-state', 'loading');
    const onlineCourses = document.getElementById('online-courses');
    onlineCourses.style.opacity = '0';
    onlineCourses.style.height = '0';
    setTimeout(() => {
        onlineCourses.style.visibility = 'hidden';
    }, 200);
    const onlineCourse = document.getElementById('online-course');
    onlineCourse.setAttribute('data-idx', idx);
    onlineCourse.setAttribute('data-data-id', data_id);
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
    pywebview.api.handle_set_subtitle();
    const tabs = document.getElementById('tabs');
    tabs.removeAttribute('data-state')
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

function downloadCourseToSlot() {
    if (pywebview.api.downloading) {
        showInfoMessage('Another download is in progress, please wait ...');
        return
    }
    let idx, slotTitle;
    try {
        const activeSlot = document.getElementById('local-courses').getElementsByClassName('entry-active')[0];
        idx = activeSlot.getAttribute('data-idx');
        slotTitle = activeSlot.firstChild.firstChild.innerText;
        if (slotTitle === '(Empty Slot)') {
            showErrorMessage('Cannot download to empty slot. You can only replace existing courses.');
            return
        }
    } catch {
        showErrorMessage('Please select a local slot first.');
        return
    }
    const dataId = document.getElementById('online-course').getAttribute('data-data-id');
    showDialog('Download Course',
        `Download "${document.getElementById('details-course-title').innerText}" (${document.getElementById('details-course-id').innerText}) ` +
        `to slot #${idx} and replace "${slotTitle}"？`, true, 'Yes', true, 'No', 'download-course',
        {'data_id': dataId, 'idx': idx}
    )
}

function searchCourse() {
    const tabs = document.getElementById('tabs');
    if (tabs.getAttribute('data-state') === 'loading') {
        return;
    }
    tabs.setAttribute('data-state', 'loading');
    const course_id = prompt('Enter course ID:');
    showInfoMessage("Searching course...")
    pywebview.api.handle_search_course(course_id);
}


function showOnlineMakerDetails(name, region, maker_id, country, last_active, mii_image_url, pose_name,
                                hat_name, shirt_name, pants_name, courses_played, courses_attempted, courses_cleared,
                                courses_deaths, likes, maker_points, easy_highscore, normal_highscore, expert_highscore,
                                super_expert_highscore, versus_rating, versus_rank, versus_plays, versus_won, versus_lost,
                                versus_disconnected, coop_clears, coop_plays, versus_kills, versus_killed_by_others,
                                uploaded_levels, first_clears, world_records, super_world_clears, super_world_id) {
    const tabs = document.getElementById('tabs');
    tabs.setAttribute('data-state', 'loading');
    const onlineCourses = document.getElementById('online-courses');
    onlineCourses.style.opacity = '0';
    onlineCourses.style.height = '0';
    setTimeout(() => {
        onlineCourses.style.visibility = 'hidden';
    }, 200);
    const onlineCourse = document.getElementById('online-course');
    onlineCourse.style.opacity = '0';
    onlineCourse.style.height = '0';
    setTimeout(() => {
        onlineCourse.style.visibility = 'hidden';
    }, 200);
    document.getElementById('details-mii-img').setAttribute('src', '');
    const onlineMaker = document.getElementById('online-maker');
    onlineMaker.setAttribute('data-super-world-id', super_world_id);
    fillInnerText('details-maker-name', name);
    fillInnerText('details-maker-id', maker_id);
    fillInnerText('details-maker-region', region);
    fillInnerText('details-maker-country', country);
    fillInnerText('details-maker-last-active', last_active);
    fillInnerText('details-maker-uploaded-courses', uploaded_levels);
    fillInnerText('details-maker-likes', likes);
    fillInnerText('details-maker-points', maker_points);
    fillInnerText('details-maker-course-played', courses_played);
    fillInnerText('details-maker-course-attempted', courses_attempted);
    fillInnerText('details-maker-course-cleared', courses_cleared);
    fillInnerText('details-maker-course-deaths', courses_deaths);
    fillInnerText('details-maker-first-clears', first_clears);
    fillInnerText('details-maker-world-records', world_records);
    fillInnerText('details-maker-super-world-clears', super_world_clears);
    fillInnerText('details-maker-mii-pose', pose_name);
    fillInnerText('details-maker-mii-hat', hat_name);
    fillInnerText('details-maker-mii-shirt', shirt_name);
    fillInnerText('details-maker-mii-pants', pants_name);
    fillInnerText('details-maker-endless-e', easy_highscore);
    fillInnerText('details-maker-endless-n', normal_highscore);
    fillInnerText('details-maker-endless-ex', expert_highscore);
    fillInnerText('details-maker-endless-sex', super_expert_highscore);
    fillInnerText('details-maker-vs-rank', versus_rank);
    fillInnerText('details-maker-vs-rating', versus_rating);
    fillInnerText('details-maker-vs-plays', versus_plays);
    fillInnerText('details-maker-vs-won', versus_won);
    fillInnerText('details-maker-vs-lost', versus_lost);
    fillInnerText('details-maker-vs-disconnected', versus_disconnected);
    fillInnerText('details-maker-vs-kills', versus_kills);
    fillInnerText('details-maker-vs-killed-by-others', versus_killed_by_others);
    fillInnerText('details-maker-coop-plays', coop_plays);
    fillInnerText('details-maker-coop-won', coop_clears);
    document.getElementById('details-mii-img').setAttribute('src', mii_image_url);
    onlineMaker.style.visibility = 'visible';
    onlineMaker.style.height = '';
    onlineMaker.style.opacity = '1';
}

function showCurrentCourseMakerDetails() {   // show maker details of displaying course
    pywebview.api.is_maker_search = false;
    pywebview.api.handle_course_maker_details();
}

function backFromMakerDetails() {
    const onlineMaker = document.getElementById('online-maker');
    onlineMaker.style.opacity = '0';
    onlineMaker.style.height = '0';
    setTimeout(() => {
        onlineMaker.style.visibility = 'hidden';
    }, 200);
    if (pywebview.api.is_maker_search) {
        pywebview.api.handle_set_subtitle();  // TODO
        const tabs = document.getElementById('tabs');
        tabs.removeAttribute('data-state')
        const onlineCourses = document.getElementById('online-courses');
        onlineCourses.style.visibility = 'visible';
        onlineCourses.style.height = '';
        onlineCourses.style.opacity = '1';
    } else {
        pywebview.api.handle_set_subtitle(pywebview.api.cached_course_name);
        const onlineCourse = document.getElementById('online-course');
        onlineCourse.style.visibility = 'visible';
        onlineCourse.style.height = '';
        onlineCourse.style.opacity = '1';
    }
    document.getElementById('right-card').scrollTop = 0;
}