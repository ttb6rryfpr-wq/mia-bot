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

# Меню для лица (пока заглушка)
def get_face_procedures_keyboard():
    buttons = [
        [KeyboardButton(text="🌟 INDIBA RF (Лицо)")],
        [KeyboardButton(text="🧪 Пилинги и уход")],
        [KeyboardButton(text="◀️ Назад к категориям")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Здравствуйте! Я — Мия, виртуальный помощник студии эстетики и аппаратной косметологии Анны.\n"
        "Я помогу вам подобрать процедуру для идеального преображения и отвечу на все вопросы.\n\n"
        "Выберите направление:",
        reply_markup=get_categories_keyboard(),
    )
    await state.set_state(MiaStates.choosing_category)

@router.message(MiaStates.choosing_category, F.text == "🔥 Коррекция тела (Топ-запросы)")
async def category_body(message: Message, state: FSMContext):
    await message.answer("Выберите процедуру по телу:", reply_markup=get_body_procedures_keyboard())
    await state.set_state(MiaStates.choosing_procedure)

@router.message(MiaStates.choosing_category, F.text == "✨ Уход и омоложение лица")
async def category_face(message: Message, state: FSMContext):
    await message.answer("Направления по лицу скоро пополнятся новыми процедурами!", reply_markup=get_face_procedures_keyboard())
    await state.set_state(MiaStates.choosing_procedure)

@router.message(MiaStates.choosing_procedure, F.text == "◀️ Назад к категориям")
async def back_to_categories(message: Message, state: FSMContext):
    await message.answer("Выберите направление:", reply_markup=get_categories_keyboard())
    await state.set_state(MiaStates.choosing_category)

# Обработка выбора Криолиполиза
@router.message(MiaStates.choosing_procedure, F.text == "🧊 Криолиполиз")
async def choose_cryo(message: Message, state: FSMContext):
    await message.answer(
        "🧊 **Криолиполиз** — отличный метод удаления локальных жировых отложений холодом без операций.\n\n"
        "Выберите зону / количество манипул:",
        reply_markup=get_cryo_zones_keyboard(),
        parse_mode="Markdown"
    )

@router.message(F.text.in_({
    "Руки, бедра, бока (2 манипулы)", 
    "Живот и бока (4 манипулы)", 
    "Криолиполиз (6 манипул × 45 мин)"
}))
async def cryo_zone_selected(message: Message, state: FSMContext):
    await state.update_data(procedure=f"Криолиполиз: {message.text}")
    await ask_height_weight_flow(message, state)

@router.message(MiaStates.choosing_procedure, F.text == "◀️ К списку процедур")
async def back_to_body_list(message: Message, state: FSMContext):
    await message.answer("Выберите процедуру по телу:", reply_markup=get_body_procedures_keyboard())

# Обработка выбора Липосоникс
@router.message(MiaStates.choosing_procedure, F.text == "⚡ Липосоникс / ULFIT")
async def choose_liposonix(message: Message, state: FSMContext):
    await message.answer(
        "⚡ **Липосоникс / ULFIT** — мощный ультразвуковой лифтинг жировых ловушек.\n"
        "⚠️ *Обратите внимание: процедура проводится при размере одежды от 44-го.*\n\n"
        "Выберите зону:",
        reply_markup=get_liposonix_zones_keyboard(),
        parse_mode="Markdown"
    )

@router.message(F.text.in_({
    "Липосоникс — Живот", "Липосоникс — Бока", "Липосоникс — Бёдра", 
    "Липосоникс — Ягодицы", "Комплекс / Локальные отложения (Индивидуально)"
}))
async def liposonix_zone_selected(message: Message, state: FSMContext):
    await state.update_data(procedure=f"Липосоникс: {message.text}")
    await message.answer(
        "Укажите ваш **размер одежды** (напоминаем, процедура проводится строго при размере от 44-го):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MiaStates.waiting_for_clothing_size)

@router.message(MiaStates.waiting_for_clothing_size)
async def clothing_size_received(message: Message, state: FSMContext):
    await state.update_data(clothing_size=message.text)
    await ask_height_weight_flow(message, state)

# Обработка выбора Кавитации
@router.message(MiaStates.choosing_procedure, F.text == "🌊 Кавитация")
async def choose_cavitation(message: Message, state: FSMContext):
    await message.answer(
        "🌊 **Кавитация** — эффективное разрушение жировых клеток ультразвуком.\n\n"
        "Выберите длительность / формат:",
        reply_markup=get_cavitation_keyboard(),
        parse_mode="Markdown"
    )

@router.message(F.text.in_({"Кавитация 30 минут", "Кавитация 60 минут (несколько зон)"}))
async def cavitation_selected(message: Message, state: FSMContext):
    await state.update_data(procedure=f"Кавитация: {message.text}")
    await ask_height_weight_flow(message, state)

# Остальные процедуры тела (Лазерный липолиз, Индиба, RF-лифтинг)
@router.message(MiaStates.choosing_procedure, F.text.in_({
    "🏮 Лазерный липолиз", "📻 Индиба-массаж (Талия и живот)", "✨ RF-лифтинг тела (30 мин)"
}))
async def other_body_procedure(message: Message, state: FSMContext):
    await state.update_data(procedure=message.text)
    await ask_height_weight_flow(message, state)

async def ask_height_weight_flow(message: Message, state: FSMContext):
    await message.answer(
        "Укажите вашу **желаемую зону коррекции** своими словами (например: живот, бока, галифе, бедра):",
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
    await message.answer(
        f"Спасибо! Я рассчитала ваш индекс массы тела (ИМТ: {bmi}).\n"
        "Сколько вам полных лет?"
    )
    await state.set_state(MiaStates.waiting_for_age)

@router.message(MiaStates.waiting_for_age)
async def age_received(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(
        "Есть ли у вас основные противопоказания?\n"
        "(беременность/ГВ, онкология, кардиостимулятор, металлические импланты или грыжи в зоне обработки, эпилепсия)\n\n"
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

    # Если выбрана Индиба, спрашиваем про микротоки
    if "Индиба" in proc:
        await message.answer(
            "⚠️ **Важный вопрос для Индибы:**\n"
            "Используете ли вы параллельно любую микротоковую терапию?"
        )
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
        "Мы почти закончили! Чтобы забронировать время, представьтесь, пожалуйста. **Как вас зовут?**",
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
    await message.answer(
        "Поделитесь вашим **номером телефона** (нажмите кнопку ниже или введите цифры):",
        reply_markup=phone_keyboard
    )
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

    # Формируем карточку лида для вас
    lead_card = (
        "🔔 **НОВЫЙ ЗАПРОС ИЗ БОТА (@MIAestetik_Studio_bot)!**\n\n"
        f"👤 **Имя:** {data.get('name')}\n"
        f"📞 **Телефон:** {data.get('phone')}\n"
        f"💬 **Мессенджер:** {messenger}\n\n"
        f"⚙️ **Процедура:** {proc}\n"
        f"📍 **Зона:** {data.get('zone')}\n"
        f"📊 **Рост/Вес/Возраст:** {data.get('height')} см / {data.get('weight')} кг / {data.get('age')} лет\n"
        f"📐 **ИМТ:** {data.get('bmi')}\n"
        f"🛡 **Противопоказания:** {data.get('contra')}\n"
        f"⚡ **Доп. (размер/микротоки):** Размер: {data.get('clothing_size', 'н/д')} | Микротоки: {data.get('microcurrents')}"
    )

    try:
        await message.bot.send_message(ADMIN_CHAT_ID, lead_card, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Не удалось отправить лид администратору: {e}")

    # Определяем точную ссылку на DIKIDI или перевод на Анну
    has_contra = data.get("has_contra")
    dikidi_url = None

    # Маппинг ссылок DIKIDI
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

    # Выдача результата клиенту
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
        # Для 6 манипул крио, индивидуального липосоникса или при наличии противопоказаний — перевод на Анну
        await message.answer(
            "Готово! Я передала всю информацию Анне. Так как ваш запрос требует индивидуального расчета или уточнения деталей, "
            "Анна свяжется с вами лично в ближайшее время в указанном мессенджере."
        )

    await state.clear()

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    print("Бот @MIAestetik_Studio_bot полностью обновлен и запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())