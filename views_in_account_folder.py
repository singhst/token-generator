import hashlib
from store import Storage
from datetime import datetime, timedelta
import time

class UsersView():

    storage = Storage()

    def __init__(self):
        pass

    # === Sing <BEGIN> =======================
    # initial key = the HAS256 result of "userid+pw+time"
    def token_to_global(self, old_token) -> (str, str, str):
        """
        return
        ---
        old_token, new_token, the_global
        """
        new_token = hashlib.sha384(old_token.encode())
        new_token = new_token.hexdigest()

        the_global = hashlib.sha256(new_token.encode())
        the_global = the_global.hexdigest()

        return old_token, new_token, the_global

    def logout(self, the_global):
        self.storage.delete_one(the_global)

    def refresh_global(self, received_global: str, received_time):
        """
        process
        ---
        (1) check match (2) check timeout

        ==> if matched & no timeout

        (3) regennrate & update the global, and (4) send 'OK' http request
        """
        # received_time = datetime.now() + timedelta(minutes=30)

        # regenerate & update the token and global
        _, new_token, new_global = self.token_to_global(received_global)
        self.storage.update_one(received_global, new_global, new_token, received_time)
        print("> Global refreshed")
    # === Sing <END> =======================


if __name__ == "__main__":

    view = UsersView()

    print("\n==== System initialization ======================================")
    print(view.storage.global_storage_dict)

    print("\n==== an user log in ======================================")
    # process:      (1) generate token (2) generate global
    # for debug purpose
    print("@ before: ", view.storage.global_storage_dict)
    time = datetime.now()
    print(">", time)
    token = 'userid+pw+time'
    _, __, the_global = view.token_to_global(token)
    userid = '12312'
    # store it
    view.storage.insert_one(the_global, userid, token, time)
    # for debug purpose
    print("@ after: ", view.storage.global_storage_dict)

    print("\n==== within 30min, an user send a global refresh request ======================================")
    # received:     the global
    # process:      (1) check match (2) check timeout
    #               ==> if matched & no timeout
    #               (3) regennrate & update the global, and (4) send 'OK' http request
    received_global = the_global
    received_time = time + timedelta(minutes=30)
    # for debug purpose
    print("@ before: ", view.storage.global_storage_dict)
    view.refresh_global(received_global,received_time)
    # for debug purpose
    print("@ after: ", view.storage.global_storage_dict)

    print("\n==== after 50min, an user send a global-refresh request ======================================")
    # received:     the global
    # process:      (1) check match and timeout
    #               ==> if matched but timeout
    #               (2) log out user, and (3) send 'HTTP_403_FORBIDDEN'
    
    print(time.time())