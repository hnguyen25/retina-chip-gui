import scipy.signal as signal
import numpy as np
import time

"""
Contains functions to filter model.

Each filter function is overloaded, with one version
that uses just two inputs (default) and one with multiple more params ("Timed"). 

use:
numChan, chMap, chId, startIdx, findCoors = identifyRelevantChannels(dataAll)
filtData = applyFilterToData (dataAll, numChan, chMap, filtType='modHierlemann')

fastBandpass = filtfilt, passband[250,4000], order = 1 (~8 min)
fasterBandpass = sosfiltfilt, passband[250,4000], order = 1 (~7.5 min)
modHierlemann = filtfilt, FIR, [250,4000], 75 taps (~4 min)
auto = filtfilt, pass[250,4000],stop[5,6000], maxPassLoss = 3, minStopLoss = 30, determines order and cutoff needed to reach this (~50 min)
hObandpass = filtfilt, passband [250,4000], order = 5 (~40 min)
Hierlemann = filtfilt,FIR,[100],75 taps (~4 min)
Litke = filtfilt, [250,2000],order = 2 (~18 min)
highpass = filtfilt, [250], order = 5 (~26 min)
none = no filtering of model (~0 min)
"""


def applyFilterToChannelData(channel_data, filtType='Hierlemann', debug = False):
    """

    Args:
        channel_data:
        filtType:

    Returns:

    """
    dataFilt = np.zeros((np.shape(channel_data)))
    if filtType == 'Hierlemann':
        dataFilt = applyFilterHierlemann(channel_data, dataFilt)
    elif filtType == 'Modified Hierlemann':
        dataFilt = applyFilterModHierlemann(channel_data, dataFilt)
    elif filtType == 'Highpass':
        dataFilt = applyFilterHighpass(channel_data, dataFilt)
    elif filtType == 'H0 Bandpass':
        dataFilt = applyFilterH0bandpass(channel_data, dataFilt)
    elif filtType == 'Auto':
        dataFilt = applyFilterAuto(channel_data, dataFilt)
    elif filtType == 'Fast Bandpass':
        dataFilt = applyFilterFastBandpass(channel_data, dataFilt)
    elif filtType == 'Faster Bandpass':
        dataFilt = applyFilterFasterBandpass(channel_data, dataFilt)
    elif filtType == 'Litke':
        dataFilt = applyFilterLitke(channel_data, dataFilt)
    elif filtType == 'None':
        dataFilt = np.copy(channel_data)
    else:
        dataFilt = np.copy(channel_data)
        print('Filter type "' + str(filtType) +'" not recognized. Options include Hierlemann, highpass, bandpass, Litke or none')
    if debug:
        print("Filter type: " +str(filtType))
    return dataFilt



def applyFilterToAllData(dataAll, numChan, chMap, filtType='Modified Hierlemann', debug = False):
    """

    Args:
        dataAll:
        numChan:
        chMap:
        filtType:

    Returns:

    """
    # Future update: only calculate for channels recorded not all
    dataFilt = np.zeros((np.shape(dataAll)))

    if filtType == 'Hierlemann':
        dataFilt = applyFilterHierlemannTimed(dataAll, dataFilt, numChan, chMap)
    elif filtType == 'Modified Hierlemann':
        dataFilt = applyFilterModHierlemannTimed(dataAll, dataFilt, numChan, chMap)
    elif filtType == 'Highpass':
        dataFilt = applyFilterHighpassTimed(dataAll, dataFilt, numChan, chMap)
    elif filtType == 'H0 Bandpass':
        dataFilt = applyFilterH0bandpassTimed(dataAll, dataFilt, numChan, chMap)
    elif filtType == 'Auto':
        dataFilt = applyFilterAutoTimed(dataAll, dataFilt, numChan, chMap)
    elif filtType == 'Fast Bandpass':
        dataFilt = applyFilterFastBandpassTimed(dataAll, dataFilt, numChan, chMap)
    elif filtType == 'Faster Bandpass':
        dataFilt = applyFilterFasterBandpassTimed(dataAll, dataFilt, numChan, chMap)
    elif filtType == 'Litke':
        dataFilt = applyFilterLitkeTimed(dataAll, dataFilt, numChan, chMap)
    elif filtType == 'None':
        dataFilt = np.copy(dataAll)
    else:
        dataFilt = np.copy(dataAll)
        print('Filter not recognized. Options include Hierlemann, highpass, bandpass, Litke or none')
    if debug:
        print("Filter type: " +str(filtType))
    return dataFilt

