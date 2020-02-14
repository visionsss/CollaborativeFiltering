from util.reader import get_item_info, get_user_click
import math


def base_contribute(item_click_by_user_count, delta_time):
    """
    base contribute
    Args:
        item_click_by_user_count:how many users click the item
        delta_time: delta timestamp
    Return:
        base contribute
    """
    # return 1
    # return math.log10(1+item_click_by_user_count)
    delta_time = delta_time/(60*60*24)
    return 1/(1+delta_time)


def transfer_user_click(user_click):
    """
    transfer user_click
    Args:
        user_click: dict key:userId value:[item1, item2]
    Return:
        item_click_by_user: key:item, value:[user1, user2]
    """
    item_click_by_user = {}
    for user_id, items in user_click.items():
        for item in items:
            if item not in item_click_by_user.keys():
                item_click_by_user[item] = [user_id]
            else:
                item_click_by_user[item].append(user_id)
    return item_click_by_user


def cal_user_sim(item_click_by_user, user_click_time):
    """
    calculate user sim
    Args:
        item_click_by_user: key:item value:[user1, user2]
        user_click_time: list [(userId_movieId, timestamp)]
    Return:
        user_sim: key:user_i value:[(user_j, score),]
    """
    co_appear = {}  # 记录user1与user2同时点击一个item的次数
    user_item_click_item = {}  # 记录每个user点击的item次数
    for item, users in item_click_by_user.items():
        for user_i in users:
            if user_i not in user_item_click_item.keys():
                user_item_click_item[user_i] = 1
            else:
                user_item_click_item[user_i] += 1
            if user_i not in co_appear.keys():
                co_appear[user_i] = {}
            for user_j in users:
                if user_i == user_j:
                    continue
                if user_j not in co_appear[user_i].keys():
                    co_appear[user_i][user_j] = 0
                delta_time = abs(user_click_time[f'{user_j}_{item}'] - user_click_time[f'{user_i}_{item}'])
                co_appear[user_i][user_j] += base_contribute(len(users), delta_time)
    # calculate user1, user2 sim
    user_sim = {}
    for user_i, relate_user in co_appear.items():
        for user_j, co_time in relate_user.items():
            sim_score = co_time/(user_item_click_item[user_i]*user_item_click_item[user_j])**0.5
            if user_i not in user_sim.keys():
                user_sim[user_i] = {}
            user_sim[user_i][user_j] = sim_score

    # 排序，把与item1最相似的排前面
    for user_i, user_list in user_sim.items():
        # 字典排序sorted(dict.items(), key=lambda x: x[1])， 返回的是list
        user_sim[user_i] = sorted(user_sim[user_i].items(), key=lambda x: x[1], reverse=True)
    return user_sim


def cal_recommend_result(user_click, user_sim):
    """
    calculate recommend result
    Args:
        user_click: key:userId, value[item1, item2]
        user_sim: key:user1 value:[(user2, sim_score),()]
    Return:
        recommend_result:dict key:userId value:{item, sim_score}
    """
    recommend_result = {}
    topK_user = 3
    item_num = 5
    for user_i, item_list in user_click.items():
        recommend_result[user_i] = {}
        if user_i not in user_sim.keys():
            continue
        for (user_j, sim_score) in user_sim[user_i][:topK_user]:
            for item_i in item_list[-item_num:]:
                recommend_result[user_i][item_i] = sim_score
    return recommend_result


def main_flow():
    """
    main flow
    """
    user_click, user_click_time = get_user_click('../data/ratings.csv')  # 获得user[item1,item2]
    item_click_by_user = transfer_user_click(user_click)
    user_sim = cal_user_sim(item_click_by_user, user_click_time)
    recommend_result = cal_recommend_result(user_click, user_sim)
    print(recommend_result)


if __name__ == '__main__':
    main_flow()