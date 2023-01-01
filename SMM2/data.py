import enum

TILE_WIDTHS = {"M1": 16, "M3": 16, "MW": 16, "WU": 64, "3W": 64}

ACTOR_COUNT = 2600

ACTOR_CATEGORIES = [
    "Terrain",
    "Items",
    "Enemies",
    "Gizmos"
]

PLAYER_NAMES = {
    "Mario":"Mario",
    "Luigi":"Luigi",
    "Toad":"Kinopio",
    "Toadette":"Kinopico"
}

GAME_STYLE_NAMES = {
    "M1":"Super Mario Bros.",
    "M3":"Super Mario Bros. 3",
    "MW":"Super Mario World",
    "WU":"New Super Mario Bros. U",
    "3W":"Super Mario 3D World"
}

COURSE_THEME_NAMES = [
    "Ground",
    "Underground",
    "Castle",
    "Airship",
    "Underwater",
    "Ghost House",
    "Snow",
    "Desert",
    "Sky",
    "Forest"
]

WORLD_THEME_NAMES = [
    "Ground",
    "Underground",
    "Desert",
    "Snow",
    "Sky",
    "Forest",
    "Volcano",
    "Space"
]

SPEED_NAMES  = [
    "None",
    "Slow",
    "Normal",
    "Fast",
    "Custom"
]

MOTION_NAMES = [
    "None",
    "OneWay",
    "TwoWay"
]

CC_CATEGORY_NAMES  = [
    "None",
    "Parts",
    "Status",
    "Action"
]

CC_HASHES = [
    0xDFA2AFF1,
    0x7F07ACBF,
    0xC77685E8,
    0xCCE12A46,
    0xC7DAD20F,
    0x4B115542,
    0xDF6717DE,
    0xE50302F7,
    0xCE9A707B,
    0xE47C2BE8,
    0xE25C5F60,
    0x563755F2,
    0xA3AEC34A,
    0x5A085610,
    0x634A6671,
    0xA09BB51F,
    0x794C6EB3,
    0x387C22CA,
    0x103BBA8C,
    0xFE75363E,
    0x4C44DA92,
    0x7A128199,
    0xCE2E5A15,
    0xCF81610A,
    0x48D111E0,
    0x7F88648A,
    0x501C7C00,
    0x756120EE,
    0xFFE76309,
    0xF571D608,
    0x66C2B75E,
    0xF0F35CBA,
    0xE3F62C75,
    0x4067AB4E,
    0x3F50B513,
    0x3F4124E8,
    0x467AFB58,
    0x4B980B7F,
    0xCA315249,
    0x3C164EB1,
    0x6DAA9A3F,
    0x405DCE65,
    0xED1023EA,
    0x62B74A93,
    0x2A8E77BB,
    0xC73BE7EC,
    0x7C8612D5,
    0x35A5AF47,
    0xBB926013,
    0x3A2F3996,
    0x7DDB5D7F,
    0xB7402052,
    0x6A1CE415,
    0x66477BE4,
    0x48B4157B,
    0x63F3D532,
    0xE6F2EEBE,
    0x553A9590,
    0x1A098D50,
    0xFAE86A49,
    0xB4FA3D4B,
    0xDE0ABFC6,
    0xD9893249,
    0x4C8772A3,
    0xDE56FFB5,
    0x97F8A309,
    0xF55B3863,
    0xC78F5040,
    0xF5B932C2,
    0xA3E39544,
    0x1664515A,
    0x08327AE6,
    0x3EAB9AA1,
    0x97F4CF7A,
    0x3AF23BDE,
    0xC2A80228,
    0xEF026A7F,
    0x46219146
]

FILE_SIZES = {
    "COURSE_DATA":0x5C000,
    "THUMBNAIL_DATA":0x1C000,
    "REPLAY_DATA":0x68000
}

COURSE_HEADER_SiZE = 0x200
COURSE_AREA_SIZE = 0x2DEE0

SAVE_COURSE_OFFSET = 0xB920

DIRECTION = {
    1:  "LEFT",
    2:  "RIGHT",
    3:  "DOWN",
    4:  "UP",
    5:  "LEFT_TO_DOWN",
    6:  "DOWN_TO_LEFT",
    7:  "LEFT_TO_UP",
    8:  "UP_TO_LEFT",
    9:  "RIGHT_TO_DOWN",
    10:  "DOWN_TO_RIGHT",
    11: "RIGHT_TO_UP",
    12: "UP_TO_RIGHT",
    13: "RIGHT_TO_END",
    14: "LEFT_TO_END",
    15: "UP_TO_END",
    16: "DOWN_TO_END"
}
