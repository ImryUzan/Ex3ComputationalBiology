import csv
import random
import matplotlib.pyplot as plot
import datetime
import os
import copy
import numpy as np
import sys

LR = 0.1
ne_1 = 0.5
ne_2 = 0.25
ne_3 = 0.125




def create_one_random_vec(vec_size,min_possible_val, max_possible_val):
    new_vec = []

    for i in range(0,vec_size):
        #norm
        if i == 0:
            #economic amount
            val_one_cell = random.randint(1, 10)/10
            #val_one_cell = random.randint(1, 10)
        else:
            val_one_cell = random.randint(min_possible_val, max_possible_val)/max_possible_val
        new_vec.append(val_one_cell)

    return new_vec


def create_new_som(first_line_size = 5,mid_line_size = 9,vec_size = 15,min_possible_val = 0, max_possible_val = 300000):

    new_som = []


    #create the upper lines
    for line_size in range(first_line_size,mid_line_size):
        new_line = []
        for i in range(0,line_size):
            random_vec = create_one_random_vec(vec_size,min_possible_val, max_possible_val)
            new_line.append(random_vec)

        new_som.append(new_line)

    #create the mid line
    new_line = []
    for i in range(0, mid_line_size):
        random_vec = create_one_random_vec(vec_size, min_possible_val, max_possible_val)
        new_line.append(random_vec)

    new_som.append(new_line)


    #create the lower lines
    for line_size_opo in range(first_line_size,mid_line_size):
        line_size = mid_line_size + first_line_size - 1 - line_size_opo
        new_line = []
        for i in range(0,line_size):
            random_vec = create_one_random_vec(vec_size,min_possible_val, max_possible_val)
            new_line.append(random_vec)

        new_som.append(new_line)


    return new_som





#make sure the vecs are in the same len
def check_distance(vec_1,vec_2):
    dist  = -1
    if len(vec_1) != len(vec_2):
        print("worng size!!! cannot calculate the distant!!!")

    else:
        sum_err = 0
        for index in range(0,len(vec_1)):
            err = vec_1[index] -  vec_2[index]
            sum_err = sum_err + pow(err,2)

        dist = pow(sum_err,0.5)

    return dist




#find the closest ne
def find_most_close_cell(som_fild,vec_to_check):
    save_sec_min_line = 0
    save_sec_min_cell = 0
    save_min_line = 0
    save_min_cell = 0
    save_min_dist = -1
    is_first_time = True

    for line_index in range(0,len(som_fild)):
        for cell_index in range(0,len(som_fild[line_index])):
            dist = check_distance(som_fild[line_index][cell_index],vec_to_check)

            if is_first_time:
                save_min_dist = dist
                is_first_time = False

            elif dist < save_min_dist:
                save_sec_min_line = save_min_line
                save_sec_min_cell = save_min_cell
                save_min_dist = dist
                save_min_line = line_index
                save_min_cell = cell_index



    return (save_min_line,save_min_cell,save_min_dist),(save_sec_min_line,save_sec_min_cell)





# make sure the xcel file is in the same directory like the python file
def exstrac_data_from_xcel(file_path):

    # Give the location of the file
    path = file_path

    file = open(path)
    csvreader = csv.reader(file)

    rows = []
    for row in csvreader:
        rows.append(row)


    return rows






