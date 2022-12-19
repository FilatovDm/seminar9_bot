from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from random import randrange

del_words = 'абв'
n = randrange(100, 500)
k = randrange(10, 30)
name_0 = "Игрок 1"
name_1 = "Умный БОТ"
order = bool(randrange(2))


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    input_words = update.message.text.split()[1:]
    print(input_words)
    await update.message.reply_text(" ".join(filter(lambda x: not all(char in x for char in del_words), input_words)))


def candy_down(take):
    global n
    n -= take


async def move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    our_move = int(update.message.text.split()[1])
    if 1 <= our_move <= k:
        candy_down(our_move)
        await update.message.reply_text(f"Осталось конфет {n}")
        x = n % (k + 1)
        m = x if x else 1
        await update.message.reply_text(f"Бот взял {m} конфет")
        candy_down(m)
        await update.message.reply_text(f"Осталось конфет {n}")
        await update.message.reply_text(f"Введите количество конфет")
    else:
        await update.message.reply_text("Не верное количество")
        await update.message.reply_text(f"Можно взять от 1 до {k}")

    # n -= our_move
    # if n:
    #     order = not order
    # else:
    #     game = False
    #  await update.message.reply_text()


# await update.message.reply_text(f"Выиграл {name_1 if order else name_0}")


async def candy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global n, k, name_0, name_1, order

    """"Игра с умным ботом"""
    candy_max = k if k < n else n
    await update.message.reply_text(f"Ход делает {name_1 if order else name_0}")
    await update.message.reply_text(f"На столе {n} конфет")
    await update.message.reply_text(f"Можно взять от 1 до {candy_max}")

    if order:
        x = n % (candy_max + 1)
        m = x if x else 1
        await update.message.reply_text(f"Бот взял {m} конфет")
        candy_down(m)
        await update.message.reply_text(f"Осталось конфет {n}")
    else:
        await update.message.reply_text(f"Введите количество конфет")


bot_token = "5781169536:AAFhBvtCoxM1IcAqCek0PARvs9R9pZlDBVo"
app = ApplicationBuilder().token(bot_token).build()

app.add_handler(CommandHandler("start", hello))
app.add_handler(CommandHandler("del", words))
app.add_handler(CommandHandler("game", candy))
app.add_handler(CommandHandler("move", move))

app.run_p