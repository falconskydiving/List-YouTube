import os
import pickle

def mkDirFiles():
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists("export"):
        os.mkdir("export")
    if not os.path.exists("data/data_01"):
        writeFile = open('data/data_01', 'wb')
        default_setting_values = [['main_suggest_keyword_cnt', 5], ['suggest_keyword_cnt_1', 5], ['suggest_keyword_cnt_2', 5], ['alphabet_keyword_cnt', 5], ['video_acquire_cnt', 5]]
        pickle.dump(default_setting_values, writeFile)
        writeFile.close()
    if not os.path.exists("data/data_02"):
        writeFile = open('data/data_02', 'wb')
        empty_values = []
        pickle.dump(empty_values, writeFile)
        writeFile.close()    
    if not os.path.exists("data/data_03"):
        writeFile = open('data/data_03', 'wb')
        default_setting_values = [[0, 0], [0, 0], [0, 0], [0, 0]]
        pickle.dump(default_setting_values, writeFile)
        writeFile.close()
    if not os.path.exists("data/data_04"):
        writeFile = open('data/data_04', 'wb')
        default_setting_values = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        pickle.dump(default_setting_values, writeFile)
        writeFile.close()
    if not os.path.exists("data/data_05"):
        writeFile = open('data/data_05', 'wb')
        default_regular_gate_values = ["まとめ", "", "再生リスト", "一覧", "プレイリスト", "お気に入り"]
        pickle.dump(default_regular_gate_values, writeFile)
        writeFile.close()
    if not os.path.exists("data/data_06"):
        writeFile = open('data/data_06', 'wb')
        default_setting_values = []
        pickle.dump(default_setting_values, writeFile)
        writeFile.close()
    if not os.path.exists("data/data_07"):
        writeFile = open('data/data_07', 'wb')
        default_setting_values = [0]
        pickle.dump(default_setting_values, writeFile)
        writeFile.close()