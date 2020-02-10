from util.reader import get_item_info, get_user_click


def base_contribute():
    return 1


def cal_item_sim(user_click):
    """calculate the sim of two item
    计算物品间的相似度
    such as dict[userId1][userId2] is sim_score of the two user

    Args:
        user_click: key:userId, value:[item1, item2]
    Return:
        dict key:userId, value:{key:userId, value:sim_score}
    """
    co_appear = {}  # 记录item1与item2同时被同一个用户点击的用户个数
    item_user_click_item = {}  # 记录每个item被点击的次数
    for user_id, items in user_click.items():
        for index_i, item_i in enumerate(items):
            # 记录每个item被点击的次数 item_user_click_item
            if item_i not in item_user_click_item.keys():
                item_user_click_item[item_i] = 1
            else:
                item_user_click_item[item_i] += 1
            for index_j, item_j in enumerate(items):
                if index_i == index_j:  # 自己跟自己的相似度是1，不用记录
                    continue
                # 记录item1和item2同时出现的次数 co_appear
                if item_i not in co_appear.keys():
                    co_appear[item_i] = {}
                if item_j not in co_appear[item_i].keys():
                    co_appear[item_i][item_j] = 0
                co_appear[item_i][item_j] += base_contribute()

    # 计算item1与item2之间的相似度
    sim_info = {}
    for item_i, relate_item in co_appear.items():
        for item_j, co_time in relate_item.items():
            sim_score = co_time/(item_user_click_item[item_i]*item_user_click_item[item_j])**0.5  # item_cf 公式
            if item_i not in sim_info:
                sim_info[item_i] = {}
            sim_info[item_i][item_j] = sim_score

    # 排序，把与item1最相似的排前面
    for item_i, item_list in sim_info.items():
        # 字典排序sorted(dict.items(), key=lambda x: x[1])， 返回的是list
        sim_info[item_i] = sorted(sim_info[item_i].items(), key=lambda x: x[1], reverse=True)
    return sim_info


def cal_recommend_result(sim_info, user_click):
    """recommend by item_cf
    Args:
        sim_info: item_sim_dict, key:item_i, value:[{time_j:sim_score}]
        user_click: key:userId, value:[item1, item2]
    Return:
        dict key:user_id, value:dict{item_id, recommend_score}
    """
    recommend_result = {}
    recent_click_num = 3  # 最近点击的电影数目
    topK = 5  # 最相似的K个item
    for user_id, click_list in user_click.items():
        recommend_result[user_id] = {}
        for item in (click_list[:recent_click_num]):
            if item not in sim_info.keys():
                continue
            for item_sim_id, item_sim_score in (sim_info[item][:topK]):
                recommend_result[user_id][item_sim_id] = item_sim_score
    return recommend_result


def main_flow():
    """
    main flow of item_cf
    """
    user_click = get_user_click('../data/ratings.csv')  # 获得user[item1,item2]
    # 计算item与item直接的相似度
    sim_info = cal_item_sim(user_click)
    # print(sim_info)
    # 计算推荐结果
    recommend_result = cal_recommend_result(sim_info, user_click)
    print('推荐给userId=1的电影以及推荐度：')
    print(recommend_result[1])
    print('userId=1看过的电影')
    print(user_click[1])


if __name__ == '__main__':
    main_flow()
