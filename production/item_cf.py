from util.reader import get_item_info, get_user_click
import math


def base_contribute(item_len, delta_time):
    # return 1  # 原始贡献
    # return 1/math.log10(1+item_len)  # 降低活跃用户的贡献度
    total_sec = 60*60*24
    delta_time = delta_time/total_sec
    return 1/(1+delta_time)


def cal_item_sim(user_click, user_click_time):
    """calculate the sim of two item
    such as dict[itemId1][itemId2] is sim_score of the two item

    Args:
        user_click: key:userId, value:[item1, item2]
        user_click_time: list [(userId_movieId, timestamp)]
    Return:
        dict key:item_i, value:list({key:item_j, value:sim_score})
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
            if item_i not in co_appear.keys():
                co_appear[item_i] = {}
            for index_j, item_j in enumerate(items):
                if index_i == index_j:  # 自己跟自己的相似度是1，不用记录
                    continue
                # 记录item1和item2同时出现的次数 co_appear
                if item_j not in co_appear[item_i].keys():
                    co_appear[item_i][item_j] = 0
                delta_time = abs(user_click_time[f'{user_id}_{item_i}']-user_click_time[f'{user_id}_{item_j}'])
                co_appear[item_i][item_j] += base_contribute(len(items), delta_time)

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
        for item in (click_list[-recent_click_num:]):
            if item not in sim_info.keys():
                continue
            for item_sim_id, item_sim_score in (sim_info[item][:topK]):
                recommend_result[user_id][item_sim_id] = item_sim_score

    return recommend_result


def debug_item_sim(item_info, sim_info):
    """
    show item info
    Args:
        item_info:dict key:itemId, value:[title, genre]
        sim_info:dict key:itemId, value{itemId2, score}
    """
    itemId = 2
    if itemId not in item_info.keys():
        print("not this itemId")
    [item_title, item_genre] = item_info[itemId]
    print(item_title)
    for itemId2, score in sim_info[itemId][:10]:
        [title2, genre2] = item_info[itemId2]
        print(title2, score)


def debug_recommend_result(recommend_result, item_info):
    """
    debug_recommend_result
    Args:
         recommend_result: dict key:userId, value:{itemId:score}
         item_info: dict key:itemId, value:[title, genre]
    """
    # recommend_result sorted
    for key, value in recommend_result.items():
        recommend_result[key] = sorted(recommend_result[key].items(), key=lambda x: x[1], reverse=True)
    user_id = 1
    print('给userId推荐的电影为')
    for item_id, score in recommend_result[user_id]:
        print(item_info[item_id][0], score)


def main_flow():
    """
    main flow of item_cf
    """
    user_click, user_click_time = get_user_click('../data/ratings.csv')  # 获得user[item1,item2]
    # 计算item与item直接的相似度
    sim_info = cal_item_sim(user_click, user_click_time)
    # print(sim_info)
    # 计算推荐结果
    recommend_result = cal_recommend_result(sim_info, user_click)

    item_info = get_item_info('../data/movies.csv')  # 获得{movieId:[title, genre]}
    debug_item_sim(item_info, sim_info)
    debug_recommend_result(recommend_result, item_info)


if __name__ == '__main__':
    main_flow()