def change_the_firs_nes(som_fild,row,col,dest_vec,LR,ne_2,ne_3,zero_som,is_recursicv):

    #right ne
    if col > 0 and (zero_som[row][col-1] != 1 or is_recursicv):

        if is_recursicv:
            som_fild, zero_som = change_the_firs_nes(som_fild, row, col-1, dest_vec, LR, ne_3, 0, zero_som,False)

        else:
            zero_som[row][col - 1] = 1
            for index_in_vec in range(0, len(som_fild[row][col])):
                som_fild[row][col-1][index_in_vec] = som_fild[row][col-1][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row][col-1][index_in_vec])



    #left ne
    if col < len(som_fild[row])-1 and (zero_som[row][col + 1] != 1 or is_recursicv):
        if is_recursicv:
            som_fild, zero_som = change_the_firs_nes(som_fild, row, col+1, dest_vec, LR, ne_3, 0, zero_som,False)
        else:
            zero_som[row][col + 1] = 1
            for index_in_vec in range(0, len(som_fild[row][col])):
                som_fild[row][col+1][index_in_vec] = som_fild[row][col+1][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row][col+1][index_in_vec])



    if row == 0:
        if zero_som[row + 1][col + 1] != 1 or is_recursicv:
            if is_recursicv:
                som_fild, zero_som = change_the_firs_nes(som_fild, row +1, col + 1, dest_vec, LR, ne_3, 0, zero_som,False)
            else:
                for index_in_vec in range(0, len(som_fild[row][col])):
                    som_fild[row+1][col+1][index_in_vec] = som_fild[row+1][col+1][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row+1][col+1][index_in_vec])

                zero_som[row + 1][col + 1] = 1

        if zero_som[row + 1][col] != 1 or is_recursicv:
            if is_recursicv:
                som_fild, zero_som = change_the_firs_nes(som_fild, row + 1, col, dest_vec, LR, ne_3, 0, zero_som,False)
            else:
                for index_in_vec in range(0, len(som_fild[row][col])):
                    som_fild[row+1][col][index_in_vec] = som_fild[row+1][col][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row+1][col][index_in_vec])

                zero_som[row + 1][col] = 1



    elif row == (len(som_fild) - 1):
        if zero_som[row -1][col +1] != 1 or is_recursicv:
            if is_recursicv:
                som_fild, zero_som = change_the_firs_nes(som_fild, row -1, col+1, dest_vec, LR, ne_3, 0, zero_som,False)
            else:
                for index_in_vec in range(0, len(som_fild[row][col])):
                    som_fild[row-1][col+1][index_in_vec] = som_fild[row-1][col+1][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row-1][col+1][index_in_vec])

                zero_som[row - 1][col + 1] = 1

        if zero_som[row-1][col] != 1 or is_recursicv:
            if is_recursicv:
                som_fild, zero_som = change_the_firs_nes(som_fild, row - 1, col, dest_vec, LR, ne_3, 0, zero_som,False)
            else:
                for index_in_vec in range(0, len(som_fild[row][col])):
                    som_fild[row-1][col][index_in_vec] = som_fild[row-1][col][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row-1][col][index_in_vec])

                zero_som[row - 1][col] = 1

    else:
        #if i am in the upper part of the fild
        if len(som_fild[row]) > len(som_fild[row -1]) and not len(som_fild[row]) > len(som_fild[row + 1]):

            if zero_som[row + 1][col + 1] != 1 or is_recursicv:
                if is_recursicv:
                    som_fild, zero_som = change_the_firs_nes(som_fild, row +1 , col+1, dest_vec, LR, ne_3, 0, zero_som,False)
                else:
                    for index_in_vec in range(0, len(som_fild[row][col])):
                        som_fild[row + 1][col + 1][index_in_vec] = som_fild[row + 1][col + 1][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row + 1][col + 1][index_in_vec])
                    zero_som[row + 1][col + 1] = 1

            if zero_som[row + 1][col] != 1 or is_recursicv:
                if is_recursicv:
                    som_fild, zero_som = change_the_firs_nes(som_fild, row + 1, col, dest_vec, LR, ne_3, 0, zero_som,False)

                else:
                    for index_in_vec in range(0, len(som_fild[row][col])):
                        som_fild[row + 1][col][index_in_vec] = som_fild[row + 1][col][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row + 1][col][index_in_vec])
                    zero_som[row + 1][col] = 1

            if col > 0 and (zero_som[row - 1][col - 1] != 1or is_recursicv):
                if is_recursicv:
                    som_fild, zero_som = change_the_firs_nes(som_fild, row - 1, col-1, dest_vec, LR, ne_3, 0, zero_som,False)
                else:
                    for index_in_vec in range(0, len(som_fild[row][col])):
                        som_fild[row - 1][col - 1][index_in_vec] = som_fild[row - 1][col - 1][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row - 1][col - 1][index_in_vec])
                    zero_som[row - 1][col - 1] = 1

            if col < len(som_fild[row])-1 and (zero_som[row - 1][col] != 1 or is_recursicv):
                if is_recursicv:
                    som_fild, zero_som = change_the_firs_nes(som_fild, row - 1, col, dest_vec, LR, ne_3, 0, zero_som, False)
                else:
                    for index_in_vec in range(0, len(som_fild[row][col])):
                        som_fild[row - 1][col][index_in_vec] = som_fild[row - 1][col][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row - 1][col][index_in_vec])
                    zero_som[row - 1][col] = 1


        #bottom part
        elif len(som_fild[row]) > len(som_fild[row + 1]) and not len(som_fild[row]) > len(som_fild[row - 1]):
            if zero_som[row - 1][col + 1] != 1 or is_recursicv:
                if is_recursicv:
                    som_fild, zero_som = change_the_firs_nes(som_fild, row - 1, col+1, dest_vec, LR, ne_3, 0, zero_som,False)
                else:
                    for index_in_vec in range(0, len(som_fild[row][col])):
                        som_fild[row - 1][col + 1][index_in_vec] = som_fild[row - 1][col + 1][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row - 1][col + 1][index_in_vec])
                    zero_som[row - 1][col + 1] = 1


            if zero_som[row - 1][col] != 1 or is_recursicv:
                if is_recursicv:
                    som_fild, zero_som = change_the_firs_nes(som_fild, row - 1, col, dest_vec, LR, ne_3, 0, zero_som, False)
                else:
                    for index_in_vec in range(0, len(som_fild[row][col])):
                        som_fild[row - 1][col][index_in_vec] = som_fild[row - 1][col][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row - 1][col][index_in_vec])
                    zero_som[row - 1][col] = 1

            if col > 0 and (zero_som[row + 1][col - 1] != 1 or is_recursicv):
                if is_recursicv:
                    som_fild, zero_som = change_the_firs_nes(som_fild, row + 1, col-1, dest_vec, LR, ne_3, 0, zero_som,False)
                else:
                    for index_in_vec in range(0, len(som_fild[row][col])):
                        som_fild[row + 1][col - 1][index_in_vec] = som_fild[row + 1][col - 1][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row + 1][col - 1][index_in_vec])
                    zero_som[row + 1][col - 1] = 1

            if col < len(som_fild[row]) - 1 and (zero_som[row + 1][col] != 1 or is_recursicv):
                if is_recursicv:
                    som_fild, zero_som = change_the_firs_nes(som_fild, row + 1, col, dest_vec, LR, ne_3, 0, zero_som, False)
                else:
                    for index_in_vec in range(0, len(som_fild[row][col])):
                        som_fild[row + 1][col][index_in_vec] = som_fild[row + 1][col][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row + 1][col][index_in_vec])
                    zero_som[row + 1][col] = 1

        #midle line
        else:

            if col > 0:
                if zero_som[row + 1][col - 1] != 1 or is_recursicv:
                    if is_recursicv:
                        som_fild, zero_som = change_the_firs_nes(som_fild, row + 1, col - 1, dest_vec, LR, ne_3, 0, zero_som, False)
                    else:
                        for index_in_vec in range(0, len(som_fild[row][col])):
                            som_fild[row + 1][col - 1][index_in_vec] = som_fild[row + 1][col - 1][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row + 1][col - 1][index_in_vec])
                        zero_som[row + 1][col - 1] = 1


                if zero_som[row - 1][col - 1] != 1 or is_recursicv:
                    if is_recursicv:
                        som_fild, zero_som = change_the_firs_nes(som_fild, row - 1, col - 1, dest_vec, LR, ne_3, 0,zero_som, False)
                    else:
                        for index_in_vec in range(0, len(som_fild[row][col])):
                            som_fild[row - 1][col - 1][index_in_vec] = som_fild[row - 1][col - 1][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row - 1][col - 1][index_in_vec])
                        zero_som[row - 1][col - 1] = 1


            if col < len(som_fild[row]) - 1:
                if zero_som[row + 1][col] != 1 or is_recursicv:
                    if is_recursicv:
                        som_fild, zero_som = change_the_firs_nes(som_fild, row + 1, col, dest_vec, LR, ne_3, 0,zero_som, False)
                    else:
                        for index_in_vec in range(0, len(som_fild[row][col])):
                            som_fild[row + 1][col][index_in_vec] = som_fild[row + 1][col][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row + 1][col][index_in_vec])
                        zero_som[row + 1][col] = 1


                if zero_som[row - 1][col] != 1 or is_recursicv:
                    if is_recursicv:
                        som_fild, zero_som = change_the_firs_nes(som_fild, row - 1, col, dest_vec, LR, ne_3, 0,zero_som, False)
                    else:
                        for index_in_vec in range(0, len(som_fild[row][col])):
                            som_fild[row - 1][col][index_in_vec] = som_fild[row - 1][col][index_in_vec] + LR * ne_2 * (dest_vec[index_in_vec] - som_fild[row - 1][col][index_in_vec])
                        zero_som[row - 1][col] = 1


    return som_fild,zero_som




