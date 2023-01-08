#!/usr/bin/env bash

mkdir -p web/res; pushd web/res || exit

for url in "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Person/SVG/ic_fluent_person_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Edit/SVG/ic_fluent_edit_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Clock/SVG/ic_fluent_clock_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Brightness High/SVG/ic_fluent_brightness_high_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Text Bullet List Tree/SVG/ic_fluent_text_bullet_list_tree_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Ribbon/SVG/ic_fluent_ribbon_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Ribbon Star/SVG/ic_fluent_ribbon_star_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Heart/SVG/ic_fluent_heart_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Heart Broken/SVG/ic_fluent_heart_broken_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Number Symbol/SVG/ic_fluent_number_symbol_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Tag/SVG/ic_fluent_tag_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Search/SVG/ic_fluent_search_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/People Search/SVG/ic_fluent_people_search_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Map/SVG/ic_fluent_map_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Phone Screen Time/SVG/ic_fluent_phone_screen_time_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Location/SVG/ic_fluent_location_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Location Dismiss/SVG/ic_fluent_location_dismiss_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/WiFi Off/SVG/ic_fluent_wifi_off_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/People Team Add/SVG/ic_fluent_people_team_add_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/People Team Delete/SVG/ic_fluent_people_team_delete_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Games/SVG/ic_fluent_games_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Cellular Data 1/SVG/ic_fluent_cellular_data_1_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Cellular Data 2/SVG/ic_fluent_cellular_data_2_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Cellular Data 3/SVG/ic_fluent_cellular_data_3_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Cellular Data 4/SVG/ic_fluent_cellular_data_4_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Send Copy/SVG/ic_fluent_send_copy_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Book Coins/SVG/ic_fluent_book_coins_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Book Number/SVG/ic_fluent_book_number_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Fast Acceleration/SVG/ic_fluent_fast_acceleration_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Accessibility/SVG/ic_fluent_accessibility_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Hat Graduation/SVG/ic_fluent_hat_graduation_20_regular.svg" \
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Presenter/SVG/ic_fluent_presenter_20_regular.svg"
do
  if ! [ -f "$(basename "$url")" ]; then
    wget "$url"
  fi
done

popd || exit