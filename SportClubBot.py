from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bs4 import BeautifulSoup
import requests
import random
from time import sleep
from PIL import Image
from io import BytesIO
import datetime as dt

sportclubBot = Bot('puk')
sportclubBot_dispatcher = Dispatcher(sportclubBot)

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.3'
]
user_agent = random.choice(user_agent_list)
# homeMANtraining = False
# gymMANtraining = False
# homeWOMANtraining = False
# gymWOMANtraining = False

@sportclubBot_dispatcher.message_handler(commands='start')
async def startSport(message: types.Message):
    datetime = dt.datetime.now()
    time = datetime.time().strftime("%H:%M:%S")
    day = datetime.day
    month = datetime.month
    year = datetime.year
    if day < 10:
        day = '0' + str(day)
    if month < 10:
        month = '0' + str(month)
    todayIS = str(day) + '.' + str(month) + '.' + str(year)
    print(time)
    print(todayIS)

    await message.answer_sticker('CAACAgIAAxkBAAEJ6HZky8HmIkzA9KdYBydjekIKiEi89gACfhoAAvvOoUrX0Aid6OC5Xy8E')
    await message.answer('SportClubBot🥊 готов вам устроить жесткую тренировку💡' + '\n\n\n' 
                         + 'Время в данный момент⌛: ' + time + '\n\n\n' + 'Cегодняшняя дата🗓: ' + todayIS)
    await createKeyBoard_SportClub(message)

@sportclubBot_dispatcher.message_handler(content_types=types.ContentType.TEXT)
async def checkDay(message: types.Message):
    if message.text == 'Тренировки для мужчин💪':
        await manTrainings(message)
    if message.text == 'Дом🏠':
        await manHOMEtrainings(message)
    if message.text == 'Всё тело🤸🏼‍♂️':
        await bodyMANtraining(message)
    global firstday
    firstday = False
    global countsDay
    countsDay = 0
    if message.text == '1':
        countsDay += 1
        firstday = True
        print(firstday)
        if firstday:
            await firstdayBodyMan(message)
    global secondday
    secondday = False
    if message.text == '2':
        countsDay += 1
        secondday = True
        print(secondday)
        if secondday:
            await seconddayBodyMan(message)
    if message.text == 'Главное меню⛔':
        await createKeyBoard_SportClub(message)
    if message.text == 'Cледующий день🔀':
        await seconddayBodyMan(message)
    if message.text == 'Cледующее упражнение⏩':
        await changeExercise(message)



async def bodyMANtraining(message: types.Message):
    await sportclubBot.send_message(message.chat.id, 'Данная тренировка состоит из 5 дней с акцентом на всё ваше тело')
    await sportclubBot.send_message(message.chat.id, 'С какого дня вы хотите начать?')
    await daysKeyboard(message)

async def daysKeyboard(message: types.Message):
    daysKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    one = KeyboardButton('1')
    two = KeyboardButton('2')
    three = KeyboardButton('3')
    four = KeyboardButton('4')
    five = KeyboardButton('5')
    back = KeyboardButton('Главное меню⛔')
    daysKeyboard.add(one, two)
    daysKeyboard.add(three, four)
    daysKeyboard.add(five)
    daysKeyboard.add(back)
    await sportclubBot.send_message(message.chat.id, 'Если ещё не занимались, пишите 1 день, без пробелов запятых и дней только цифра', reply_markup=daysKeyboard)

async def moveKeyboard(message: types.Message):
    moveKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    next = KeyboardButton('Cледующее упражнение⏩')
    nextday = KeyboardButton('Cледующий день🔀')
    back = KeyboardButton('Главное меню⛔')
    moveKeyboard.add(next)
    moveKeyboard.add(nextday)
    moveKeyboard.add(back)
    await sportclubBot.send_message(message.chat.id, 'Как только закончите упражение, воспользуйтесь клавиатурой для перехода к следующему', reply_markup=moveKeyboard)
    
