"""
Huy Nguyen (2022)

Loads and minimally processes raw data obtained from DC1 into a common, standardized format. Saves data into .npz file
format for additional processing.

Note: Each initialized RawDC1DataHandler is intended to only process data from ONE datarun (i.e. one specific directory)
Make multiple handlers if you are loading multiple data runs.

Contains functionality to multithread data loading and profile performance.

(DC1 Data) -> RawDC1DataHandler -> ProcessedDataHandler

TODOs:
    - import all data
    - parallelize data loading
    - handle both realtime and offline loading
"""
class RawDC1DataHandler():

    parent_dir = None

    run_dir = None


    raw_data_container = None
    processed_data_container = None



    def __init__(self, save_dir):
        self.save_dir = save_dir




    # ==================================
    # Real-time and Offline Data Loading
    # ==================================

    def realtimeLoading(self):
        pass

    def offlineLoading(self):
        pass

    # =================================
    # Parallelization
    # =================================



    # =================================
    # DC1 Specific Processing
    # =================================


    # =================================
    # Saving Data to File
    # =================================
