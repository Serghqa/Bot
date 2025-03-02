import logging

from operator import itemgetter
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window, StartMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Group, Select
from pprint import pprint
from init_pole import Pole
from typing import List, Tuple

from dialog_states import StartSG
from services import check_hit

logger = logging.getLogger(__name__)


async def start_getter(**kwargs):
    user = kwargs.get('event_from_user')
    return {'username': user.username}


async def play_getter(pole: Pole, dialog_manager: DialogManager, **kwargs):
    play_status = pole.ships_pole
    dialog_manager.start_data['play_status'] = play_status
    return dialog_manager.start_data


async def start_play(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    pole: Pole = dialog_manager.start_data.get('pole')
    pole.__init__()
    pole.arrangement()
    keyboard = [('🌊', f'{i} {j}') for i in range(8) for j in range(8)]
    data = {'keyboard': keyboard, 'play_status': True, 'hit': False, 'kill': False, 'shots': {}}
    dialog_manager.start_data.update(data)
    await dialog_manager.next()


async def update_keyboard(
        callback: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str
):
    logger.info('update_keyboard')
    if item_id in dialog_manager.start_data['shots']:
        return
    dialog_manager.start_data['shots'][item_id] = True
    hit = False
    kill = False
    i, j = map(int, item_id.split())
    pole: Pole = dialog_manager.start_data.get('pole')
    if pole.pole[i][j] != 0:
        hit = True
        key = '🔥'
        for ship in pole.ships_pole:
            if (i, j) in ship.cell:
                ship.counter -= 1
                if ship.counter == 0:
                    pole.ships_pole.remove(ship)
                    hit = False
                    kill = True
                break
    else:
        key = '💩'
    keyboard: List[Tuple[str]] = dialog_manager.start_data.get('keyboard')
    for n, cell in enumerate(keyboard):
        if item_id == cell[1]:
            cell = (key, item_id)
            keyboard[n] = cell
            dialog_manager.start_data['kill'] = kill
            dialog_manager.start_data['hit'] = hit
            break
    if not dialog_manager.start_data.get('play_status'):
        await dialog_manager.next()


start_dialog = Dialog(
    Window(
        Format('Привет, {username}, это игра в Морской бой'),
        Const('Давай сыграем'),
        Button(text=Const('Играть'), id='play', on_click=start_play),
        getter=start_getter,
        state=StartSG.start,
    ),
    Window(
        Format('Жми кнопки', when='play_status'),
        Format('Ранил', when='hit'),
        Format('Убил', when='kill'),
        Group(
            Select(
                Format('{item[0]}'),
                id='cell',
                item_id_getter=itemgetter(1),
                items='keyboard',
                on_click=update_keyboard
            ),
            width=8,
            when='play_status',
        ),
        getter=play_getter,
        state=StartSG.play,
    ),
    Window(
        Const('Победа'),
        state=StartSG.win,
    ),
)
