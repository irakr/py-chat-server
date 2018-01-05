# user.py

# Global dictionaries of users
all_users = {}
online_users = {}

class User:
    '''
    Represents a User entity.
    Note: A user object may still exist in the system even if not logged in.
    '''
    count = 0

    # Just instantiates a user object; not necessarily logs in the user.
    def __init__(self, id, name):
        self.__uid = uid
        self.__name = name
        self.__logged_in = False
        User.count += 1
        all_users[self.__uid] = self

    # Remove the user; also force log out.
    def __del__(self):
        User.count -= 1
        if self.__logged_in == True:
            self.log_out()
        try:
            del all_users[self.__uid]
        except KeyError:
            pass

    def log_in(self):
        self.__logged_in = True
        online_users[self.__uid] = self
        print '--->' + self.__uid + ' added to global dict.'

    def log_out(self):
        self.__logged_in = False
        # Silently remove from global online_user{} dict.
        try:
            del online_users[self.__uid]
        except KeyError:
            pass