def create_zero_som(first_line_size = 5,mid_line_size = 9,vec_size = 15,min_possible_val = 0, max_possible_val = 300000):

    zero_som = []


    #create the upper lines
    for line_size in range(first_line_size,mid_line_size):
        new_line = []
        for i in range(0,line_size):
            new_line.append(0)

        zero_som.append(new_line)

    #create the mid line
    new_line = []
    for i in range(0, mid_line_size):
        new_line.append(0)

    zero_som.append(new_line)


    #create the lower lines
    for line_size_opo in range(first_line_size,mid_line_size):
        line_size = mid_line_size + first_line_size - 1 - line_size_opo
        new_line = []
        for i in range(0,line_size):
            new_line.append(0)

        zero_som.append(new_line)


    return zero_som






def change_som_fild(som_fild,row,col,dest_vec,LR,ne_1,ne_2,ne_3):

    zero_som = create_zero_som()
    is_recursicv = False
    for index_in_vec in range(0,len(som_fild[row][col])):
        #change the chosen cell
        som_fild[row][col][index_in_vec] = som_fild[row][col][index_in_vec] + LR * ne_1 * (dest_vec[index_in_vec] - som_fild[row][col][index_in_vec])

    zero_som[row][col] = 1
    som_fild,zero_som = change_the_firs_nes(som_fild, row, col, dest_vec, LR, ne_2,ne_3,zero_som,is_recursicv)
    som_fild, zero_som = change_the_firs_nes(som_fild, row, col, dest_vec, LR, ne_3, ne_3,zero_som,True)


    return som_fild