def applyFilterHierlemann(channel_data, dataFilt):
    """

    Args:

    Returns:

    """
    BP_LOW_CUTOFF = 100.0
    NUM_TAPS = 75
    TAPS = signal.firwin(NUM_TAPS,
                         [BP_LOW_CUTOFF, ],
                         pass_zero=False,
                         fs=20e3 * 1.0)
    a = 1
    dataFilt= signal.filtfilt(TAPS, [a], channel_data)
    return dataFilt

# Extra params
def applyFilterHierlemannTimed(dataAll, dataFilt, numChan, chMap):
    """

    Args:
        dataAll:
        dataFilt:
        numChan:
        chMap:

    Returns:

    """
    BP_LOW_CUTOFF = 100.0
    NUM_TAPS = 75
    TAPS = signal.firwin(NUM_TAPS,
                         [BP_LOW_CUTOFF, ],
                         pass_zero=False,
                         fs=20e3 * 1.0)
    a = 1
    for k in range(0, numChan):
        start = time.time()
        dataFilt[chMap[0, k], chMap[1, k], :] = signal.filtfilt(TAPS, [a], dataAll[chMap[0, k], chMap[1, k], :])
        end = time.time()
        text1 = 'Estimated Time Remaining: ' + str.format('{0:.2f}', (end - start) * (numChan - k) / 60) + ' min'
        text2 = str(k + 1) + '/' + str(numChan) + ' Channels Filtered'
        print(text1 + ' ' + text2, end="\r")
    return dataFilt

def applyFilterModHierlemann(channel_data, dataFilt):
    """

    Args:
        channel_data:
        dataFilt:

    Returns:

    """
    BP_LOW_CUTOFF = 250.0
    BP_HIGH_CUTOFF = 4000.0
    NUM_TAPS = 100
    TAPS = signal.firwin(NUM_TAPS,
                         [BP_LOW_CUTOFF, BP_HIGH_CUTOFF],
                         pass_zero=False,
                         fs=20e3 * 1.0)
    a = 1
    dataFilt = signal.filtfilt(TAPS, [a], channel_data)
    return dataFilt

# Extra params
def applyFilterModHierlemannTimed(dataAll, dataFilt, numChan, chMap):
    """

    Args:
        dataAll:
        dataFilt:
        numChan:
        chMap:

    Returns:

    """
    BP_LOW_CUTOFF = 250.0
    BP_HIGH_CUTOFF = 4000.0
    NUM_TAPS = 100
    TAPS = signal.firwin(NUM_TAPS,
                         [BP_LOW_CUTOFF, BP_HIGH_CUTOFF],
                         pass_zero=False,
                         fs=20e3 * 1.0)
    a = 1
    for k in range(0, numChan):
        start = time.time()
        dataFilt[chMap[0, k], chMap[1, k], :] = signal.filtfilt(TAPS, [a], dataAll[chMap[0, k], chMap[1, k], :])
        end = time.time()
        text1 = 'Estimated Time Remaining: ' + str.format('{0:.2f}', (end - start) * (numChan - k) / 60) + ' min'
        text2 = str(k + 1) + '/' + str(numChan) + ' Channels Filtered'
        print(text1 + ' ' + text2, end="\r")

    return dataFilt

def applyFilterHighpass(channel_data, dataFilt):
    """

    Args:


    Returns:

    """
    nyq = 0.5 * (20e3 * 1.0)
    cutoff = 250 / nyq
    b, a = signal.butter(5, [cutoff], btype="highpass", analog=False)
    dataFilt = signal.filtfilt(b, a, channel_data)
    return dataFilt

