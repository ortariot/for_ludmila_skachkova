import vk_api
from config import user_token, comm_token, offset, line
import datetime
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType


class Bot:
    def __init__(self):
        print('Bot was created')
        self.session = vk_api.VkApi(token=user_token)
        self.vk = self.session.get_api()
        self.session_group = vk_api.VkApi(token=comm_token) 
        


    def write_msg(self, user_id, message):
        msg = self.session.method("messages.send",{"user_id" : user_id, 'message': message,'random_id': randrange(10 ** 7) })

    def user_info(self, user_id):
        resp = self.session.method("users.get",{"user_id" : user_id, "fields" : "sex , city , bdate"})
        '''здесь вы получаете один элемент в ответе, зачем вам все эти циклы? 
           исключеняи на такие большие куски кода ставить нельзя, ставьте более 'адресно'
        '''
        try:
            for i in resp:
                first_name = i.get('first_name')
            for s in resp:
                sex = s.get('sex')
                if sex == 2:
                    find_sex = 1
                elif sex == 1:
                    find_sex = 2
            for c in resp:
                city = c.get('city')
            title_city = city['title']
            for bd in resp:
                bdate = bd.get('bdate')
            date_list = bdate.split('.')
            year = int(date_list[2])
            year_now = int(datetime.date.today().year)
            age_from = ((year_now - year) - 5)
            age_to = ((year_now - year) + 5)
            dict_info = {'sex' : find_sex , 'city' : title_city, 'age_from' : age_from , 'age_to' : age_to}
            return dict_info
        except TypeError:
            self.write_msg(user_id, 'Профиль не заполнен ')

    def userseach(self, user_id):
        dict_info = self.user_info(user_id)
        response = self.session.method("users.search", {'sort': 1,
                                                   'sex': dict_info['sex'],
                                                   'status': 1,
                                                   'age_from': dict_info['age_from'],
                                                   'age_to': dict_info['age_to'],
                                                   'has_photo': 1,
                                                   'count': 1,
                                                   'fields': 'is_closed',
                                                   'hometown': dict_info['city']
                                                   })
        '''пример удачног оисключения'''
        
        try:
            response = response['items']
        except KeyError:
            return None         
        for element in response:
            if not element["is_closed"]:
                profile_id = element.get('id')
     
        return profile_id

    def get_photo(self, user_id):
        owner_id = self.userseach(user_id)

        response = self.session.method('photos.get',
                              {
                                  'access_token': user_token,
                                  'owner_id': owner_id,
                                  'album_id': 'profile',
                                  'extended': 1,
                                  'photo_sizes': 1,
                              })
        dict_photos = dict()
        for i in response['items']:
            photo_id = str(i["id"])
            i_likes = i["likes"]
            if i_likes["count"]:
                likes = i_likes["count"]
                dict_photos[likes] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        attachments = []
        photo_ids = []
        for i in list_of_ids:
            photo_ids.append(i[1])

            '''плоъая логика. напрмиер если у пользоватеял будет только 2 фото
                вы его отсяете если ошибка будет тут:
                attachments.append('photo{}_{}'.format(user_id, photo_ids[2]))

               '''
        try:
            attachments.append('photo{}_{}'.format(user_id, photo_ids[0]))
            attachments.append('photo{}_{}'.format(user_id, photo_ids[1]))
            attachments.append('photo{}_{}'.format(user_id, photo_ids[2]))
           
            return attachments
        except IndexError:
            attachments.append('photo{}_{}'.format(user_id, photo_ids[0]))
           
            return attachments


    def send_photo(self, user_id, message, attachments):

        response = self.session.method("messages.send",
                                       {
                                        "user_id" : user_id,
                                        'message': message,
                                        'random_id': randrange(10 ** 7),
                                        'attachment': ",".join(attachments)
                                       })


    def show_found_person(self, user_id):
        try:
            self.send_photo(user_id, 'Три фото с максимальными лайками')
            vk_link = 'vk.com/id' + str(self.userseach(user_id))
        except TypeError:
             return f' Похоже просмотренны все профили из БД. \n' \
                    f' Наберите "Искать дальше" для поиска и добавления в БД.'


bot = Bot()



        





