#!/usr/bin/env bash

mkdir -p web/res; pushd web/res

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
           "https://cdn.jsdelivr.net/gh/microsoft/fluentui-system-icons@main/assets/Tag/SVG/ic_fluent_tag_20_regular.svg"
do
  if ! [ -f "$(basename "$url")" ]; then
    wget "$url"
  fi
done

popd