# Extra params
def applyFilterHighpassTimed(dataAll, dataFilt, numChan, chMap):
    """

    Args:
        dataAll:
        dataFilt:
        numChan:
        chMap:

    Returns:

    """
    nyq = 0.5 * (20e3 * 1.0)
    cutoff = 250 / nyq
    b, a = signal.butter(5, [cutoff], btype="highpass", analog=False)
    for k in range(0, numChan):
        start = time.time()
        dataFilt[chMap[0, k], chMap[1, k], :] = signal.filtfilt(b, a, dataAll[chMap[0, k], chMap[1, k], :])
        end = time.time()
        text1 = 'Estimated Time Remaining: ' + str.format('{0:.2f}', (end - start) * (numChan - k) / 60) + ' min'
        text2 = str(k + 1) + '/' + str(numChan) + ' Channels Filtered'
        print(text1 + ' ' + text2, end="\r")
    return dataFilt

def applyFilterH0bandpass(channel_data, dataFilt):
    """

    Args:

    Returns:

    """
    nyq = 0.5 * (20e3 * 1.0)
    cutoff1 = 250 / nyq
    cutoff2 = 4000 / nyq
    b, a = signal.butter(5, [cutoff1, cutoff2], btype="bandpass", analog=False)
    dataFilt = signal.filtfilt(b, a, channel_data)
    return dataFilt

# Extra params
def applyFilterH0bandpassTimed(dataAll, dataFilt, numChan, chMap):
    """

    Args:
        dataAll:
        dataFilt:
        numChan:
        chMap:

    Returns:

    """
    nyq = 0.5 * (20e3 * 1.0)
    cutoff1 = 250 / nyq
    cutoff2 = 4000 / nyq
    b, a = signal.butter(5, [cutoff1, cutoff2], btype="bandpass", analog=False)
    print('Order = ' + str(5))
    for k in range(0, numChan):
        start = time.time()
        dataFilt[chMap[0, k], chMap[1, k], :] = signal.filtfilt(b, a, dataAll[chMap[0, k], chMap[1, k], :])
        end = time.time()
        text1 = 'Estimated Time Remaining: ' + str.format('{0:.2f}', (end - start) * (numChan - k) / 60) + ' min'
        text2 = str(k + 1) + '/' + str(numChan) + ' Channels Filtered'
        print(text1 + ' ' + text2, end="\r")
    return dataFilt


def applyFilterAuto(channel_data, dataFilt):
    """

    Args:

    Returns:

    """
    samFreq = 20e3 * 1.0
    passband = [250, 4000]
    stopband = [5, 6000]
    max_loss_passband = 3
    min_loss_stopband = 30
    order, normal_cutoff = signal.buttord(passband, stopband, max_loss_passband, min_loss_stopband, fs=samFreq)
    b, a = signal.butter(order, normal_cutoff, btype='bandpass', fs=samFreq)
    dataFilt = signal.filtfilt(b, a, channel_data)
    return dataFilt

# Extra params
def applyFilterAutoTimed(dataAll, dataFilt, numChan, chMap):
    """

    Args:
        dataAll:
        dataFilt:
        numChan:
        chMap:

    Returns:

    """
    samFreq = 20e3 * 1.0
    passband = [250, 4000]
    stopband = [5, 6000]
    max_loss_passband = 3
    min_loss_stopband = 30
    order, normal_cutoff = signal.buttord(passband, stopband, max_loss_passband, min_loss_stopband, fs=samFreq)
    b, a = signal.butter(order, normal_cutoff, btype='bandpass', fs=samFreq)
    print('Order = ' + str(order))
    for k in range(0, numChan):
        start = time.time()
        dataFilt[chMap[0, k], chMap[1, k], :] = signal.filtfilt(b, a, dataAll[chMap[0, k], chMap[1, k], :])
        end = time.time()
        text1 = 'Estimated Time Remaining: ' + str.format('{0:.2f}', (end - start) * (numChan - k) / 60) + ' min'
        text2 = str(k + 1) + '/' + str(numChan) + ' Channels Filtered'
        print(text1 + ' ' + text2, end="\r")
    return dataFilt

def applyFilterFastBandpass(channel_data, dataFilt):
    """

    Args:
        dataAll:
        dataFilt:
        numChan:
        chMap:

    Returns:

    """
    nyq = 0.5 * (20e3 * 1.0)
    cutoff1 = 250 / nyq
    cutoff2 = 4000 / nyq
    b, a = signal.butter(1, [cutoff1, cutoff2], btype='bandpass', analog=False)
    dataFilt= signal.filtfilt(b, a, channel_data)
    return dataFilt

