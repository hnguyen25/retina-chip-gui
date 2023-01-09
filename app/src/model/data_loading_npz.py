def load_npz_file(app):
    print('npz! ------')
    data = np.load(app.settings["path"])
    print(data.files)
    for file in data.files:
        print('file:' + file)
        print(data[file])
    modified_data = data['modified_data']
    small_spike_idx = data['small_spike_idx']
    large_spike_idx = data['large_spike_idx']
    print(modified_data)
    print(small_spike_idx)
    print(large_spike_idx)
