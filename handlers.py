import logging

from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from keyboards import (
    create_inline_keyboard as inline_kb,
    create_keyboard_pole as pole_kb,
    update_keyboard
)
from aiogram_dialog import DialogManager, StartMode

from dialog_states import StartSG
from services import check_hit, get_text
from middleware import InnerMiddleware
from fsm_states import FSMState
from init_pole import Pole


logger = logging.getLogger(__name__)

router = Router()
#  router.message.middleware(InnerMiddleware())


@router.message(F.text, CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager, pole: Pole):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK, data={'pole': pole})
