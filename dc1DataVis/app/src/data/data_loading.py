"""
@authors Maddy Hays, Huy Nguyen (2022)
Functions for loading data files into form that can be read by GUI
"""''
import os
import numpy as np



# MULTIPROCESS
def load_one_mat_file():

    data_real = None
    cnt_real = None
    N = None
    preprocessed_data, filtered_data = None, None
    electrodeList = None
    
    return {
        "data_real": data_real,
        "cnt_real": cnt_real,
        "N": N,
        "preprocessed_data": preprocessed_data,
        "filtered_data": filtered_data,
        "electrodeList": electrodeList
    }








"""
========================================
DATA LOADING FUNCTIONS TO PULL MATLAB FILES FROM A COMPLETE RECORDING IN A FOLDER
=========================================
HOW TO USE
loadingDict = initDataLoading('/Volumes/Lab/Users/mads/dc1DataVis/debugData', '2022-02-18-1', 'data000', 'gmem1'):
dataAll, cntAll, times = processData(loadingDict, dataIdentifierString='gmem1', buffer_num=0)
"""
def init_data_loading(path : str):
    bufDir = os.listdir(path)
    num_of_buf = len(bufDir)
    bramdepth = 65536

    datarun = os.path.basename(path)
    datapiece = os.path.basename(os.path.dirname(path))

    # initialize variables
    dataAll = np.zeros((32, 32, int(bramdepth * num_of_buf / 2)))  # Largest possible value of dataAll, perfect recording, only double cnt
    cntAll = np.zeros((32, 32, int(bramdepth * num_of_buf / 2)))
    times = np.zeros((int(bramdepth * num_of_buf / 2)))

    loadingDict = {
        "path": path,
        "datarun": datarun,
        "datapiece": datapiece,
        "bufDir": bufDir,
        "num_of_buf": num_of_buf,
        "bramDepth": bramdepth,
        "dataAll": dataAll,
        "cntAll": cntAll,
        "times": times
    }

    return loadingDict





def removeMultipleCounts(dataRaw):
    # Initialize Variables Needed for Each Buffer
    chan_index_pre = 1025  # Check for chan changes, double cnt
    cnt_pre = 0  # Check for cnt changes, double cnt
    N = 0  # Sample times (DOES NOT ALLOW NON-COLLISION FREE SAMPLES)
    data_real = np.zeros(
        (32, 32, len(dataRaw) - 2))  # Initialize to max possible length. Note: Throw out first two values b/c garbo
    cnt_real = np.zeros((32, 32, len(dataRaw) - 2))

    # Convert data and remove double/triple counts
    for i in range(2, len(dataRaw) - 1):
        # Convert bit number into binary
        word = (np.binary_repr(dataRaw[i], 32))

        # Break that binary into it's respective pieces and convert to bit number
        cnt = int(word[12:14], 2)
        col = int(word[27:32], 2)
        row = int(word[22:27], 2)
        chan_index = row * 32 + col

        # Only record the unique non-double count sample
        if (i == 2 or (cnt_pre != cnt or chan_index != chan_index_pre)):

            # Sample time only changes when cnt changes
            if cnt != cnt_pre:
                N += 1
            # On the occurance the first cnt is not 0, make sure sample time is 0
            if i == 2:
                N = 0

            # Update variables
            cnt_pre = cnt
            chan_index_pre = chan_index

            # Record pertinent data
            data_real[row][col][N] = int(word[14:22], 2)
            cnt_real[row][col][N] = cnt

    return data_real, cnt_real, N

