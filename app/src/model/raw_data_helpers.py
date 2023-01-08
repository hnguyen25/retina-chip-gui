import numpy as np

def removeMultipleCounts(dataRaw):
    """

    Args:
        dataRaw:

    Returns:

    """
    # Initialize Variables Needed for Each Buffer
    chan_index_pre = 1025  # Check for chan changes, double cnt
    cnt_pre = 0  # Check for cnt changes, double cnt
    N = 0  # Sample times (DOES NOT ALLOW NON-COLLISION FREE SAMPLES)
    data_real = np.zeros(
        (32, 32, len(dataRaw) - 2))  # Initialize to max possible length. Note: Throw out first two values b/c garbo
    cnt_real = np.zeros((32, 32, len(dataRaw) - 2))

    # Convert model and remove double/triple counts
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

            # Record pertinent model
            data_real[row][col][N] = int(word[14:22], 2)
            cnt_real[row][col][N] = cnt

    return data_real, cnt_real, N

def identify_relevant_channels(raw_data: np.array):
    """ Only n number of channels can be recorded at a given time due to bandwidth concerns--the rest are shut off.
    For given model recorded at during a certain window, find which channels were recorded.

    Args:
        raw_data_all: unprocessed model in a given time window (num_channels_X x num_channels_Y x time_len)

    Returns:
        num_channels: number of channels that were found to have been recorded for given model
        channel_map: list of channels that were recorded, i.e. nonzero (x/y_coords, num_channels)
        channel_id: list of channels that were recorded, but identified by a single numerical ID
        start_idx:

    @param raw_data: all the raw model loaded thus far from files
    """
    # This bit takes the longest. ~ 30 sec for whole array 4 channel recording
    num_samples = np.count_nonzero(raw_data, axis=2)
    num_channels = np.count_nonzero(num_samples)

    # Map and Identify recorded channels
    find_coords = np.nonzero(num_samples)
    channel_map = np.array(find_coords)
    channel_id = np.zeros(num_channels)
    start_idx = np.zeros(num_channels)

    from src.model.data_loading import map2idx
    for k in range(0,num_channels):
        channel_id[k] = map2idx(channel_map[0,k],channel_map[1,k])
        start_idx[k] = (raw_data[channel_map[0, k], channel_map[1, k], :] != 0).argmax(axis=0)

    recorded_channels = np.stack((channel_id, start_idx), axis=1).astype(int)

    #return recorded_channels
    return num_channels, channel_map, channel_id, start_idx, find_coords, recorded_channels