def check_if_sec_and_first_best_are_close(tupple_index_and_min_dist,tupple_index_sec_best,LR,ne_1,ne_2,ne_3):
    dist_x = abs(tupple_index_and_min_dist[0] - tupple_index_sec_best[0])
    dist_y = abs(tupple_index_and_min_dist[1] - tupple_index_sec_best[1])
    if dist_x <=1 and dist_y <=1:
        return True
    else:
        return False


def run_one_step(dict_city_name_to_tupple_eco_and_list,som_fild,city_and_most_close_index,is_first_time, LR, ne_1, ne_2, ne_3):
    should_stop = True
    save_city_and_most_close_index = {}
    sum = 0
    amount = 0
    for city_name,tupple in dict_city_name_to_tupple_eco_and_list.items():
        amount = amount +1
        tupple_index_and_min_dist,tupple_index_sec_best = find_most_close_cell(som_fild,tupple[1])
        is_close = check_if_sec_and_first_best_are_close(tupple_index_and_min_dist, tupple_index_sec_best,LR,ne_1,ne_2,ne_3)
        save_city_and_most_close_index[city_name] = (tupple_index_and_min_dist[0],tupple_index_and_min_dist[1])
        if not is_first_time:
            if save_city_and_most_close_index[city_name] != city_and_most_close_index[city_name] or not is_close:
                sum = sum+1
        else:
            should_stop = False

        som_fild = change_som_fild(som_fild, tupple_index_and_min_dist[0], tupple_index_and_min_dist[1], tupple[1], LR, ne_1, ne_2, ne_3)

    if should_stop:
        avg = sum/amount
        if avg > 0.1:
            should_stop = False

    return som_fild,save_city_and_most_close_index,should_stop



