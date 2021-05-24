from typing import Union
from random import choice
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import CallbackQueryHandler, ConversationHandler
import utils
from models import Session, Word, User


MAIN_MENU_STATE, IN_GAME_STATE, START_GAME,\
    SHOW_STATS, SHOW_RATING, GOOD_STRESS, BAD_STRESS = map(str, range(7))
TELEGRAM_BOT_TOKEN = ''


MAIN_MENU_KEYBOARD = [
    [
        InlineKeyboardButton('Начать игру', callback_data=START_GAME),
        InlineKeyboardButton('Статистика', callback_data=SHOW_STATS),
    ],
    [
        InlineKeyboardButton('Рейтинг', callback_data=SHOW_RATING),
    ],
]
MAIN_MENU_KEYBOARD_MARKUP = InlineKeyboardMarkup(MAIN_MENU_KEYBOARD)


GAME_KEYBOARD = [
    [
        InlineKeyboardButton('Правильно', callback_data=GOOD_STRESS),
        InlineKeyboardButton('Неправильно', callback_data=BAD_STRESS),
    ],
]
GAME_KEYBOARD_MARKUP = InlineKeyboardMarkup(GAME_KEYBOARD)


__TMP_SESS = Session()
WORDS = dict((word.id, (word.word, word.bad_variant))
             for word in __TMP_SESS.query(Word).all())
__TMP_SESS.close()


def start_handler(update: Update, _: CallbackContext) -> MAIN_MENU_STATE:
    update.message.reply_text('Привет! Этот бот поможет тебе подготовиться'
                              'к заданию 4 ЕГЭ по русскому языку.\n'
                              'Обо всех ошибках сообщать @rov01yp.',
                              reply_markup=MAIN_MENU_KEYBOARD_MARKUP)

    return MAIN_MENU_STATE


def main_menu_callback_handler(update: Update, context: CallbackContext)\
        -> Union[MAIN_MENU_STATE, IN_GAME_STATE]:
    query = update.callback_query
    query.answer()

    if query.data == START_GAME:
        return in_game_callback_handler(update, context)
    if query.data == SHOW_STATS:
        query.edit_message_text('Показываю статистику!',
                                reply_markup=MAIN_MENU_KEYBOARD_MARKUP)
    elif query.data == SHOW_RATING:
        query.edit_message_text('Показываю рейтинг!',
                                reply_markup=MAIN_MENU_KEYBOARD_MARKUP)

    return MAIN_MENU_STATE


def in_game_callback_handler(update: Update, context: CallbackContext)\
        -> Union[MAIN_MENU_STATE, IN_GAME_STATE]:
    query = update.callback_query
    query.answer()

    if 'play_variant' in context.chat_data:
        session = Session()
        user = session.query(User).get(query.from_user.id)
        word_id = context.chat_data['current_word_id']
        word = session.query(Word).get(word_id)

        if query.data == context.chat_data['play_variant']['stress_state']:
            context.chat_data['score'] += 1
            user.update_stats(word_id, True)
            word.update_stats(True)
            session.commit()
            session.close()
        else:
            score = context.chat_data['score']

            query.edit_message_text(
                'Неправильно! Правильный вариант '
                f'ударения: "{word.word}".\n'
                f'Ваш итоговый счёт: {score}.',
                reply_markup=MAIN_MENU_KEYBOARD_MARKUP,
            )

            user.update_best_score(score)
            user.update_stats(word_id, False)
            word.update_stats(False)
            session.commit()
            session.close()

            del context.chat_data['score']
            del context.chat_data['not_played_word_ids']
            del context.chat_data['play_variant']
            del context.chat_data['current_word_id']

            return MAIN_MENU_STATE
    else:
        #  Straight from the main menu
        session = Session()

        user = session.query(User).get(query.from_user.id)
        if user is None:
            user = User(query.from_user.id, query.from_user.first_name)
            session.add(user)
        user.total_games += 1

        session.commit()
        session.close()

        context.chat_data['not_played_word_ids'] = set(WORDS.keys())
        context.chat_data['score'] = 0

    if not context.chat_data['not_played_word_ids']:
        query.edit_message_text(
            'Поздравляем! Вы ответили на все вопросы правильно!\n'
            f'Ваш итоговый счёт: {context.chat_data["score"]}.',
            reply_markup=MAIN_MENU_KEYBOARD_MARKUP,
        )

        session = Session()
        user = session.query(User).get(query.from_user.id)
        user.update_best_score(score)
        session.commit()
        session.close()

        del context.chat_data['score']
        del context.chat_data['not_played_word_ids']
        del context.chat_data['play_variant']
        del context.chat_data['current_word_id']
        return MAIN_MENU_STATE

    current_word_id =\
        utils.get_word_id(context.chat_data['not_played_word_ids'])
    context.chat_data['current_word_id'] = current_word_id
    context.chat_data['play_variant'] = choice([
        {
            'word': WORDS[current_word_id][0],
            'stress_state': GOOD_STRESS
        },
        {
            'word': WORDS[current_word_id][1],
            'stress_state': BAD_STRESS
        },
    ])
    query.edit_message_text(
        f'Очков: {context.chat_data["score"]}.\n'
        'Правильно ли стоит ударение в слове: '
        f'"{context.chat_data["play_variant"]["word"]}"?',
        reply_markup=GAME_KEYBOARD_MARKUP
    )
    return IN_GAME_STATE


def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    main_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            MAIN_MENU_STATE:
                [CallbackQueryHandler(main_menu_callback_handler)],
            IN_GAME_STATE:
                [CallbackQueryHandler(in_game_callback_handler)],
        },
        fallbacks=[],
        allow_reentry=True,
    )
    dispatcher.add_handler(main_conversation_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
