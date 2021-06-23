import math


class Queue_objects:
    def __init__(
        self,
        total_users,
        hardlimit,
        hardlimit_users_parcentage,
        default_limit,
    ):
        self.hardlimit = hardlimit
        self.default_limit = default_limit

        self.users_using_hardlimit = math.ceil(
            total_users * (hardlimit_users_parcentage / 100)
        )
        users_using_default_limit = total_users - self.users_using_hardlimit
        self.total_items_of_husers = hardlimit * self.users_using_hardlimit
        total_items_of_dusers = default_limit * users_using_default_limit
        self.total_itemsum = self.total_items_of_husers + total_items_of_dusers

        # heavy_itemsの割合は、l_user,s_user全体でそれぞれ1割ずつ
        self.heavy_items_of_husers = math.ceil(self.total_items_of_husers * 0.1)
        self.heavy_items_of_dusers = math.ceil(total_items_of_dusers * 0.1)

    def get_record(self, user_id, item_id, default):
        return {
            "user_id": user_id,
            "item_id": item_id,
            "default": default,
        }

    def queue_objects(self, queue) -> None:
        husers_item_list = zip(
            *[iter(range(1, self.total_items_of_husers + 1))] * self.hardlimit
        )
        for user_id, user_items in enumerate(husers_item_list):
            user_id += 1
            for item_id in user_items:
                if item_id <= self.heavy_items_of_husers:
                    default = False
                    queue.put(
                        self.get_record(
                            user_id,
                            item_id,
                            default,
                        )
                    )
                    continue
                default = True
                queue.put(self.get_record(user_id, item_id, default))

        # s_userで作成されるuser_idとitem_idは、l_userの続きになるようにする
        start_item_id_of_dusers = self.total_items_of_husers + 1
        end_item_id_of_dusers_heavy_items = (
            self.total_items_of_husers + self.heavy_items_of_dusers
        )
        s_user_items_list = zip(
            *[iter(range(start_item_id_of_dusers, self.total_itemsum + 1))]
            * self.default_limit
        )
        for user_id, user_items in enumerate(s_user_items_list):
            user_id += self.users_using_hardlimit + 1
            for item_id in user_items:
                if item_id <= end_item_id_of_dusers_heavy_items:
                    default = False
                    queue.put(
                        self.get_record(
                            user_id,
                            item_id,
                            default,
                        )
                    )
                    continue
                default = True
                queue.put(self.get_record(user_id, item_id, default))
