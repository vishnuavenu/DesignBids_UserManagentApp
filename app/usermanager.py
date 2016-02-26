import os
import pwd
from app import APP_GID
import pdb
import crypt
import subprocess

class UserManager(object):
    def __init__(self):
        self.user_table = []
        self.update_table()

    def get_all_users(self, gid):
        """
        :param gid: Application group Id : APP_GID
        :return: List of users registered in the applcation
        """
        self.update_table()
        return list(filter(lambda user: user['gid'] == gid, self.user_table))

    def update_table(self):
        """
        Updates the user_table with current data
        :return:
        """

        del self.user_table[:]  # cleaning previous record ..

        for user in pwd.getpwall():
            if user.pw_gid == APP_GID:
                san_user = dict()  # Sanitized user data
                san_user['username'] = user.pw_name
                san_user['password'] = user.pw_passwd
                san_user["home"] = user.pw_dir
                san_user["shell"] = user.pw_shell
                san_user["uid"] = user.pw_uid
                san_user["gid"] = user.pw_gid
                self.user_table.append(san_user)
                del san_user

    def register_user(self, user, gid):
        try:
            encPass = crypt.crypt(user["password"], "22")
            os.system("useradd  %s -p %s -m -d %s -s %s -g %d " % (user['username'], encPass, user["home"], user['shell'], gid))

        except KeyError as e:
            print(e)
            return False
        except OSError as e:
            print(" [+] OS ERROR .....   ")
            print(e)
            return False
        finally:
            self.update_table()
            # pdb.set_trace()
            return True  # operation successfull


    def update_user(self, user, gid):

        print("From the update : ")
        print(user)
        try:
            os.system("usermod -l %s -m -d %s -s %s -g %d  %s" %
                      (str(user["username"]), str(user["home"]),
                       str(user["shell"]),gid, str(user["previous_name"])))
        except KeyError as e:
            print(e)
            return False  # Missing Info
        except subprocess.SubprocessError as e:
            print(" [+] OS ERROR .....  :/ ")
            print(e)
            return False  # Internal Error
        finally:
            self.update_table()
            return True  # operation successful


    def remove_user(self, uid):
        try:
            username = self.find_user_by_uid(int(uid))["username"]
            print("USER %s" % username)
            # os.system("userdel -r %s " % str(username)) # total annihilation

            subprocess.call(["userdel",
                             "-r",
                             "%s" % str(username)
                             ]) # total annihilation
        except subprocess.SubprocessError as e:
            print(" [+] OS ERROR .....  :/ ")
            print(e)
            return False  # Internal Error
        finally:
            self.update_table()
            print("[+] Refresh ...... after Removal")
            return True # operation successful

    def find_user_by_name(self, name):
        for user in self.user_table:
            if user["username"] == name:
                return user
        return None

    def find_user_by_uid(self, uid):
        for user in self.user_table:
            if user["uid"] == uid:
                return user
        return None


