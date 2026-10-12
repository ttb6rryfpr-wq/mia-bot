import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

# Токен вашего бота @MIAestetik_Studio_bot
TOKEN = "8842365131:AAF7JSyXwBCz41aS9lNvU3EnYHpwqPRhPSQ"

# Ваш личный ID в Telegram для получения заявок
ADMIN_CHAT_ID = 8447115812

router = Router()

class MiaStates(StatesGroup):
    choosing_category = State()
    choosing_procedure = State()
    waiting_for_clothing_size = State()  # Для Липосоникс
    waiting_for_zone = State()
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_age = State()
    waiting_for_contra = State()
    waiting_for_microcurrents = State()  # Для Индибы
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_messenger = State()

# Главное меню: выбор категории
def get_categories_keyboard():
    buttons = [
        [KeyboardButton(text="🔥 Коррекция тела (Топ-запросы)")],
        [KeyboardButton(text="✨ Уход и омоложение лица")],
        [KeyboardButton(text="🌿 Уход и витамины / NL")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Меню процедур для тела
def get_body_procedures_keyboard():
    buttons = [
        [KeyboardButton(text="🧊 Криолиполиз")],
        [KeyboardButton(text="⚡ Липосоникс / ULFIT")],
        [KeyboardButton(text="🏮 Лазерный липолиз")],
        [KeyboardButton(text="🌊 Кавитация")],
        [KeyboardButton(text="📻 Индиба-массаж (Талия и живот)")],
        [KeyboardButton(text="✨ RF-лифтинг тела (30 мин)")],
        [KeyboardButton(text="◀️ Назад к категориям")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Меню выбора действия для процедуры (Подробнее / Записаться)
def get_procedure_action_keyboard():
    buttons = [
        [KeyboardButton(text="📖 Подробнее о процедуре")],
        [KeyboardButton(text="📝 Записаться / Подобрать параметры")],
        [KeyboardButton(text="◀️ К списку процедур")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Меню подзон для Криолиполиза
def get_cryo_zones_keyboard():
    buttons = [
        [KeyboardButton(text="Руки, бедра, бока (2 манипулы)")],
        [KeyboardButton(text="Живот и бока (4 манипулы)")],
        [KeyboardButton(text="Криолиполиз (6 манипул × 45 мин)")],
        [KeyboardButton(text="◀️ К списку процедур")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Меню подзон для Липосоникс
def get_liposonix_zones_keyboard():
    buttons = [
        [KeyboardButton(text="Липосоникс — Живот")],
        [KeyboardButton(text="Липосоникс — Бока")],
        [KeyboardButton(text="Липосоникс — Бёдра")],
        [KeyboardButton(text="Липосоникс — Ягодицы")],
        [KeyboardButton(text="Комплекс / Локальные отложения (Индивидуально)")],
        [KeyboardButton(text="◀️ К списку процедур")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Меню подзон для Кавитации
def get_cavitation_keyboard():
    buttons = [
        [KeyboardButton(text="Кавитация 30 минут")],
        [KeyboardButton(text="Кавитация 60 минут (несколько зон)")],
        [KeyboardButton(text="◀️ К списку процедур")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Меню для лица (с разделами и заглушками)
def get_face_procedures_keyboard():
    buttons = [
        [KeyboardButton(text="🌟 INDIBA RF (Лицо)")],
        [KeyboardButton(text="🧪 Пилинги и уход")],
        [KeyboardButton(text="◀️ Назад к категориям")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# --- КАТЕГОРИИ NL И УХОДА (Инлайн-клавиатуры) ---
def get_nl_categories_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✨ Коллаген", callback_data="nl_collagen")],
            [InlineKeyboardButton(text="🧬 Антиэйдж (Молодость)", callback_data="nl_antiage")],
            [InlineKeyboardButton(text="🔥 Похудение и DrainEffect", callback_data="nl_slim")],
            [InlineKeyboardButton(text="🧴 Красота и уход", callback_data="nl_beauty")],
            [InlineKeyboardButton(text="📦 Прочее (Животные, Дети)", callback_data="nl_other")],
            [InlineKeyboardButton(text="💎 Стать покупателем (Регистрация)", url="https://nlstar.com/ref/QTjP5R/")]
        ]
    )
    return keyboard

def get_beauty_subcategories_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌸 Уход за лицом", url="https://ng.nlstar.com/ru/api/referrals/ref/Z4VfCv/")],
            [InlineKeyboardButton(text="🌿 Уход за телом", url="https://ng.nlstar.com/ru/api/referrals/ref/VeHQpy/")],
            [InlineKeyboardButton(text="👔 Мужская косметика", url="https://ng.nlstar.com/ru/api/referrals/ref/CMEcFs/")],
            [InlineKeyboardButton(text="🦷 Уход за полостью рта", url="https://ng.nlstar.com/ru/api/referrals/ref/XkH1T3/")],
            [InlineKeyboardButton(text="🔙 Назад к каталогу NL", callback_data="back_to_nl")]
        ]
    )
    return keyboard

def get_other_subcategories_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🐾 Для животных", callback_data="nl_pets")],
            [InlineKeyboardButton(text="🧸 Для детей", callback_data="nl_kids")],
            [InlineKeyboardButton(text="🔙 Назад к каталогу NL", callback_data="back_to_nl")]
        ]
    )
    return keyboard

def get_pets_subcategories_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💊 Витамины для животных", url="https://ng.nlstar.com/ru/api/referrals/ref/W4EEUd/")],
            [InlineKeyboardButton(text="🧴 Косметика для животных", url="https://ng.nlstar.com/ru/api/referrals/ref/yT4zdU/")],
            [InlineKeyboardButton(text="🔙 Назад в «Прочее»", callback_data="nl_other")]
        ]
    )
    return keyboard

def get_kids_subcategories_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💊 Детские БАД", url="https://ng.nlstar.com/ru/api/referrals/ref/RQAZJL/")],
            [InlineKeyboardButton(text="🧴 Детская косметика", url="https://ng.nlstar.com/ru/api/referrals/ref/a5p5SL/")],
            [InlineKeyboardButton(text="🔙 Назад в «Прочее»", callback_data="nl_other")]
        ]
    )
    return keyboard


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Здравствуйте! Я — Мия, виртуальный помощник студии эстетики и аппаратной косметологии Анны (м. Тульская).\n"
        "Я помогу вам подобрать процедуру для преображения или выбрать качественный уход и витамины изнутри.\n\n"
        "Выберите нужное направление:",
        reply_markup=get_categories_keyboard(),
    )
    await state.set_state(MiaStates.choosing_category)

@router.message(MiaStates.choosing_category, F.text == "🔥 Коррекция тела (Топ-запросы)")
async def category_body(message: Message, state: FSMContext):
    await message.answer("Выберите процедуру по телу:", reply_markup=get_body_procedures_keyboard())
    await state.set_state(MiaStates.choosing_procedure)

@router.message(MiaStates.choosing_category, F.text == "✨ Уход и омоложение лица")
async def category_face(message: Message, state: FSMContext):
    await message.answer("Выберите направление по лицу:", reply_markup=get_face_procedures_keyboard())
    await state.set_state(MiaStates.choosing_procedure)

@router.message(MiaStates.choosing_category, F.text == "🌿 Уход и витамины / NL")
async def category_nl(message: Message, state: FSMContext):
    await message.answer(
        "🌿 **Забота о красоте и здоровье изнутри**\n\n"
        "Я сотрудничаю с NL International и рекомендую продукцию, которая идеально дополняет и усиливает результаты аппаратных процедур.\n\n"
        "Выберите интересующий вас раздел:",
        reply_markup=get_nl_categories_keyboard(),
        parse_mode="Markdown"
    )

# --- ОБРАБОТЧИКИ ИНЛАЙН-КНОПОК NL ---
@router.callback_query(F.data == "nl_collagen")
async def cb_collagen(callback: Message):
    text = (
        "✨ **Коллаген для упругости кожи и суставов**\n"
        "Идеально поддерживает каркас кожи после процедур Липосоникс и Indiba.\n\n"
        "• **Collagentrinity (Вишня):** 3 вида коллагена (говяжий, морской, куриный) с пептидами (9 140 мг пептидов, эластин, гиалуроновая кислота в порции).\n"
        "• **Collagen Peptides (Тропик):** 10 000 мг пептидов коллагена + витамин С, глицин, пролин."
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Каталог направления Коллаген", url="https://ng.nlstar.com/ru/api/referrals/ref/xn79LR/")],
            [InlineKeyboardButton(text="🍒 Купить Collagentrinity (1)", url="https://ng.nlstar.com/ru/api/referrals/ref/hTFR5E/")],
            [InlineKeyboardButton(text="🍒 Купить Collagentrinity (2)", url="https://ng.nlstar.com/ru/api/referrals/ref/LRiM39/")],
            [InlineKeyboardButton(text="🍍 Купить Collagen Peptides", url="https://ng.nlstar.com/ru/api/referrals/ref/JgHoG2/")],
            [InlineKeyboardButton(text="🔙 Назад к категориям NL", callback_data="back_to_nl")]
        ]
    )
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data == "nl_antiage")
async def cb_antiage(callback: Message):
    text = (
        "🧬 **Антиэйдж (Программы молодости и антиоксиданты)**\n\n"
        "• **«Анти-эйдж Молекула» (Anti-age Molecule):** Активация выработки NAD+ для клеточной энергии, низкомолекулярная гиалуроновая кислота для упругости кожи.\n"
        "• **Пептидный напиток Cellcode®:** 7 пептидных компонентов и растительных экстрактов для запуска клеточного обновления и защиты суставов, сердца и тонуса."
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Каталог направления Anti-Age", url="https://ng.nlstar.com/ru/api/referrals/ref/LJ37dE/")],
            [InlineKeyboardButton(text="🔙 Назад к категориям NL", callback_data="back_to_nl")]
        ]
    )
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data == "nl_slim")
async def cb_slim(callback: Message):
    text = (
        "🔥 **Похудение и поддержка после процедур**\n"
        "Отличная поддержка результатов криолиполиза и кавитации:\n\n"
        "• **DrainEffect (Мята / Гранат):** Устранение отеков, запуск похудения, выведение токсинов.\n"
        "• **Metaboost®:** Жиросжигатель с L-карнитином, хромом и инулином.\n"
        "• **ED Smart (Супы и коктейли):** Сбалансированное питание и умная замена приема пищи (Фисташковое мороженое, Кофе, Ванильный пломбир, Сырный/Куриный суп и др.)."
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Общий каталог похудения", url="https://ng.nlstar.com/ru/api/referrals/ref/vUkRdD/")],
            [InlineKeyboardButton(text="🧴 Косметика для похудения", url="https://ng.nlstar.com/ru/api/referrals/ref/bnY282/")],
            [InlineKeyboardButton(text="🥗 Функциональное питание ED Smart", url="https://ng.nlstar.com/ru/api/referrals/ref/SrFCko/")],
            [InlineKeyboardButton(text="🔙 Назад к категориям NL", callback_data="back_to_nl")]
        ]
    )
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data == "nl_beauty")
async def cb_beauty(callback: Message):
    text = "🧴 **Красота и уход**\nВыберите интересующий вас подраздел ухода:"
    await callback.message.edit_text(text, reply_markup=get_beauty_subcategories_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "nl_other")
