import os
import zipfile
import csv
import numpy as np
import re
import datetime
import matplotlib.pyplot as plt


def find_file(custom_dir, suffix):
    # find all files have the same suffix in folder custom_dir
    # custom_dir can have many sub folders as you like.
    file_name = list()
    for root, dirs, files in os.walk(custom_dir,):
        for file in files:
            if file[-len(suffix):] == suffix:
                file_name.append(os.path.join(root, file))
        for what in dirs:
            find_file(what, suffix)
    print('Found', len(file_name), 'files!')
    return file_name


def un_zip(file, output_folder, unzip_type):
    #  unzip one files every time, file must be a complete address.
    # unzip_type, sf means single file, others means a folder
    if unzip_type == 'sf':
        f = zipfile.ZipFile(file, 'r')
        for files in f.namelist():
            f.extract(files, output_folder)
    else:
        for files in file:
            f = zipfile.ZipFile(files, 'r')
            for sub_files in f.namelist():
                f.extract(sub_files, output_folder)
    return 0


def data_plot(data_address, suffix, begin_time, days, features):
    """
    unfinished
    you must specifying the data_address like E:/..../year(2019)/month(01)/day(01)/
    suffix is the files type like '.csv', not the zip or tar files!
    begin_time means the time start of plot graph,
    days mean, how many days' data you want to plot
    features means the what is plot on Y axis, now only support one features every time
    """
    input_list = find_file(data_address, suffix)
    data_matrix = np.zeros()
    plot_matrix = np.zeros(days*24*60*60)
    count = 0
    for files in input_list:
        # F:\gongzuo\泽岐深度学习\2018\01\01\TB001-00  00.csv
        term = re.findall("\d+", files)
        time_label = int(term[0]+term[1]+term[2])
        if time_label < begin_time:
            continue
        if count > days:
            break
        data_matrix = np.loadtxt(files, delimiter=",", skiprows=1)
        length = data_matrix.shape[0]
        plot_matrix[count*length:(1+count)*length] = data_matrix[:, features]
        count = count + 1

    # Draw the picture
    fig = plt.figure()

    plt.show()
    return 0


def data_input(data_dir, suffix, time_beg, time_end, step):
    # data_input(20190101, 20200101, second/min/year)
    """
    unfinished
    """
    input_list = find_file(data_dir, suffix)
    if suffix == '.tar' or '.zip':
        for zip_file in input_list:
            un_zip(zip_file, data_dir, 1)
        new_suffix = '.csv'
        print('unzip all the files!')
        input_list = find_file(data_dir, new_suffix)
    train_data = np.zeros([1, 2])
    test_data = np.zeros([1, 2])

    for files in input_list:
        f = csv.reader(open(files, 'r'))
        for user in f:
            print(user[1])
        break
    return train_data, test_data


