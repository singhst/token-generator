"""
For storing user globals

# Python program to show that we can create
# instance variables inside methods
# ==> https://www.geeksforgeeks.org/python-classes-and-objects/
"""

from datetime import datetime, timedelta


class Storage:

    # Class Variable
    # The format of the dict to store globals
    global_storage_dict = {
        'global': {
            'userid': 'default',
            'token': 'default',
            'time': 'datetime object'
        }
    }

    # The init method or constructor
    def __init__(self):
        # Instance Variable
        # self.global_storage_dict = global_storage_dict
        pass

    def insert_one(self, the_global: str, userid: str, token: str, time: str):
        self.global_storage_dict.update(
            {the_global: {'userid': userid, 'token': token, 'time': time}})

    def insert_dict(self, x_dict: dict):
        self.global_storage_dict.update(x_dict)

    def update_one(self, old_global: str, new_global: str, new_token: str, new_time: str):
        """
        Update the global, token and time of an user based on previous global.
        """
        # changing global, token and the last refresh time
        self.global_storage_dict[new_global] = self.global_storage_dict.pop(old_global)
        self.global_storage_dict[new_global]['token'] = new_token
        self.global_storage_dict[new_global]['time'] = new_time

    def delete_one(self, the_global: str) -> dict:
        # Using pop() to remove a dict. pair
        removed_value = self.global_storage_dict.pop(the_global)
        return removed_value

    def get_global_dict(self) -> dict:
        return self.global_storage_dict

    def check_userid(self, input_userid: str):
        """
        Check whether the userid
        (1) exists in the dict
        """
        # Check existence
        for _,the_global in self.global_storage_dict.items():
            if the_global['userid'] == input_userid:
                print("> userid loged in")
                return True
        print("> userid didn't loged in")
        return False

    def check_global(self, input_global: str) -> bool:
        """
        Check whether the input global
        (1) exists in the dict
        """
        # Check existence
        if input_global in self.global_storage_dict:
            print("> Client global matched")
            return True
        else:
            print("> Client global not matched")

        return False

    def check_timeout(self, input_global: str, now_time: datetime, out_time_min=35) -> bool:
        """
        Check whether the input global
        (1) is time out or not
        """
        # Check timeout
        time_difference = now_time - self.global_storage_dict[input_global]['time']
        # if time difference <= out_time_min, i.e. no timeout
        print("> timedelta=", time_difference, end=', ')
        if time_difference <= timedelta(minutes=out_time_min):
            print("not time out")
            return True
        else:
            print("time out")
        
        return False

if __name__ == "__main__":
    global_storage = Storage()

    print("\n==== System initialization, the default data format of global")
    print(global_storage.global_storage_dict)

    print("\n==== an user log in, adds the global to dict type class var")
    # 1.
    # situation:    an user log in
    # process:      (1) generate token (2) generate global
    time = datetime.now()
    print(">", time)
    token = 'userid+pw+time'
    the_global = 'g0'
    userid = '12312'
    _init_login_token = {
        the_global: {
            'userid': userid,
            'token': token,
            'time': time
        }
    }
    # store it
    # global_storage.insert_dict(_init_login_token)
    global_storage.insert_one(the_global, userid, token, time)
    print(global_storage.global_storage_dict)

    print("\n==== within 30min, an user send a global refresh request")
    # 2.
    # situation:    within 30min, an user send a global-refresh request
    # received:     the global
    # process:      (1) check match (2) check timeout
    #               ==> if matched & no timeout
    #               (3) regennrate & update the global, and (4) send 'OK' http request
    time = datetime.now() + timedelta(minutes=30)
    received_global = 'g0'
    # if received global matches and not times out
    if global_storage.check_global(received_global):
        # regenerate & update the token and global
        new_token = 'new'
        new_global = 'g0_new'
        global_storage.update_one(received_global, new_global, new_token, time)
        print(global_storage.global_storage_dict)
        # send 'OK' http request
        print("> send OK request")

    print("\n==== after 50min, an user send a global-refresh request")
    # 3.
    # situation:    after 50min, an user send a global-refresh request
    # received:     the global
    # process:      (1) check match (2) check timeout
    #               ==> if matched but timeout
    #               (3) delete his/her global
    time = datetime.now() + timedelta(minutes=80)
    received_global = 'g0_new'
    # if received global matches but times out
    if ~global_storage.check_global(received_global):
        # delete the global
        global_storage.delete_one(received_global)
        print(global_storage.global_storage_dict)
        # send 'OK' http request
        print("> log out")