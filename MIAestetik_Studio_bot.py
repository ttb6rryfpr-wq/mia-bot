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
        [KeyboardButton(text="🎯 С чего начать (Старт коррекции)")],
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

# Меню «С чего начать»
def get_start_programs_keyboard():
    buttons = [
        [KeyboardButton(text="📋 Консультация + подбор программы")],
        [KeyboardButton(text="✨ Комплекс «Старт коррекции»")],
        [KeyboardButton(text="◀️ Назад к категориям")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Меню процедур для лица
def get_face_procedures_keyboard():
    buttons = [
        [KeyboardButton(text="🧪 Карбокситерапия CO2")],
        [KeyboardButton(text="💎 V-LIFT с PDRN и пептидами")],
        [KeyboardButton(text="✨ Ультразвуковая чистка лица")],
        [KeyboardButton(text="📻 Аппаратный уход RF (Лицо)")],
        [KeyboardButton(text="💧 «Фарфоровая куколка» (Фонофорез)")],
        [KeyboardButton(text="☕ Кофейный антивозрастной пилинг")],
        [KeyboardButton(text="🌿 Tiffany / Бирюзовый PDRN-пилинг")],
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

@router.message(MiaStates.choosing_category, F.text == "🎯 С чего начать (Старт коррекции)")
async def category_start(message: Message, state: FSMContext):
    await message.answer("Выберите стартовую программу:", reply_markup=get_start_programs_keyboard())
    await state.set_state(MiaStates.choosing_procedure)

@router.message(MiaStates.choosing_category, F.text == "✨ Уход и омоложение лица")
async def category_face(message: Message, state: FSMContext):
    await message.answer("Выберите процедуру по уходу за лицом:", reply_markup=get_face_procedures_keyboard())
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
        "• **Collagentrinity (Вишня):** 3 вида коллагена с пептидами (9 140 мг пептидов, эластин, гиалуроновая кислота).\n"
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
        "• **«Анти-эйдж Молекула» (Anti-age Molecule):** Активация выработки NAD+ для клеточной энергии, гиалуроновая кислота.\n"
        "• **Пептидный напиток Cellcode®:** 7 пептидных компонентов для клеточного обновления и защиты."
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
        "Поддержка результатов криолиполиза и кавитации:\n\n"
        "• **DrainEffect (Мята / Гранат):** Устранение отеков, запуск похудения.\n"
        "• **Metaboost®:** Жиросжигатель с L-карнитином, хромом и инулином.\n"
        "• **ED Smart (Супы и коктейли):** Умная замена приема пищи."
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
    text = "🌿 **Забота о красоте и здоровье изнутри**\n\nВыберите интересующий вас раздел:"
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
            "✨ **Как проходит сеанс:** 45–60 минут бережного охлаждения жировой складки под защитной салфеткой.\n\n"
            "📋 **Рекомендации:** Пейте больше чистой воды (~30 мл/кг), избегайте бань и саун в день процедуры."
        )
        await message.answer(text, parse_mode="Markdown", reply_markup=get_procedure_action_keyboard())

@router.message(MiaStates.choosing_procedure, F.text == "📝 Записаться / Подобрать параметры")
async def cryo_start_form(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Криолиполиз":
        await message.answer("🧊 Выберите зону / количество манипул:", reply_markup=get_cryo_zones_keyboard())

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
        text = "⚡ Зона 5×5 см — 1 200 ₽. Процедура проводится строго при размере одежды от 44-го."
        await message.answer(text, parse_mode="Markdown", reply_markup=get_procedure_action_keyboard())

@router.message(MiaStates.choosing_procedure, F.text == "📝 Записаться / Подобрать параметры")
async def liposonix_start_form(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Липосоникс":
        await message.answer("⚡ Выберите зону Липосоникс:", reply_markup=get_liposonix_zones_keyboard())

@router.message(F.text.in_({
    "Липосоникс — Живот", "Липосоникс — Бока", "Липосоникс — Бёдра", 
    "Липосоникс — Ягодицы", "Комплекс / Локальные отложения (Индивидуально)"
}))
async def liposonix_zone_selected(message: Message, state: FSMContext):
    await state.update_data(procedure=f"Липосоникс: {message.text}")
    await message.answer("Укажите ваш **размер одежды** (от 44-го):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(MiaStates.waiting_for_clothing_size)

@router.message(MiaStates.waiting_for_clothing_size)
async def clothing_size_received(message: Message, state: FSMContext):
    await state.update_data(clothing_size=message.text)
    await ask_height_weight_flow(message, state)


# --- 3. ЛАЗЕРНЫЙ ЛИПОЛИЗ ---
@router.message(MiaStates.choosing_procedure, F.text == "🏮 Лазерный липолиз")
async def choose_laser(message: Message, state: FSMContext):
    await state.update_data(current_procedure="Лазерный липолиз")
    await message.answer("🏮 **Лазерный липолиз** 650 нм. Что вы хотите сделать?", reply_markup=get_procedure_action_keyboard())

@router.message(MiaStates.choosing_procedure, F.text == "📖 Подробнее о процедуре")
async def laser_details(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Лазерный липолиз":
        await message.answer("🏮 Сеанс 40 минут. Идеален в комплексе с лимфодренажем и RF.", parse_mode="Markdown", reply_markup=get_procedure_action_keyboard())

@router.message(MiaStates.choosing_procedure, F.text == "📝 Записаться / Подобрать параметры")
async def laser_start_form(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Лазерный липолиз":
        await state.update_data(procedure="🏮 Лазерный липолиз")
        await ask_height_weight_flow(message, state)


# --- 4. КАВИТАЦИЯ ---
@router.message(MiaStates.choosing_procedure, F.text == "🌊 Кавитация")
async def choose_cavitation(message: Message, state: FSMContext):
    await state.update_data(current_procedure="Кавитация")
    await message.answer("🌊 Выберите формат кавитации:", reply_markup=get_cavitation_keyboard())

@router.message(F.text.in_({"Кавитация 30 минут", "Кавитация 60 минут (несколько зон)"}))
async def cavitation_selected(message: Message, state: FSMContext):
    await state.update_data(procedure=f"Кавитация: {message.text}")
    await ask_height_weight_flow(message, state)


# --- 5. ИНДИБА-МАССАЖ ---
@router.message(MiaStates.choosing_procedure, F.text == "📻 Индиба-массаж (Талия и живот)")
async def choose_indiba(message: Message, state: FSMContext):
    await state.update_data(current_procedure="Индиба")
    await message.answer("📻 **INDIBA RF** (448 кГц). Что вы хотите сделать?", reply_markup=get_procedure_action_keyboard())

@router.message(MiaStates.choosing_procedure, F.text == "📖 Подробнее о процедуре")
async def indiba_details(message: Message, state: FSMContext):
    if (await state.get_data()).get("current_procedure") == "Индиба":
        await message.answer("📻 Глубокий комфортный прогрев тканей, подтяжка и моделирование (45 мин).", parse_mode="Markdown", reply_markup=get_procedure_action_keyboard())

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


# --- СТАРТОВЫЕ ПРОГРАММЫ И ЛИЦО (Прямые ссылки на DIKIDI) ---
@router.message(MiaStates.choosing_procedure, F.text.in_({
    "📋 Консультация + подбор программы", "✨ Комплекс «Старт коррекции»",
    "🧪 Карбокситерапия CO2", "💎 V-LIFT с PDRN и пептидами",
    "✨ Ультразвуковая чистка лица", "📻 Аппаратный уход RF (Лицо)",
    "💧 «Фарфоровая куколка» (Фонофорез)", "☕ Кофейный антивозрастной пилинг",
    "🌿 Tiffany / Бирюзовый PDRN-пилинг"
}))
async def direct_dikidi_procedure(message: Message, state: FSMContext):
    proc = message.text
    dikidi_url = None

    if "Консультация + подбор программы" in proc:
        dikidi_url = "https://dkd.su/1932426/s/21753983"
    elif "Комплекс «Старт коррекции»" in proc:
        dikidi_url = "https://dkd.su/1932426/s/22125430"
    elif "Карбокситерапия CO2" in proc:
        dikidi_url = "https://dkd.su/1932426/s/21225840"
    elif "V-LIFT с PDRN" in proc:
        dikidi_url = "https://dkd.su/1932426/s/22555535"
    elif "Ультразвуковая чистка лица" in proc:
        dikidi_url = "https://dkd.su/1932426/s/21335030"
    elif "Аппаратный уход RF (Лицо)" in proc:
        dikidi_url = "https://dkd.su/1932426/s/23432381"
    elif "Фарфоровая куколка" in proc:
        dikidi_url = "https://dkd.su/1932426/s/22555865"
    elif "Кофейный антивозрастной пилинг" in proc:
        dikidi_url = "https://dkd.su/1932426/s/22538168"
    elif "Tiffany / Бирюзовый PDRN-пилинг" in proc:
        dikidi_url = "https://dkd.su/1932426/s/22538181"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="📅 Записаться онлайн в DIKIDI", url=dikidi_url)]]
    )
    await message.answer(
        f"🌸 Вы выбрали: **{proc}**\n\n"
        "Вы можете сразу забронировать удобное время визита в нашей студии на м. Тульская по ссылке:",
        reply_markup=kb,
        parse_mode="Markdown"
    )
    await state.clear()


# --- АНКЕТА И СБОР ДАННЫХ ДЛЯ ТЕЛА ---
async def ask_height_weight_flow(message: Message, state: FSMContext):
    await message.answer("Укажите вашу **желаемую зону коррекции** своими словами:", reply_markup=ReplyKeyboardRemove())
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
        await message.answer("Введите корректный рост цифрами (например, 168):")
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
        await message.answer("Введите корректный вес цифрами (например, 65):")
        return
    data = await state.get_data()
    bmi = round(weight / ((data["height"] / 100.0) ** 2), 1)
    await state.update_data(weight=weight, bmi=bmi)
    await message.answer(f"Спасибо! Ваш ИМТ: {bmi}.\nСколько вам полных лет?")
    await state.set_state(MiaStates.waiting_for_age)

@router.message(MiaStates.waiting_for_age)
async def age_received(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Есть ли противопоказания? (беременность/ГВ, онкология, кардиостимулятор, импланты, грыжи, эпилепсия)\n\nНапишите: **нет** или укажите нюансы.")
    await state.set_state(MiaStates.waiting_for_contra)

@router.message(MiaStates.waiting_for_contra)
async def contra_received(message: Message, state: FSMContext):
    contra_text = message.text.lower()
    has_contra = any(w in contra_text for w in ["да", "беремен", "онко", "кардио", "имплант", "грыж", "эпилепси"])
    status = "Не обнаружены" if not has_contra else f"Есть нюанс: {message.text}"
    await state.update_data(contra=status, has_contra=has_contra)

    if "Индиба" in (await state.get_data()).get("procedure", ""):
        await message.answer("⚠️ Используете ли параллельно микротоковую терапию?")
        await state.set_state(MiaStates.waiting_for_microcurrents)
    else:
        await state.update_data(microcurrents="Не применимо")
        await request_contact_step(message, state)

@router.message(MiaStates.waiting_for_microcurrents)
async def microcurrents_received(message: Message, state: FSMContext):
    await state.update_data(microcurrents=message.text)
    await request_contact_step(message, state)

async def request_contact_step(message: Message, state: FSMContext):
    await message.answer("Как вас зовут?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(MiaStates.waiting_for_name)

@router.message(MiaStates.waiting_for_name)
async def name_received(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    phone_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📱 Поделиться контактом", request_contact=True)]], resize_keyboard=True)
    await message.answer("Поделитесь номером телефона:", reply_markup=phone_kb)
    await state.set_state(MiaStates.waiting_for_phone)

@router.message(MiaStates.waiting_for_phone, F.contact | F.text)
async def phone_received(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)
    await message.answer("В каком мессенджере удобнее продолжить общение? (Telegram, WhatsApp)", reply_markup=ReplyKeyboardRemove())
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
        f"📊 **Параметры:** {data.get('height')} см / {data.get('weight')} кг / {data.get('age')} лет (ИМТ: {data.get('bmi')})\n"
        f"🛡 **Противопоказания:** {data.get('contra')}"
    )

    try:
        await message.bot.send_message(ADMIN_CHAT_ID, lead_card, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Не удалось отправить лид: {e}")

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
        dikidi_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📅 Записаться онлайн в DIKIDI", url=dikidi_url)]])
        await message.answer("Готово! Я передала информацию Анне. Противопоказаний не обнаружено, вы можете записаться онлайн:", reply_markup=dikidi_kb)
    else:
        await message.answer("Готово! Я передала информацию Анне. Она свяжется с вами в ближайшее время.")

    await state.clear()


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    print("Бот @MIAestetik_Studio_bot обновлен: лицо и старт коррекции добавлены!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
