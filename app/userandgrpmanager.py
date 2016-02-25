import os
import pwd
import grp


class UserandGrpManager(object):
    def __init__(self):
        self.user_table = []
        self.group_table = []

    def getallusers(self, gid):
        self.update()
        return list(filter(lambda user: user[
                                            'gid'] == gid, self.user_table))

    def getallgroup(self):
        return self.group_table

    def update(self):
        del self.user_table[:]  # cleaning previous record ..
        for user in pwd.getpwall():
            san_user = {}
            san_user['username'] = user.pw_name
            san_user['password'] = user.pw_passwd
            san_user["home"] = user.pw_dir
            san_user["shell"] = user.pw_shell
            san_user["uid"] = user.pw_uid
            san_user["gid"] = user.pw_gid
            self.user_table.append(san_user)

        del self.group_table[:] # Delete Previous Record
        for group in grp.getgrall():
            san_grp= {}
            san_grp["grpname"] = group.gr_name
            san_grp["password"] = group.gr_passwd
            san_grp["gid"] = group.gr_gid
            san_grp["mem"] = group.gr_mem
            self.group_table.append(san_grp)

    def register_user(self,user,gid):
        self.update()
        try:
            os.system("useradd  %s -p %s -m -d %s -s %s -g %d " %
            (user['username'], user["password"], user["home"], user['shell'], gid))
        except KeyError:
            return False
        except OSError:
            return False
        return True


    def update_user(self,user, gid):
        self.update()
        try:
            os.system("usermod -l %s -p %s -m -d %s -s %s -g %d %s" %
            (user["username"], user["password"], user["home"], user["shell"], gid, user["actual_name"]))
            self.update()
        except KeyError:
            return False  # Missing Info
        except OSError:
            print(" [+] Some OS ERROR .....  :/ ")
            return False  # Internal Error
        return True


    def remove_user(self, name):
        self.update()
        try:
            os.system("userdel -r %s "%(name)) # total annihilation
        except OSError:
            return False
        return True # operation successfull

    def find_user_by_name(self, name):
        self.update()
        for user in self.user_table:
            if user["username"] == name:
                return user
        return None

    def find_user_by_uid(self, uid):
        self.update()
        for user in self.user_table:
            if user["uid"] == uid:
                pass

    def find_group_by_name(self, name):
        self.update()
        for _grp in self.group_table:
            if _grp["grpname"] == name:
                return _grp
        return None

    def find_group_by_gid(self, gid):
        self.update()
        for _grp in self.group_table:
            if _grp["gid"] == gid:
                return _grp
        return None

