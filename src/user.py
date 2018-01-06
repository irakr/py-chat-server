# user.py

import logging_wrapper as logw
logger = logw.createLogger(__name__)

# Global dictionaries of users
all_users = {}
online_users = {}

class User(object):
    """
    Represents a User entity.
    Note: A user object may still exist in the system even if not logged in.

    Privilege levels: 0(No privilege), 1(Normal user), 2(Admin).
    """
    count = 0

    """
    Args:
        id -- Unique user ID. id = -1 for a Dummy user.
        name -- Name of the user. name = 'Dummy' for a Dummy user.
    """
    # Just instantiates a user object; not necessarily logs in the user.
    def __init__(self, id=-1, name='Dummy'):
        self.__uid = id
        self.__name = name[:]
        self.__logged_in = False
        self.privilege = 0
        User.count += 1
        all_users[self.__uid] = self

    # Remove the user; also force log out.
    def remove(self):
        if self.__logged_in == True:
            self.log_out()
        try:
            del all_users[self.__uid]
        except KeyError:
            pass

    def __del__(self):
        if User:
            User.count -= 1

    def log_in(self):
        self.__logged_in = True
        online_users[self.__uid] = self
        logger.debug('---> + %s + added to global dict.', self.__uid)

    def log_out(self):
        self.__logged_in = False
        # Silently remove from global online_user{} dict.
        try:
            del online_users[self.__uid]
        except KeyError:
            pass

class AdminUser(User):
    """ Admin user with the highest privileges. """
    def __init__(self, id, name):
        super(AdminUser, self).__init__(id, name)
        self.privilege = 2

class RegularUser(User):
    """ Regular user with normal privileges only. Does not have control
        of the ServerControl commands.
    """
    def __init__(self, id, name):
        super(RegularUser, self).__init__(id, name)
        self.privilege = 1
