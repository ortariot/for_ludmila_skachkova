from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import user_token, comm_token, offset, line
from fun import bot
from models import create_tables, User
from bdorm import engine
from models import check_vk_profile_id


session = vk_api.VkApi(token=comm_token)

for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = event.user_id

        if request == 'новый поиск':
            create_tables(engine)
            bot.user_info(user_id)
            while True:
                bot.userseach(user_id)
                ''''непонятно чт отут хотите? profile_id это что'''
                if check_vk_profile_id(profile_id) == False:
                    bot.userseach(user_id)
                else:
                    break
            bot.get_photo(user_id)
            bot.show_found_person(user_id)
            bot.write_msg(user_id, '1 - выбрать,  0 - пропустить, \nq - выход из поиска')

            ''''непонятно чт отут хотите? msg_text откуда берётся'''
            if msg_text == '1':
                bot.save_user(vk_id, vk_profile_id)
                 bot.write_msg(user_id, f' Отличный выбор')
            elif msg_text == '0':
                bot.userseach(user_id)
                bot.get_photo(user_id)
                bot.show_found_person(user_id)
            elif msg_text == 'q':
                 bot.write_msg(user_id, 'Введите Vkinder для активации бота')





