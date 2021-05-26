from datetime import time
from pytz import UTC


TELEGRAM_BOT_TOKEN = ''

MAIN_MENU_STATE, IN_GAME_STATE, SETTINGS_STATE, START_GAME, SHOW_STATS,\
    SHOW_RATING, SHOW_SETTINGS, GOOD_STRESS, BAD_STRESS, CHANGE_NOTIF_SETTING,\
    CHANGE_SHOW_IN_RATING_SETTING, GO_BACK = map(str, range(12))

MAIN_MENU_TEXT = ('Привет! Этот бот поможет тебе подготовиться к заданию '
                  '4 ЕГЭ по русскому языку.\nОбо всех ошибках '
                  'сообщать @rov01yp.')
NOTIFICATION_TEXT =\
    'До ЕГЭ осталось всего несколько дней, самое время практиковаться!'


NOTIFICATION_TIME = time(9, 0, 0, 0, tzinfo=UTC)


GAME_CHAT_DATA_KEYS =\
    ('score', 'not_played_word_ids', 'play_variant', 'current_word_id')