async def cb_other(callback: Message):
    text = "📦 **Прочее**\nВыберите нужную категорию:"
    await callback.message.edit_text(text, reply_markup=get_other_subcategories_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "nl_pets")
async def cb_pets(callback: Message):
    text = "🐾 **Забота о домашних животных**\nВыберите категорию:"
    await callback.message.edit_text(text, reply_markup=get_pets_subcategories_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "nl_kids")
async def cb_kids(callback: Message):
    text = "🧸 **Продукция для детей**\nВыберите категорию:"
    await callback.message.edit_text(text, reply_markup=get_kids_subcategories_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "back_to_nl")
async def cb_back_nl(callback: Message):
    text = (
        "🌿 **Забота о красоте и здоровье изнутри**\n\n"
        "Выберите интересующий вас раздел:"
    )
    await callback.message.edit_text(text, reply_markup=get_nl_categories_keyboard(), parse_mode="Markdown")


@router.message(MiaStates.choosing_procedure, F.text == "◀️ Назад к категориям")
async def back_to_categories(message: Message, state: FSMContext):
    await message.answer("Выберите направление:", reply_markup=get_categories_keyboard())
    await state.set_state(MiaStates.choosing_category)

@router.message(MiaStates.choosing_procedure, F.text == "◀️ К списку процедур")
async def back_to_body_list(message: Message, state: FSMContext):
    await message.answer("Выберите процедуру по телу:", reply_markup=get_body_procedures_keyboard())
    await state.set_state(MiaStates.choosing_procedure)