async def firstdayBodyMan(message: types.Message):
    global exercise
    exercise = 1
    bodyManLink = 'https://goodlooker.ru/trenirovki-dlja-muzhchin-na-5-dnej.html'   
    bodyManResponce = requests.get(bodyManLink, headers={'User-Agent': user_agent})
    bodyManSoup = BeautifulSoup(bodyManResponce.text, "html.parser")
    bodyTrain = bodyManSoup.find('span', style="background-color: #ffff99;").text
    print(bodyTrain)
    bodyTrainDesc = bodyManSoup.find('p', text = 'Поставьте ноги на ширине плеч, прямые руки поднимите вверх. Согните ноги в коленях, выполняя приседание до параллели с полом или немного выше. При этом руки опускайте вниз синхронно с движением ног. Вы должны двигаться так, словно находитесь в стартовой позиции перед прыжком в длину. Старайтесь приседать до параллели бедер, чтобы максимально проработать мышцы ног. Упражнение из тренировки для мужчин в домашних условиях укрепляет мышцы нижней части тела, разогревает мышцы и суставы, разгоняет кровь, настраивает на активную работу над собой.').text

    print(bodyTrainDesc)

    bodyVideoTrain = bodyManSoup.find('img', class_="aligncenter size-full wp-image-34711").get('src')
    # print(bodyVideoTrain)
    # GIF = None 
    # GIF = download_gif(bodyVideoTrain)
    bodyHowMany = bodyManSoup.find('span', style="color: #808080;").text
    print(bodyHowMany)
    await sportclubBot.send_message(message.chat.id, "Поздравляю вас с 1 днём жестких качаний")
    sleep(1)
    await sportclubBot.send_message(message.chat.id, "Приступим к началу ваших тренировок на всё тело..")
    sleep(1)
    await sportclubBot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJ8Epkz91SG63RzhpWr8e_em4-MtvtMgACKhcAAp5CoUpBBAI3Cw3Xsi8E')
    sleep(1)
    await sportclubBot.send_message(message.chat.id, bodyTrain)
    sleep(1.5)
    await sportclubBot.send_message(message.chat.id, bodyTrainDesc)
    sleep(1.5)
    await sportclubBot.send_message(message.chat.id, bodyHowMany)
    # await sportclubBot.send_message(message.chat.id, bodyVideoTrain)
    # await message.answer_animation(types.InputFile(BytesIO(GIF)))
    sleep(1)
    await sportclubBot.send_video(message.chat.id, bodyVideoTrain, None, 'Text')
    sleep(1.5)
    await moveKeyboard(message)

async def changeExercise(message: types.Message):
    if exercise == 1:
        exercise +=1
        bodyManLink = 'https://goodlooker.ru/trenirovki-dlja-muzhchin-na-5-dnej.html'   
        bodyManResponce = requests.get(bodyManLink, headers={'User-Agent': user_agent})
        bodyManSoup = BeautifulSoup(bodyManResponce.text, "html.parser")
        bodyTrain = bodyManSoup.find_all('span', style="background-color: #ffff99;")
        for i in bodyTrain:
            Exercise = i.get_text()
            if Exercise[0] == '2':
                print(Exercise)
        

async def seconddayBodyMan(message: types.Message):
    await sportclubBot.send_message(message.chat.id, "ДЕНЬ 2: Тренировка мужчин на всё тело")
    
async def createKeyBoard_SportClub(message: types.Message):
    sportClubKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    man = KeyboardButton('Тренировки для мужчин💪')
    woman = KeyboardButton('Тренировки для женщин💄')
    sportClubKeyboard.add(man)
    sportClubKeyboard.add(woman)
    await sportclubBot.send_message(message.chat.id, 'Готовы подкачаться?', reply_markup=sportClubKeyboard)
    

@sportclubBot_dispatcher.message_handler(lambda message: message.text == 'Тренировки для мужчин💪')
async def manTrainings(message: types.Message):
    await message.answer('Да я вижу ты машина!🔥')
    await locationSPORTkeyboard1(message)
    # if message.text == 'Дом🏠':
    #     print('man')
    #     # await manHOMEtrainings(message)
    # elif message.text == 'Тренажерный зал🏋️‍♂️':
    #     print('man')
    #     # await manGYMtrainings(message)

