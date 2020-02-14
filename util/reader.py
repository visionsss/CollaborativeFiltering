import pandas as pd
import numpy as np


def get_user_click(rating_file):
    """read rating file

    get user click list

    Arg:
        rating_file: input file[userId,movieId,rating,timestamp]

    Returns:
        user_click: dict key:userId, value:[itemId1, itemId2]
        user_click_time: key:'userId_movieId' value:timestamp
    """
    df = pd.read_csv(rating_file)  # 读取文件
    df = df.sample(2000, random_state=8)  # 采样
    df = df.sort_values(['timestamp'], ascending=False)  # 最近看的电影排前面
    user_click = {}
    user_click_time = {}
    for index, row in df.iterrows():  # 遍历
        row_id = int(row['userId'])
        movie_id = int(row['movieId'])
        time_stamp = int(row['timestamp'])
        if row['rating'] >= 3:  # 分数>=3
            if row_id not in user_click.keys():  # 如果userId不存在
                user_click[row_id] = [movie_id, ]  # 初始化
            else:
                user_click[row_id].append(movie_id)  # 添加value
            if str(row_id) + '_' + str(movie_id) not in user_click_time.keys():
                user_click_time[str(row_id) + '_' + str(movie_id)] = time_stamp

    return user_click, user_click_time


def get_item_info(item_file):
    """read item file

    get item info[title, genres]

    Args:
        item_file: input file[movieId,title,genres]

    Return:
        dict key: itemId, value:[title, genres]
    """
    item_info = {}
    df = pd.read_csv(item_file)
    for index, row in df.iterrows():
        movie_id = int(row['movieId'])
        item_info[movie_id] = [row['title'], row['genres']]
    return item_info


if __name__ == '__main__':
    ratings_file = '../data/ratings.csv'
    items_file = '../data/movies.csv'
    users_click = get_user_click(ratings_file)
    print(len(users_click), users_click[1])
    items_info = get_item_info(items_file)
    print(len(items_info), items_info[1])
