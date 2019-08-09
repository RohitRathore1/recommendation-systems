# -*- coding: utf-8 -*-
"""
Created on Fri Aug 09 08:55:49 2019
@author: Rohit
"""

# numpy
# github repo at https://github.com/vinayak-mehta/Movie-Recommender-System/tree/master/data
import math
import numpy as np


def read_file():
    data = []

    with open('u.data') as fp:
        for line in fp.readlines()[: 100000]:
            things = line.split()
            convered_things = list(map(int, things))
            data.append(convered_things)
    uid = data[0][0]
    # print data

    return data


def pearson(rating1, rating2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in rating1:
        if key in rating2:
            n += 1
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
    # now compute denominator
    denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator


def main():
    num_dataP = 100000
    read_file()
    # user=940
    # item=1137
    data = read_file()
    test_sample = np.random.choice(num_dataP, num_dataP*0.25, replace='false')
    umat = {}
    sum_rate = 0
    count = 0
    c_user = 0
    sum_user = 0
    sum_wt = 0
    sum_error = 0
    num_success = 0
    for test_case, i in enumerate(test_sample):
        # print(data[i][0])
        user = data[i][0]
        item = data[i][1]
        orig_rating = data[i][2]

        for j, row in enumerate(data[:100000]):
            if j == i:
                continue
            uid, mid, rate, time = row
            if uid in umat:
                umat[uid][mid] = (rate)

            else:
                umat[uid] = {}
                umat[uid][mid] = rate

            if mid == item:
                sum_rate = sum_rate+rate
                count = count+1
            if uid == user:
                sum_user = sum_user+rate
                c_user = c_user+1
        # print umat

        mean_item = sum_rate/count
        mean_user = sum_user/c_user

        #print (mean_item)
        #print (mean_user)

        num = 0
        deno = 0
        weight_list = []
        u_user_ratings = {}
        v_user_ratings = {}
        movie_list = umat[user].keys()
        # print movie_list

        # for python 2for k,v in umat.iteritems() :
        for k, v in umat.items():
            if k != user:
                # print v.()
                # for v_key,v_value in v.iteritems():
                if item in v.keys():
                    common_movies = list(set(v.keys()) & set(movie_list))
                    # print common_movies
                    if len(common_movies) == 0:
                        print "nothing common :P"
                        continue
                    elif len(common_movies) != 0:
                        for i in common_movies:
                            # print k,i
                            u_user_ratings[i] = umat[user][i]
                            v_user_ratings[i] = umat[k][i]
                    weight = pearson(u_user_ratings, v_user_ratings)
                    # only positive weights will give me similarity?
                    if weight > 0:
                        deno = deno+weight

                    # weight_list.append(weight)
                        num = num+(umat[k][item]-mean_item)*weight
        if deno > 0:
            score = mean_user+(num/deno)

            print score, orig_rating, test_case
            # to calculate mean square error
            # number of things that got predicted = num_success
            num_success += 1
            sum_error = sum_error + (orig_rating-score)*(orig_rating-score)

    error = sum_error/num_success
    print error
    # print u_user_ratings


if __name__ == '__main__':
    main()
