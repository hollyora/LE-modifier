import json

class DataModifier():

    _check_dict = {
        'savedQuests': 'questID',
        'sceneProgresses': 'scene',
        'unlockedWaypointScenes': 'replace',
        'timelineCompletion': 'timelineID',
        'timelineDifficultyUnlocks': 'timelineID'
    }

    _insert_file_path = './insert_data.json'

    @classmethod
    def get_insert_data(cls):
        with open(cls._insert_file_path, 'r') as new_file:
            return json.load(new_file)
    
    @classmethod
    def get_raw_char_data(cls, file_path:str):
        raw_char_data = {}
        with open(file_path, 'r') as new_data_file:
            raw_char_data = json.loads(new_data_file.read()[5:])
        return raw_char_data

    def __init__(self, file_path:str):
        self.file_path = file_path
        self.char_data = self.get_raw_char_data(file_path)
        self.new_data = self.get_insert_data()

    def insert_data(self):
        keys = list(self.new_data.keys())
        #根據每個key檢查並加入insert_data裡面的資料
        for key in keys:
            # 角色資料
            origin_data = self.char_data[key].copy()
            # print(origin_data)
            # 插入的資料
            self.new_data[key]
            # 需要檢查的key
            id_key = self._check_dict[key]
            new_data_list = []
            for item in self.new_data[key]:
                for old_data in origin_data:
                    # 檢查插入資料裡面是否有存在於角色資料的資料集
                    # 如果有就取代沒有就加入
                    # print(old_data)
                    # print(item)
                    if id_key not in old_data:
                        continue
                    if old_data[id_key] == item[id_key]:
                        #print(old_data,item)
                        # print(old_data)
                        # print(self.char_data[key])
                        # print(self.char_data[key].index(old_data))
                        if old_data in self.char_data[key]:
                            self.char_data[key].pop(self.char_data[key].index(old_data))
                new_data_list.append(item)
                # print(new_data_list)
            self.char_data[key] = new_data_list
    
    def modify_file(self):
        self.char_data['level'] = 100
        self.insert_data()
    
    def save_file(self):
        with open(self.file_path, 'w') as new_data_file:
            new_data_file.write(f"EPOCH{json.dumps(self.char_data)}")

if __name__ == '__main__':
    file_path = input()
    data_checker= DataModifier(file_path)
    data_checker.modify_file()
    data_checker.save_file()