# --- 1. КРИОЛИПОЛИЗ ---
@router.message(MiaStates.choosing_procedure, F.text == "🧊 Криолиполиз")
async def choose_cryo(message: Message, state: FSMContext):
    await state.update_data(current_procedure="Криолиполиз")
    await message.answer(
        "🧊 **Криолиполиз** — метод удаления локальных жировых отложений холодом без операций.\n"
        "Что вы хотите сделать?",
        reply_markup=get_procedure_action_keyboard(),
        parse_mode="Markdown"
    )

@router.message(MiaStates.choosing_procedure, F.text == "📖 Подробнее о процедуре")
async def cryo_details(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("current_procedure") == "Криолиполиз":
        text = (
            "🧊 **Всё о процедуре: Криолиполиз**\n\n"
            "✨ **Как проходит сеанс:**\n"
            "1. На кожу накладывается специальная защитная салфетка и слой пленки.\n"
            "2. Мастер прикладывает насадку: она втягивает складку вакуумом и бережно охлаждает её.\n"
            "3. Сеанс длится 45–60 минут, после чего мастер делает легкий массаж зоны.\n\n"
            "📋 **Рекомендации ДО и ПОСЛЕ:**\n"
            "• Пейте больше чистой воды (~30 мл на 1 кг веса).\n"
            "• Избегайте бань, саун и тяжелых тренировок в день процедуры.\n"
            "• Эффект нарастает 3–8 недель. Повтор через 3–5 недель."
        )
        await message.answer(text, parse_mode="Markdown", reply_markup=get_procedure_action_keyboard())

@router.message(MiaStates.choosing_procedure, F.text == "📝 Записаться / Подобрать параметры")
async def cryo_start_form(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Криолиполиз":
        await message.answer(
            "🧊 Давайте проверим, подходит ли вам криолиполиз.\n"
            "Выберите зону / количество манипул:",
            reply_markup=get_cryo_zones_keyboard()
        )

@router.message(F.text.in_({
    "Руки, бедра, бока (2 манипулы)", 
    "Живот и бока (4 манипулы)", 
    "Криолиполиз (6 манипул × 45 мин)"
}))
async def cryo_zone_selected(message: Message, state: FSMContext):
    await state.update_data(procedure=f"Криолиполиз: {message.text}")
    await ask_height_weight_flow(message, state)


# --- 2. ЛИПОСОНИКС ---
@router.message(MiaStates.choosing_procedure, F.text == "⚡ Липосоникс / ULFIT")
async def choose_liposonix(message: Message, state: FSMContext):
    await state.update_data(current_procedure="Липосоникс")
    await message.answer(
        "⚡ **Липосоникс / ULFIT** — мощный ультразвуковой лифтинг жировых ловушек.\n"
        "Что вы хотите сделать?",
        reply_markup=get_procedure_action_keyboard(),
        parse_mode="Markdown"
    )

@router.message(MiaStates.choosing_procedure, F.text == "📖 Подробнее о процедуре")
async def liposonix_details(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Липосоникс":
        text = (
            "⚡ **Всё о процедуре: Липосоникс / ULFIT**\n\n"
            "💡 **Стоимость и расчет:**\n"
            "• Зона 5×5 см — 1 200 ₽ (3 прохода).\n"
            "⚠️ *Процедура проводится при размере одежды от 44-го.*\n\n"
            "✨ **Как проходит сеанс:** Ультразвук точечно работает с глубоким жиром (45–60 минут)."
        )
        await message.answer(text, parse_mode="Markdown", reply_markup=get_procedure_action_keyboard())

@router.message(MiaStates.choosing_procedure, F.text == "📝 Записаться / Подобрать параметры")
async def liposonix_start_form(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Липосоникс":
        await message.answer(
            "⚡ Выберите зону Липосоникс:",
            reply_markup=get_liposonix_zones_keyboard()
        )

@router.message(F.text.in_({
    "Липосоникс — Живот", "Липосоникс — Бока", "Липосоникс — Бёдра", 
    "Липосоникс — Ягодицы", "Комплекс / Локальные отложения (Индивидуально)"
}))
async def liposonix_zone_selected(message: Message, state: FSMContext):
    await state.update_data(procedure=f"Липосоникс: {message.text}")
    await message.answer(
        "Укажите ваш **размер одежды** (процедура проводится строго при размере от 44-го):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MiaStates.waiting_for_clothing_size)

@router.message(MiaStates.waiting_for_clothing_size)
async def clothing_size_received(message: Message, state: FSMContext):
    await state.update_data(clothing_size=message.text)
    await ask_height_weight_flow(message, state)


# --- 3. ЛАЗЕРНЫЙ ЛИПОЛИЗ ---
@router.message(MiaStates.choosing_procedure, F.text == "🏮 Лазерный липолиз")
async def choose_laser(message: Message, state: FSMContext):
    await state.update_data(current_procedure="Лазерный липолиз")
    await message.answer(
        "🏮 **Лазерный липолиз** — холодный лазер 650 нм для безопасного расщепления жира и подтяжки кожи.\n"
        "Что вы хотите сделать?",
        reply_markup=get_procedure_action_keyboard(),
        parse_mode="Markdown"
    )

@router.message(MiaStates.choosing_procedure, F.text == "📖 Подробнее о процедуре")
async def laser_details(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Лазерный липолиз":
        text = "🏮 **Лазерный липолиз** (40 минут). Эффективно сочетается с лимфодренажем и RF-лифтингом."
        await message.answer(text, parse_mode="Markdown", reply_markup=get_procedure_action_keyboard())

@router.message(MiaStates.choosing_procedure, F.text == "📝 Записаться / Подобрать параметры")
async def laser_start_form(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Лазерный липолиз":
        await state.update_data(procedure="🏮 Лазерный липолиз")
        await ask_height_weight_flow(message, state)


# --- 4. КАВИТАЦИЯ ---
@router.message(MiaStates.choosing_procedure, F.text == "🌊 Кавитация")
async def choose_cavitation(message: Message, state: FSMContext):
    await state.update_data(current_procedure="Кавитация")
    await message.answer(
        "🌊 **Кавитация** — эффективное разрушение жировых клеток ультразвуком.\n"
        "Выберите формат:",
        reply_markup=get_cavitation_keyboard(),
        parse_mode="Markdown"
    )

@router.message(F.text.in_({"Кавитация 30 минут", "Кавитация 60 минут (несколько зон)"}))
async def cavitation_selected(message: Message, state: FSMContext):
    await state.update_data(procedure=f"Кавитация: {message.text}")
    await ask_height_weight_flow(message, state)


# --- 5. ИНДИБА-МАССАЖ ---
@router.message(MiaStates.choosing_procedure, F.text == "📻 Индиба-массаж (Талия и живот)")
async def choose_indiba(message: Message, state: FSMContext):
    await state.update_data(current_procedure="Индиба")
    await message.answer(
        "📻 **INDIBA RF по телу** — передовая технология для подтяжки кожи и объемов.\n"
        "Что вы хотите сделать?",
        reply_markup=get_procedure_action_keyboard(),
        parse_mode="Markdown"
    )

@router.message(MiaStates.choosing_procedure, F.text == "📖 Подробнее о процедуре")
async def indiba_details(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Индиба":
        text = "📻 Комфортная процедура с эффектом глубокого прогрева тканей (45 минут)."
        await message.answer(text, parse_mode="Markdown", reply_markup=get_procedure_action_keyboard())

@router.message(MiaStates.choosing_procedure, F.text == "📝 Записаться / Подобрать параметры")
async def indiba_start_form(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Индиба":
        await state.update_data(procedure="📻 Индиба-массаж (Талия и живот)")
        await ask_height_weight_flow(message, state)


# --- 6. РФ-ЛИФТИНГ ТЕЛА ---
@router.message(MiaStates.choosing_procedure, F.text == "✨ RF-лифтинг тела (30 мин)")
async def choose_rf_body(message: Message, state: FSMContext):
    await state.update_data(procedure="✨ RF-лифтинг тела (30 мин)")
    await ask_height_weight_flow(message, state)


# --- АНКЕТА И СБОР ДАННЫХ ---
async def ask_height_weight_flow(message: Message, state: FSMContext):
    await message.answer(
        "Укажите вашу **желаемую зону коррекции** своими словами:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MiaStates.waiting_for_zone)

@router.message(MiaStates.waiting_for_zone)
async def zone_received(message: Message, state: FSMContext):
    await state.update_data(zone=message.text)
    await message.answer("Укажите ваш **рост** (в сантиметрах, например: 168):")
    await state.set_state(MiaStates.waiting_for_height)

@router.message(MiaStates.waiting_for_height)
async def height_received(message: Message, state: FSMContext):
    try:
        height = float(message.text.replace(",", "."))
        if height < 50 or height > 250:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите корректный рост цифрами (например, 168):")
        return

    await state.update_data(height=height)
    await message.answer("Укажите ваш **вес** (в килограммах, например: 65):")
    await state.set_state(MiaStates.waiting_for_weight)

@router.message(MiaStates.waiting_for_weight)
async def weight_received(message: Message, state: FSMContext):
    try:
        weight = float(message.text.replace(",", "."))
        if weight < 30 or weight > 300:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите корректный вес цифрами (например, 65):")
        return

    data = await state.get_data()
    height_m = data["height"] / 100.0
    bmi = round(weight / (height_m**2), 1)

    await state.update_data(weight=weight, bmi=bmi)
    await message.answer(f"Спасибо! Ваш ИМТ: {bmi}.\nСколько вам полных лет?")
    await state.set_state(MiaStates.waiting_for_age)

@router.message(MiaStates.waiting_for_age)
async def age_received(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(
        "Есть ли у вас основные противопоказания?\n"
        "(беременность/ГВ, онкология, кардиостимулятор, импланты, грыжи, эпилепсия)\n\n"
        "Напишите коротко: **нет** или укажите, если что-то имеется."
    )
    await state.set_state(MiaStates.waiting_for_contra)

@router.message(MiaStates.waiting_for_contra)
async def contra_received(message: Message, state: FSMContext):
    contra_text = message.text.lower()
    has_contra = any(word in contra_text for word in ["да", "беремен", "онко", "кардио", "имплант", "грыж", "эпилепси"])
    
    status = "Не обнаружены" if not has_contra else f"Есть нюанс: {message.text}"
    await state.update_data(contra=status, has_contra=has_contra)

    data = await state.get_data()
    proc = data.get("procedure", "")

    if "Индиба" in proc:
        await message.answer("⚠️ Используете ли вы параллельно микротоковую терапию?")
        await state.set_state(MiaStates.waiting_for_microcurrents)
    else:
        await state.update_data(microcurrents="Не применимо")
        await request_contact_step(message, state)

@router.message(MiaStates.waiting_for_microcurrents)
async def microcurrents_received(message: Message, state: FSMContext):
    await state.update_data(microcurrents=message.text)
    await request_contact_step(message, state)

async def request_contact_step(message: Message, state: FSMContext):
    await message.answer(
        "Чтобы забронировать время, представьтесь, пожалуйста. **Как вас зовут?**",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MiaStates.waiting_for_name)

@router.message(MiaStates.waiting_for_name)
async def name_received(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    
    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Поделиться контактом", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer("Поделитесь вашим **номером телефона**:", reply_markup=phone_keyboard)
    await state.set_state(MiaStates.waiting_for_phone)

@router.message(MiaStates.waiting_for_phone, F.contact | F.text)
async def phone_received(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)

    await message.answer(
        "В каком мессенджере вам удобнее продолжить общение? (Telegram, WhatsApp)",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MiaStates.waiting_for_messenger)

@router.message(MiaStates.waiting_for_messenger)
async def messenger_received(message: Message, state: FSMContext):
    messenger = message.text
    data = await state.get_data()
    proc = data.get("procedure", "")

    lead_card = (
        "🔔 **НОВЫЙ ЗАПРОС ИЗ БОТА (@MIAestetik_Studio_bot)**\n\n"
        f"👤 **Имя:** {data.get('name')}\n"
        f"📞 **Телефон:** {data.get('phone')}\n"
        f"💬 **Мессенджер:** {messenger}\n\n"
        f"⚙️ **Процедура:** {proc}\n"
        f"📍 **Зона:** {data.get('zone')}\n"
        f"📊 **Рост/Вес/Возраст:** {data.get('height')} см / {data.get('weight')} кг / {data.get('age')} лет\n"
        f"📐 **ИМТ:** {data.get('bmi')}\n"
        f"🛡 **Противопоказания:** {data.get('contra')}\n"
        f"⚡ **Доп.:** Размер: {data.get('clothing_size', 'н/д')} | Микротоки: {data.get('microcurrents')}"
    )

    try:
        await message.bot.send_message(ADMIN_CHAT_ID, lead_card, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Не удалось отправить лид администратору: {e}")

    has_contra = data.get("has_contra")
    dikidi_url = None

    if "Криолиполиз: Руки, бедра, бока (2 манипулы)" in proc:
        dikidi_url = "https://dkd.su/1932426/s/20721450"
    elif "Криолиполиз: Живот и бока (4 манипулы)" in proc:
        dikidi_url = "https://dkd.su/1932426/s/22340581"
    elif "Кавитация 30 минут" in proc:
        dikidi_url = "https://dkd.su/1932426/s/20726376"
    elif "Кавитация 60 минут (несколько зон)" in proc:
        dikidi_url = "https://dkd.su/1932426/s/23100581"
    elif "Лазерный липолиз" in proc:
        dikidi_url = "https://dkd.su/1932426/s/20765174"
    elif "Индиба-массаж (Талия и живот)" in proc:
        dikidi_url = "https://dkd.su/1932426/s/23088858"
    elif "RF-лифтинг тела (30 мин)" in proc:
        dikidi_url = "https://dkd.su/1932426/s/20989146"
    elif "Липосоникс — Живот" in proc:
        dikidi_url = "https://dkd.su/1932426/s/23483825"
    elif "Липосоникс — Бока" in proc:
        dikidi_url = "https://dkd.su/1932426/s/23483838"
    elif "Липосоникс — Бёдра" in proc:
        dikidi_url = "https://dkd.su/1932426/s/23483859"
    elif "Липосоникс — Ягодицы" in proc:
        dikidi_url = "https://dkd.su/1932426/s/23483877"

    if not has_contra and dikidi_url:
        dikidi_kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="📅 Записаться онлайн в DIKIDI", url=dikidi_url)]]
        )
        await message.answer(
            "Готово! Я передала всю информацию Анне. Противопоказаний по анкете не обнаружено, "
            "вы можете сразу выбрать удобное время визита по прямой ссылке:",
            reply_markup=dikidi_kb
        )
    else:
        await message.answer(
            "Готово! Я передала всю информацию Анне. Анна свяжется с вами лично в ближайшее время."
        )

    await state.clear()


# --- ЗАГЛУШКИ ДЛЯ ЛИЦА ---
@router.message(MiaStates.choosing_procedure, F.text.in_({
    "🌟 INDIBA RF (Лицо)", "🧪 Пилинги и уход"
}))
async def empty_face_procedures(message: Message, state: FSMContext):
    dikidi_profile_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="👉 Посмотреть все услуги в DIKIDI", url="https://dikidi.net/apparatestetik")]]
    )
    await message.answer(
        "Извините, этот раздел услуг сейчас находится в разработке и наполняется 🌸\n\n"
        "Вы всегда можете ознакомиться со всеми актуальными услугами и записаться в нашем профиле DIKIDI:",
        reply_markup=dikidi_profile_kb
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    print("Бот @MIAestetik_Studio_bot обновлен и запущен со всеми разделами NL и витаминов!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