@sportclubBot_dispatcher.message_handler(lambda message: message.text == 'Дом🏠')
async def manHOMEtrainings(message: types.Message):
    await manPartkeyboard(message)

@sportclubBot_dispatcher.message_handler(lambda message: message.text == 'Тренажерный зал🏋️‍♂️')
async def manGYMtrainings(message: types.Message):
    await manPartkeyboard(message)

@sportclubBot_dispatcher.message_handler()
async def checkPartForTraining(message: types.Message):
    if message.text == 'Всё тело🤸🏼‍♂️':
        await bodyMANtraining(message)

async def manPartkeyboard(message: types.Message):
    manPartkeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    body = KeyboardButton('Всё тело🤸🏼‍♂️')
    hands = KeyboardButton('Плечи и руки💪')
    stomach = KeyboardButton('Прессуха🏃‍♂️')
    legs = KeyboardButton('Ноги🦵')
    manPartkeyboard.add(body)
    manPartkeyboard.add(hands, stomach, legs)
    await sportclubBot.send_message(message.chat.id, 'Выбирай что будешь тренировать, машина🥛', reply_markup=manPartkeyboard)

@sportclubBot_dispatcher.message_handler(lambda message: message.text == 'Тренировки для женщин💄')
async def womanTrainings(message: types.Message):
    await message.answer('Ух ты просто соска💋')
    await locationSPORTkeyboard2(message)
    if message.text == 'Дом🏠':
        print('woman')
        # await womanHOMEtrainings(message)
    elif message.text == 'Тренажерный зал🏋️‍♂️':
        print('woman')
        # await womanGYMtrainings(message)

async def womanPartkeyboard(message: types.Message):
    womanPartkeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    body = KeyboardButton('Всё тело🤸‍♀️')
    hands = KeyboardButton('Плечи и руки💪🏼')
    stomach = KeyboardButton('Прессуха🏃‍♀️')
    ass = KeyboardButton('Упругие ягодицы🍑')
    legs = KeyboardButton('Бедра и ноги🦵🏼')
    womanPartkeyboard.add(body)
    womanPartkeyboard.add(hands, stomach, legs)
    womanPartkeyboard.add(ass)
    await sportclubBot.send_message(message.chat.id, 'Выбирай что будешь тренировать, красотка🍆🍑🍆💦🥛CÜM', reply_markup=womanPartkeyboard)

@sportclubBot_dispatcher.message_handler(lambda message: message.text == 'Дом🏡')
async def womanHOMEtrainings(message: types.Message):
    await womanPartkeyboard(message)

@sportclubBot_dispatcher.message_handler(lambda message: message.text == 'Тренажерный зал🏋🏻')
async def womanGYMtrainings(message: types.Message):
    await womanPartkeyboard(message)

async def locationSPORTkeyboard1(message: types.Message):
    locationSPORTkeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    home = KeyboardButton('Дом🏠')
    gym = KeyboardButton('Тренажерный зал🏋️‍♂️')
    locationSPORTkeyboard.add(home)
    locationSPORTkeyboard.add(gym)
    await sportclubBot.send_message(message.chat.id, 'Выбирай место где будешь тренироваться⤵️', reply_markup=locationSPORTkeyboard)

async def locationSPORTkeyboard2(message: types.Message):
    locationSPORTkeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    home = KeyboardButton('Дом🏡')
    gym = KeyboardButton('Тренажерный зал🏋🏻')
    locationSPORTkeyboard.add(home)
    locationSPORTkeyboard.add(gym)
    await sportclubBot.send_message(message.chat.id, 'Выбирай место где будешь тренироваться⤵️', reply_markup=locationSPORTkeyboard)

if __name__ == '__main__':
    executor.start_polling(sportclubBot_dispatcher, skip_updates=True)