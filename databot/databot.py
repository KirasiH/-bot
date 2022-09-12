from databot.database import database

class DataBot:

    def __init__(self):

        self.__db = database

        self.group_suggestion_id = 1
        self.group_admin_id = 1
        self.group_request_id = 1

        self.ban_list = []
        self.user_list = [user for user in self.__db.list_users()]

        for group in database.groups():

            self.__add_group(group[1], group[0])

        for user in self.__db.list_users(ban=True):
            self.ban_list.append(user)

    def __add_group(self, name, group_id):

        if name == 'request':
            self.group_request_id = group_id

        elif name == 'suggestion':
            self.group_suggestion_id = group_id

        elif name == 'admin':
            self.group_admin_id = group_id

    def check_user(self, user_id):
        return self.__db.check_user(user_id)

    def add_user(self, user_id, name, phone_number, status_admin, status_block):

        self.__db.add_user(user_id, name, phone_number, status_admin, status_block)

    def delete_user(self, user_id):

        try:
            self.user_list.remove(user_id)

        except:
            pass

        else:
            self.__db.delete_user(user_id)

    def user_new_name_phone(self, user_id, phone=None, name=None):

        if phone:
            self.__db.user_new_phone(user_id, phone)

        if name:
            self.__db.user_new_name(user_id, name)

    def user_name(self, user_id):

        return self.__db.user_name(user_id)

    def user_phone(self, user_id):

        return self.__db.user_phone(user_id)

    def delete_group(self, group_id):

        for group in(self.group_admin_id, self.group_suggestion_id, self.group_request_id):
            if group == group_id:
                self.__db.delete_group(group_id)
                return

    def add_group(self, group_id, name):

        self.__add_group(name, group_id)
        self.__db.add_group(group_id, name)

    def user_new_status_block(self, user_id, status):

        if status == 1:
            self.ban_list.append(user_id)
            self.__db.user_new_status_block(user_id, status)

        else:
            try:
                self.ban_list.remove(user_id)

            except:
                pass

            else:
                self.__db.user_new_status_block(user_id, status)

    def list_users(self, ban=False):

        for i in self.__db.list_users(ban):
            yield i[0]

    def list_admin(self):

        data = self.__db.list_admin()

        if data == []:
            return data

        else:
            for i in data:
                yield i[0]

    def user_info(self, user_id):

        return self.__db.user_info(user_id)


databot = DataBot()

