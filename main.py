from random import choice
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import CallbackQueryHandler, ConversationHandler
import utils
from databases import Session, Word


MAIN_MENU_STATE, IN_GAME_STATE, START_GAME,\
    SHOW_STATS, SHOW_RATING, GOOD_STRESS, BAD_STRESS = map(str, range(7))
TELEGRAM_BOT_TOKEN = ""


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

ALL_WORDS = Session().query(Word).all()
print(dir(ALL_WORDS[0]), ALL_WORDS[0].word)

def start_handler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Привет! Этот бот поможет тебе подготовиться'
                              'к заданию 4 ЕГЭ по русскому языку.',
                              reply_markup=MAIN_MENU_KEYBOARD_MARKUP)

    return MAIN_MENU_STATE


def main_menu_callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == START_GAME:
        return in_game_callback_handler(update, context)
    if query.data == SHOW_STATS:
        query.edit_message_text('Показываю статистику!')
    if query.data == SHOW_RATING:
        query.edit_message_text('Показываю рейтинг!')

    return MAIN_MENU_STATE


def in_game_callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if 'play_variant' in context.chat_data:
        if query.data == context.chat_data['play_variant'][1]:
            context.chat_data['score'] += 1
        else:
            query.edit_message_text(f'Неправильно! Правильный вариант ударения: {context.chat_data["current_word"].word}\nВаш итоговый счёт: {context.chat_data["score"]}.',
                    reply_markup=MAIN_MENU_KEYBOARD_MARKUP)

            del context.chat_data['score']
            del context.chat_data['not_played_words']
            del context.chat_data['play_variant']
            del context.chat_data['current_word']
            return MAIN_MENU_STATE
        query.answer()
    else:
        #  Straight from the main menu
        context.chat_data['not_played_words'] = ALL_WORDS.copy()
        context.chat_data['score'] = 0

    if not context.chat_data['not_played_words']:
        query.edit_message_text(f'Поздравляем! Вы ответили на все вопросы правильно!\nВаш итоговый счёт: {context.chat_data["score"]}',
                reply_markup=MAIN_MENU_KEYBOARD_MARKUP)
        del context.chat_data['score']
        del context.chat_data['not_played_words']
        del context.chat_data['play_variant']
        del context.chat_data['current_word']
        return MAIN_MENU_STATE

    context.chat_data['current_word'] = utils.get_word(context.chat_data['not_played_words'])
    context.chat_data['play_variant'] = choice([
        (context.chat_data['current_word'].word, GOOD_STRESS),
        (context.chat_data['current_word'].bad_variant, BAD_STRESS),
    ])
    query.edit_message_text(
        f'Очков: {context.chat_data["score"]}\nПравильно ли стоит ударение в слове: "{context.chat_data["play_variant"][0]}"?',
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