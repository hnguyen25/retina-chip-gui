"""
@authors Maddy Hays, Huy Nguyen (2022)
Functions for loading data files into form that can be read by GUI
"""''
import numpy as np
import scipy.io
import os
from os.path import dirname, join as pjoin
import numpy as np
import time
import scipy.io as sio

"""
=========================================
DATA LOADING FUNCTIONS FOR NUMPY FILES
=========================================
"""

def loadDataFromFileNpz(path):
    raw_data = np.load(path)
    print(raw_data.keys)
    # TODO: manipulate raw .npz data into a better form
    return raw_data['modified_data']

# For current variable names
path = '/Volumes/Lab/Users/mads/dc1DataVis/debugData'
date_piece = '2022-02-18-1'
datarun = 'data000'

"""
========================================
DATA LOADING FUNCTIONS TO PULL MATLAB FILES FROM A COMPLETE RECORDING IN A FOLDER
=========================================
HOW TO USE
loadingDict = initDataLoading('/Volumes/Lab/Users/mads/dc1DataVis/debugData', '2022-02-18-1', 'data000', 'gmem1'):
dataAll, cntAll, times = processData(loadingDict, dataIdentifierString='gmem1', buffer_num=0)
"""
def initDataLoading(path : str):
    # load and convert all data

    """
    # old method
    fileDir = pjoin(path, date_piece, datarun)

    """
    # original data
    bufDir = os.listdir(path)
    num_of_buf = len(bufDir)
    bramdepth = 65536
    datarun = os.path.basename(path)

    # initialize variables
    dataAll = np.zeros((32, 32, int(bramdepth * num_of_buf / 2)))  # Largest possible value of dataAll, perfect recording, only double cnt
    cntAll = np.zeros((32, 32, int(bramdepth * num_of_buf / 2)))
    times = np.zeros((int(bramdepth * num_of_buf / 2)))

    loadingDict = {
        "path": path,
        "datarun": datarun,
        "bufDir": bufDir,
        "num_of_buf": num_of_buf,
        "bramDepth": bramdepth,
        "dataAll": dataAll,
        "cntAll": cntAll,
        "times": times
    }
    print('num of buf', num_of_buf)
    return loadingDict

def processData(loadingDict, dataIdentifierString='gmem1', buffer_num=0):
    # Idea: plot in order of which buffers have the most 'spikes'

    # initialize variables
    timeTrack = 0
    cntTrack = 0
    print(loadingDict.keys())
    # Process all the Data
    for k in range(buffer_num, loadingDict['num_of_buf']):
        start = time.time()

        # Load Data from this Loop's Buffer
        #file_next = pjoin(path, date_piece, datarun, datarun + '_' + str(k) + '.mat')
        file_next = pjoin(loadingDict['path'], loadingDict['datarun'] + '_' + str(k) + '.mat')
        mat_contents = sio.loadmat(file_next)
        dataRaw = mat_contents[dataIdentifierString][0][:]

        data_real, cnt_real, N = removeMultipleCounts(dataRaw)

        # Determine time estimate and sample counts for the total combined buffers
        # ===============================
        # For the first buffer, we assume the first sample comes in at time 0
        if timeTrack == 0:
            loadingDict['dataAll'][:, :, :N] = data_real[:, :, :N]
            loadingDict['cntAll'][:, :, :N] = cnt_real[:, :, :N]
            endTime = N * 0.05  # 20kHz sampling rate, means time_recording (ms) = num_sam*0.05ms
            new_times = np.linspace(0, endTime, N + 1)
            loadingDict['times'][0:len(new_times)] = new_times
        # For buffers after the first, we place these values directly after the previous buffer
        # (note this does not take into account communication delays - hence an estimate)
        elif timeTrack != 0:
            loadingDict['dataAll'][:, :, cntTrack:cntTrack + N] = data_real[:, :, :N]
            loadingDict['cntAll'][:, :, cntTrack:cntTrack + N] = cnt_real[:, :, :N]
            endTime = N * 0.05
            new_times = np.linspace(timeTrack, timeTrack + endTime, N)
            loadingDict['times'][cntTrack:cntTrack + N] = new_times

        # Update for the next buffer file
        timeTrack += endTime
        cntTrack += N

        end = time.time()
        text1 = 'Estimated Time Remaining: ' + str.format('{0:.2f}', (end - start) * (loadingDict['num_of_buf'] - k) / 60) + ' min'
        text2 = file_next
        print(text1 + ' ' + text2, end="\r")

    # Truncate dataAll, cntAll, and times to remove the 0's representing lost data potential due to triple counts
    loadingDict['dataAll'] = loadingDict['dataAll'][:, :, :cntTrack - 1]
    loadingDict['cntAll'] = loadingDict['cntAll'][:, :, :cntTrack - 1]
    loadingDict['times'] = loadingDict['times'][:cntTrack - 1]

    return loadingDict['dataAll'], loadingDict['cntAll'], loadingDict['times']

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