#run the som algo - 300 updates
def run_algo_som(file_path,LR,ne_1,ne_2,ne_3):
    rows = exstrac_data_from_xcel(file_path)

    subjects_list = rows.pop(0)
    random.shuffle(rows)
    som_fild = create_new_som()


    dict_city_name_to_tupple_eco_and_list = {}

    for line_index in range(0,len(rows)):
        city_name = rows[line_index].pop(0)
        Economic_Cluster = rows[line_index][0]
        total_vote = rows[line_index][1]

        for cell_ind in range(0,len(rows[line_index])):
            if cell_ind == 0:
                # norm
                rows[line_index][cell_ind] = int(rows[line_index][cell_ind])/10
            else:
                #norm
                rows[line_index][cell_ind] = int(rows[line_index][cell_ind])/int(total_vote)

        dict_city_name_to_tupple_eco_and_list[city_name] = (int(Economic_Cluster),rows[line_index])

    save_city_and_most_close_index = {}
    is_first_time = True

    fleg_arrive_to_end_cond = False
    for i in range(0, 300):
        #run the basic algo one time
        som_fild,save_city_and_most_close_index,should_stop = run_one_step(dict_city_name_to_tupple_eco_and_list, som_fild,save_city_and_most_close_index,is_first_time, LR, ne_1, ne_2, ne_3)
        is_first_time = False
        sum_dist = 0
        number_of_cities = 0
        for city, index in save_city_and_most_close_index.items():
            sum_dist = check_distance(dict_city_name_to_tupple_eco_and_list[city][1],som_fild[index[0]][index[1]])
            number_of_cities = number_of_cities + 1

        avg_dist = sum_dist/number_of_cities


        if should_stop and i > 70:
            fleg_arrive_to_end_cond = True
            break

    return som_fild,avg_dist,fleg_arrive_to_end_cond,save_city_and_most_close_index



