import logging
import time
from telegram import Bot
from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler

from telegram.utils.request import Request
from questions import get_random_truth
from questions import get_random_dare

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

TRUTH, EVALUATION = range(1, 3)
votes_arr = []

keyboard = ReplyKeyboardMarkup([['Правда', 'Действие']])


def welcome(update: Update, context: CallbackContext):
    update.message.reply_text(text='У тебя есть секреты? Есть вещи, которые никто не знает о вас (кроме, возможно, '
                                   'вашего лучшего друга) - и которые даже заставляют ваших друзей замолчать на '
                                   'минуту - или заставляют вас смеяться? Конечно! Неважно, насколько хорошо вы '
                                   'знаете своих друзей, некоторые вещи вы просто не спрашиваете их. И это то, '
                                   'что Истина или Dare все о. Игра проста: все игроки сидят по кругу, '
                                   'и первый начинает толкать бутылку посередине одним нажатием. Узкое место теперь '
                                   'указывает на товарища по команде, а отвертка задает вопрос: правда или вызов? '
                                   'Если рассматриваемый человек выбирает правду, тот, кто перевернул бутылку, '
                                   'может задать ему вопрос, на который данное лицо должно абсолютно ответить на '
                                   'правду! С этим удовольствие от игры стоит и падает! Если ответственное лицо '
                                   'решает эту задачу, цессионарий может рассмотреть задачу, которую он теперь должен '
                                   'выполнить. Для обширных правил и больше способов игры, посмотрите на официальные '
                                   'правила Правда или действие.',
                              reply_markup=keyboard)
    return TRUTH


def get_random_truth_handler(update: Update, context: CallbackContext) -> int:
    context.user_data['id'] = update.effective_user.id
    if update.message.text.lower() == 'правда':
        update.message.reply_text(get_random_truth(), reply_markup=keyboard)
    elif update.message.text.lower() == 'действие':
        update.message.reply_text(get_random_dare(), reply_markup=keyboard)
    return EVALUATION


def evaluate(update: Update, context: CallbackContext) -> int:
    if update.effective_user.id == context.user_data['id']:
        pass
    if update.message.text == '👍':
        # votes_arr.append({'id': update.effective_user.id, 'vote': True}) if {'id': update.effective_user.id, 'vote': True} not in votes_arr else None
        update.message.reply_text(text=f'@{update.effective_user.username} твой ответ записан')
    elif update.message.text == '👎':
        # votes_arr.append({'id': update.effective_user.id, 'vote': False})
        update.message.reply_text(text=f'@{update.effective_user.username} твой ответ записан')
    else:
        update.message.reply_text('Напиши для 👍 или 👎 оценивания ответа')
    # if update.message.get_members_count() == len(votes_arr):
    #     # return VOTES


# def votes(update: Update, context: CallbackContext):
#     a = filter(lambda x: x['vote'], votes_arr)
#     b = filter(lambda x: not x['vote'], votes_arr)
#     print(a, b)
#     if len(list(a)) > len(list(b)):
#         update.message.reply_text('Задание выполнено')
#     else:
#         update.message.reply_text('Задание не выполнено')


def main():
    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0
    )
    bot = Bot(
        request=req,
        token='1192550880:AAFuQOx56LmbVJ93BUDrePwgv3qiCsNFcR4',
        base_url='https://telegg.ru/orig/bot'
    )
    updater = Updater(
        bot=bot,
        use_context=True
    )

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', welcome)
        ],
        states={
            TRUTH: [
                MessageHandler(Filters.text, get_random_truth_handler, pass_user_data=True)
            ],
            EVALUATION: [
                MessageHandler(Filters.text, evaluate, pass_user_data=True)
            ],
            # VOTES: [
            #     # MessageHandler(Filters.text, votes)
            # ]
        },
        fallbacks=[]
    )

    updater.dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
