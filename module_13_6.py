import os
from aiogram.filters.command import CommandStart
from aiogram import Bot, Dispatcher, types,F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logging
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile
from inlyne import *
import crud_functions

crud_functions.initiate_db()
logging.basicConfig(level=logging.INFO)
api = ""
bot = Bot(token= api)
dp = Dispatcher()



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
        await message.answer('Здравствуйте! Вас приветствует калькулятор подсчета калорий! ',
          reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Рассчитать"),
                    KeyboardButton(text="Купить"),
                    KeyboardButton(text="Регистрация")
                ]
            ],
            resize_keyboard=True,
        ),
    )
@dp.message(F.text == "Рассчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:',
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Рассчитать норму калорий'", callback_data='calories'),
                                     InlineKeyboardButton(text="Формулы расчёта", callback_data='formulas'),
                                 ]
                             ],
                             resize_keyboard=True,
                         ),
                 )

@dp.message(F.text == "Купить")
async def get_buying_list(message: types.Message):
    products = crud_functions.get_all_products()
    for product in products:
        name = product[1]
        description = product[2]
        price = product[3]
        caption = f'Название: {name} | Описание: {description} | Цена: {price}'
        # Добавляем возможность отправить фото, если у продукта есть изображение
        if product_image_exists(product):
            image = FSInputFile(f'files/{name}.png')
            await message.answer_photo(image, caption=caption, show_caption_above_media=True)
        else:
            await message.answer(caption)
    await message.answer('Выберите продукт для покупки:', reply_markup=get_callback_btns(btns={
        'Продукт1': 'product_buying',
        'Продукт2': 'product_buying',
        'Продукт3': 'product_buying',
        'Продукт4': 'product_buying',
    }))
def product_image_exists(product):
    product_image_path = f'files/{product[1]}.png'
    return os.path.exists(product_image_path)

@dp.callback_query(F.data =='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer("Расчет калоррий по формуле Миффлина - Сан Жеора ")
    await call.answer()

@dp.callback_query(F.data =='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message(F.text == 'Регистрация')
async def sing_up(message: types.Message, state: FSMContext):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await state.set_state(RegistrationState.username)

@dp.message(RegistrationState.username)
async def set_username(message: types.Message,  state: FSMContext):

    if crud_functions.is_included(username=message.text):
        await message.answer("Пользователь существует, введите другое имя")
        await state.set_state(RegistrationState.username)
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await state.set_state(RegistrationState.email)

@dp.message(RegistrationState.email)
async def set_email(message: types.Message,  state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await state.set_state(RegistrationState.age)

@dp.message(RegistrationState.age)
async def set_age_2(message: types.Message,  state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    crud_functions.add_user(data['username'], data['email'], int(data['age']))
    await message.answer("Регистрация завершена!")
    await state.finish()


@dp.callback_query(F.data =='calories')
async def set_age(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)
    await call.answer()


@dp.message(UserState.age)
async def set_growth(message: types.Message,  state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост(см):')
    await state.set_state(UserState.growth)

@dp.message(UserState.growth)
async def set_weight(message: types.Message,  state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)

@dp.message(UserState.weight)
async def send_calories(message: types.Message,  state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer('Введите свой пол (м/ж):')
    await state.set_state(UserState.gender)

@dp.message(UserState.gender)
async def set_gender(message: types.Message, state: FSMContext):
    global calories
    await state.update_data(gender=message.text)
    data = await state.get_data()
    age_ = int(data['age'])
    growth_ = int(data['growth'])
    weight_ = int(data['weight'])

    if data["gender"].upper() == 'Ж':
        calories = (weight_ * 10) + (6.25 * growth_) - (5 * age_) - 161

    elif data["gender"].upper() == 'М':
        calories =(weight_*10) + (6.25 * growth_) - (5* age_) + 5

    await message.answer(f"Ваша норма калорий:{calories}")
    await state.finish()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