# Extra params
def applyFilterFastBandpassTimed(dataAll, dataFilt, numChan, chMap):
    """

    Args:
        dataAll:
        dataFilt:
        numChan:
        chMap:

    Returns:

    """
    nyq = 0.5 * (20e3 * 1.0)
    cutoff1 = 250 / nyq
    cutoff2 = 4000 / nyq
    b, a = signal.butter(1, [cutoff1, cutoff2], btype='bandpass', analog=False)
    print('Order = ' + str(1))
    for k in range(0, numChan):
        start = time.time()
        dataFilt[chMap[0, k], chMap[1, k], :] = signal.filtfilt(b, a, dataAll[chMap[0, k], chMap[1, k], :])
        end = time.time()
        text1 = 'Estimated Time Remaining: ' + str.format('{0:.2f}', (end - start) * (numChan - k) / 60) + ' min'
        text2 = str(k + 1) + '/' + str(numChan) + ' Channels Filtered'
        print(text1 + ' ' + text2, end="\r")
    return dataFilt

def applyFilterFasterBandpass(channel_data, dataFilt):
    """

    Args:


    Returns:

    """
    nyq = 0.5 * (20e3 * 1.0)
    cutoff1 = 250 / nyq
    cutoff2 = 4000 / nyq
    sos1 = signal.butter(1, [cutoff1, cutoff2], btype='bandpass', output='sos')
    dataFilt = signal.sosfiltfilt(sos1, channel_data)
    return dataFilt

# Extra params
def applyFilterFasterBandpassTimed(dataAll, dataFilt, numChan, chMap):
    """

    Args:
        dataAll:
        dataFilt:
        numChan:
        chMap:

    Returns:

    """
    nyq = 0.5 * (20e3 * 1.0)
    cutoff1 = 250 / nyq
    cutoff2 = 4000 / nyq
    sos1 = signal.butter(1, [cutoff1, cutoff2], btype='bandpass', output='sos')
    print('Order = ' + str(1))
    for k in range(0, numChan):
        start = time.time()
        dataFilt[chMap[0, k], chMap[1, k], :] = signal.sosfiltfilt(sos1, dataAll[chMap[0, k], chMap[1, k], :])
        end = time.time()
        text1 = 'Estimated Time Remaining: ' + str.format('{0:.2f}', (end - start) * (numChan - k) / 60) + ' min'
        text2 = str(k + 1) + '/' + str(numChan) + ' Channels Filtered'
        print(text1 + ' ' + text2, end="\r")
    return dataFilt


def applyFilterLitke(channel_data, dataFilt):
    """

    Args:
        dataAll:
        dataFilt:
        numChan:
        chMap:

    Returns:

    """
    nyq = 0.5 * (20e3 * 1.0)
    cutoff1 = 250 / nyq
    cutoff2 = 2000 / nyq
    b, a = signal.butter(2, [cutoff1, cutoff2], btype="bandpass", analog=False)
    dataFilt = signal.filtfilt(b, a, channel_data)
    return dataFilt

# Extra params
def applyFilterLitkeTimed(dataAll, dataFilt, numChan, chMap):
    """

    Args:
        dataAll:
        dataFilt:
        numChan:
        chMap:

    Returns:

    """
    nyq = 0.5 * (20e3 * 1.0)
    cutoff1 = 250 / nyq
    cutoff2 = 2000 / nyq
    b, a = signal.butter(2, [cutoff1, cutoff2], btype="bandpass", analog=False)
    for k in range(0, numChan):
        start = time.time()
        dataFilt[chMap[0, k], chMap[1, k], :] = signal.filtfilt(b, a, dataAll[chMap[0, k], chMap[1, k], :])
        end = time.time()
        text1 = 'Estimated Time Remaining: ' + str.format('{0:.2f}', (end - start) * (numChan - k) / 60) + ' min'
        text2 = str(k + 1) + '/' + str(numChan) + ' Channels Filtered'
        print(text1 + ' ' + text2, end="\r")
    return dataFilt