#distance of one node from all hi neighbors
def distance_one_node(som_fild,raw_index,col_index):
   # check_distance

    list_indexes_to_check =[]

    if raw_index == 0:
        if col_index == 0:
            list_indexes_to_check.append((raw_index + 1, col_index))
            list_indexes_to_check.append((raw_index + 1, col_index + 1))
            list_indexes_to_check.append((raw_index, col_index + 1))
        elif col_index == len(som_fild[raw_index]) - 1:
            list_indexes_to_check.append((raw_index + 1, col_index))
            list_indexes_to_check.append((raw_index, col_index - 1))
            list_indexes_to_check.append((raw_index + 1, col_index + 1))
        else:
            list_indexes_to_check.append((raw_index + 1, col_index + 1))
            list_indexes_to_check.append((raw_index + 1, col_index))
            list_indexes_to_check.append((raw_index, col_index - 1))
            list_indexes_to_check.append((raw_index, col_index + 1))

    elif raw_index == len(som_fild)-1:
        if col_index == 0:
            list_indexes_to_check.append((raw_index - 1, col_index))
            list_indexes_to_check.append((raw_index - 1, col_index + 1))
            list_indexes_to_check.append((raw_index, col_index + 1))
        elif col_index == len(som_fild[raw_index]) - 1:
            list_indexes_to_check.append((raw_index - 1, col_index))
            list_indexes_to_check.append((raw_index, col_index - 1))
            list_indexes_to_check.append((raw_index - 1, col_index + 1))
        else:
            list_indexes_to_check.append((raw_index - 1, col_index + 1))
            list_indexes_to_check.append((raw_index - 1, col_index))
            list_indexes_to_check.append((raw_index, col_index - 1))
            list_indexes_to_check.append((raw_index, col_index + 1))
    else:
        #mid line
        if len(som_fild[raw_index])>len(som_fild[raw_index-1]) and len(som_fild[raw_index])>len(som_fild[raw_index+1]):
            if col_index == 0:
                list_indexes_to_check.append((raw_index+1,col_index))
                list_indexes_to_check.append((raw_index -1 , col_index))
                list_indexes_to_check.append((raw_index, col_index+1))
            elif col_index == len(som_fild[raw_index])-1:
                list_indexes_to_check.append((raw_index + 1, col_index - 1))
                list_indexes_to_check.append((raw_index - 1, col_index - 1))
                list_indexes_to_check.append((raw_index, col_index - 1))
            else:
                list_indexes_to_check.append((raw_index + 1, col_index - 1))
                list_indexes_to_check.append((raw_index + 1, col_index))
                list_indexes_to_check.append((raw_index - 1, col_index - 1))
                list_indexes_to_check.append((raw_index - 1, col_index ))
                list_indexes_to_check.append((raw_index, col_index - 1))
                list_indexes_to_check.append((raw_index, col_index + 1))

        #upper part
        elif len(som_fild[raw_index])>len(som_fild[raw_index-1]):
            if col_index == 0:
                list_indexes_to_check.append((raw_index + 1,col_index))
                list_indexes_to_check.append((raw_index - 1 , col_index))
                list_indexes_to_check.append((raw_index + 1, col_index+1))
                list_indexes_to_check.append((raw_index, col_index+1))
            elif col_index == len(som_fild[raw_index])-1:
                list_indexes_to_check.append((raw_index + 1, col_index))
                list_indexes_to_check.append((raw_index - 1, col_index - 1))
                list_indexes_to_check.append((raw_index, col_index - 1))
                list_indexes_to_check.append((raw_index + 1, col_index + 1))
            else:
                list_indexes_to_check.append((raw_index + 1, col_index + 1))
                list_indexes_to_check.append((raw_index + 1, col_index))
                list_indexes_to_check.append((raw_index - 1, col_index - 1))
                list_indexes_to_check.append((raw_index - 1, col_index ))
                list_indexes_to_check.append((raw_index, col_index - 1))
                list_indexes_to_check.append((raw_index, col_index + 1))

        #lower part
        else:
            if col_index == 0:
                list_indexes_to_check.append((raw_index + 1,col_index))
                list_indexes_to_check.append((raw_index - 1 , col_index))
                list_indexes_to_check.append((raw_index - 1, col_index+1))
                list_indexes_to_check.append((raw_index, col_index+1))
            elif col_index == len(som_fild[raw_index])-1:
                list_indexes_to_check.append((raw_index + 1, col_index - 1))
                list_indexes_to_check.append((raw_index - 1, col_index))
                list_indexes_to_check.append((raw_index, col_index -1))
                list_indexes_to_check.append((raw_index - 1, col_index + 1))
            else:
                list_indexes_to_check.append((raw_index - 1, col_index + 1))
                list_indexes_to_check.append((raw_index - 1, col_index))
                list_indexes_to_check.append((raw_index + 1, col_index - 1))
                list_indexes_to_check.append((raw_index + 1, col_index))
                list_indexes_to_check.append((raw_index, col_index - 1))
                list_indexes_to_check.append((raw_index, col_index + 1))

    sum_dist = 0
    counter = 0
    for tup in list_indexes_to_check:
        counter = counter + 1
        sum_dist = sum_dist + check_distance(som_fild[raw_index][col_index],som_fild[tup[0]][tup[1]])

    avg_dist_ne = sum_dist/counter

    return avg_dist_ne


#avg dist
def distance_avg_to_all_neb(som_fild):
    som_file_avg_dist = []
    sum_avg = 0
    counter = 0
    for raw_index in range(0,len(som_fild)):
        som_file_avg_dist.append([])
        for col_index in range(0,len(som_fild[raw_index])):
            avg_dist_ne = distance_one_node(som_fild, raw_index, col_index)
            sum_avg = sum_avg + avg_dist_ne
            counter = counter + 1
            som_file_avg_dist[raw_index].append(avg_dist_ne)


    return som_file_avg_dist,sum_avg/counter





