import os
import zipfile
import csv
import numpy as np
import re
import matplotlib.pyplot as plt


def find_file(custom_dir, suffix):
    # find all files have the same [suffix] in folder [custom_dir]
    # [custom_dir] can have many sub folders as you like.
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
    # unzip one file each time, [file] must be with complete address.
    # unzip_type, sf means single file, others means a folder.
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


def remove_files(file, remove_type):
    if remove_type == 'sf':
        os.remove(file)
    else:
        for files in file:
            os.remove(files)
    print('Delete all files')
    return 0


def data_plot(data_address, suffix, machine_number, begin_time: int, minutes, features: int):
    """
    unfinished
    you must specifying the [data_address] like E:/..../year(2019)/month(01)/day(01)/
    [suffix] is the type of files like '.csv', not the '.zip' or '.tar' files!
    [begin_time] means the start time of plot graph,
    [days] means that how many days' data you want to plot (Not allow exceed 1w in one graph)
    [features] means the what is plot on Y axis, only support one features every time in this version.
    """
    input_list = find_file(data_address, suffix)
    plot_matrix = np.zeros((minutes[1]-minutes[0] + 10)*60)
    count = 0
    for files in input_list:
        term = re.findall("\d+", files)
        time_label = int(term[0]+term[1]+term[2])
        time_label2 = int(term[4])*60 + int(term[5])
        if time_label < begin_time or time_label2 < minutes[0] or machine_number != term[3]:
            continue
        if time_label2 > minutes[1]:
            break
        # data_matrix = np.loadtxt(files, delimiter=",", skiprows=1)
        # print(type(data_matrix))
        with open(files, 'r') as f:
            data_matrix = csv.reader(f)
            column = [row[features] for row in data_matrix]
            column = ['0' if x == '' else x for x in column]
            length = len(column) - 1
            column = np.array(column)
        plot_matrix[count*length:(1+count)*length] = np.array(column[1:])
        count = count + 1
    print(count)
    # Draw the picture
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title='An Example Axes', ylabel='Y-Axis', xlabel='X-Axis')
    ax.plot(plot_matrix)
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