#run the SOM algo 15 times and choos the best solution
def run_best_som_algo(file_path, LR, ne_1, ne_2, ne_3):
    i = 0
    is_first_loop = True
    save_best_som = []
    save_best_som_file_avg_dist = []
    save_best_sum_avg_dist_ne = 0
    save_city_and_most_close_index = {}
    while i < 15:
        print("iter: "+str(i))
        som_fild, avg_dist, fleg_arrive_to_end_cond,city_and_most_close_index = run_algo_som(file_path, LR, ne_1, ne_2, ne_3)
        som_file_avg_dist, sum_avg_dist_ne = distance_avg_to_all_neb(som_fild)

        if is_first_loop:
            is_first_loop = False
            save_best_sum_avg_dist_ne = avg_dist
            # using deepcopy for deepcopy
            save_best_som = copy.deepcopy(som_fild)
            save_best_som_file_avg_dist = copy.deepcopy(som_file_avg_dist)
            save_city_and_most_close_index = copy.deepcopy(city_and_most_close_index)

        elif save_best_sum_avg_dist_ne > avg_dist:
            save_best_sum_avg_dist_ne = avg_dist
            save_best_som = copy.deepcopy(som_fild)
            save_best_som_file_avg_dist = copy.deepcopy(som_file_avg_dist)
            save_city_and_most_close_index = copy.deepcopy(city_and_most_close_index)

        i = i+1


    return save_best_som, save_best_som_file_avg_dist,save_city_and_most_close_index


#print the hexohid
def paint(som_fild,print_labels,is_som):
    x_list = []
    y_list = []
    color_list = []

    dict_add_for_start = {0: 2, 1: 1.5, 2: 1, 3: 0.5, 4: 0, 5: 0.5, 6: 1, 7: 1.5, 8: 2}

    for line_index in range(0, len(som_fild)):
        for col_ind in range(0, len(som_fild[line_index])):
            y_list.append(line_index)
            x_list.append(col_ind + dict_add_for_start[line_index])
            if not print_labels:
                color_list.append(som_fild[line_index][col_ind][0])
            elif is_som:
                color_list.append(som_fild[line_index][col_ind][0])
            else:
                color_list.append(som_fild[line_index][col_ind])



    # seed a random number
    np.random.seed(int(datetime.datetime.utcnow().timestamp()))
    # total data points

    if print_labels:
        x_list.append(8)
        y_list.append(8)
        color_list.append(2)
        x_list.append(0)
        y_list.append(0)
        color_list.append(0)


        for x_ind in range(0,len(x_list)):
            plot.text(x_list[x_ind]-0.3, y_list[x_ind],str(color_list[x_ind])[:6],fontsize = 'x-small')

    x_arr = np.array(x_list)
    y_arr = np.array(y_list)
    color_arr = np.array(color_list)

    plot.hexbin(x_arr, y_arr, color_arr , gridsize=8, cmap='bwr')
    plot.title('')
    # It is used to display results in the plot format
    plot.show()



def main():
    args = sys.argv
    file_path = args[1]
    som_fild, save_best_som_file_avg_dist,save_city_and_most_close_index = run_best_som_algo(file_path, LR, ne_1, ne_2, ne_3)

    for city,index in save_city_and_most_close_index.items():
        print("city: " + city + "  --->  index: (" + str(8-index[0]) + " , "+str(index[1])+")" )# real Economic_Cluster: "+str(dict_city_name_to_tupple_eco_and_list[city][0]) + "  --->  predict Economic_Cluster: " + str(som_fild[index[0]][index[1]][0]*10))


    paint(som_fild,False,True)


    som_file_avg_dist, sum_avg_dist_ne = distance_avg_to_all_neb(som_fild)
    paint(som_file_avg_dist,True,False)

    random_som_fild = create_new_som()
    paint(random_som_fild, False, True)

    som_file_avg_dist, sum_avg_dist_ne = distance_avg_to_all_neb(random_som_fild)
    paint(som_file_avg_dist,True,False)


if __name__ == "__main__":
    main()






