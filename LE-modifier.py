import json

class DataModifier():
    # 定義需要檢查的字典，用於映射資料欄位名稱和識別鍵
    _check_dict = {
        'savedQuests': 'questID',
        'sceneProgresses': 'scene',
        'unlockedWaypointScenes': 'replace',
        'timelineCompletion': 'timelineID',
        'timelineDifficultyUnlocks': 'timelineID'
    }

    # 設定插入資料檔案的相對路徑
    _insert_file_path = './insert_data.json'

    @classmethod
    def get_insert_data(cls):
        # 讀取插入資料檔案並返回其 JSON 格式內容
        with open(cls._insert_file_path, 'r') as new_file:
            return json.load(new_file)
    
    @classmethod
    def get_raw_char_data(cls, file_path:str):
        # 從指定檔案中讀取角色數據，略過前 5 個字符
        raw_char_data = {}
        with open(file_path, 'r') as new_data_file:
            raw_char_data = json.loads(new_data_file.read()[5:])
        return raw_char_data

    def __init__(self, file_path:str):
        # 初始化時載入角色數據和插入數據
        self.file_path = file_path
        self.char_data = self.get_raw_char_data(file_path)
        self.new_data = self.get_insert_data()

    def insert_data(self):
        keys = list(self.new_data.keys())
        # 依據每個鍵檢查並將插入數據加入到角色數據
        for key in keys:
            # 複製角色數據的原始內容
            origin_data = self.char_data[key].copy()
            # 插入的資料
            self.new_data[key]
            # 識別資料集中需要檢查的鍵
            id_key = self._check_dict[key]
            new_data_list = []
            for item in self.new_data[key]:
                for old_data in origin_data:
                    # 確認插入數據中是否已有角色數據的資料集
                    if id_key not in old_data:
                        continue
                    if old_data[id_key] == item[id_key]:
                        # 如果找到匹配的資料則替換
                        if old_data in self.char_data[key]:
                            self.char_data[key].pop(self.char_data[key].index(old_data))
                # 將插入資料加入新列表
                new_data_list.append(item)
            # 更新角色數據
            self.char_data[key] = new_data_list
    
    def modify_file(self):
        # 修改角色等級並插入數據
        self.char_data['level'] = 100
        self.insert_data()
    
    def save_file(self):
        # 將修改後的數據保存回文件
        with open(self.file_path, 'w') as new_data_file:
            new_data_file.write(f"EPOCH{json.dumps(self.char_data)}")

if __name__ == '__main__':
    # 從使用者輸入中獲取檔案路徑
    file_path = input()
    data_checker= DataModifier(file_path)
    data_checker.modify_file()  # 修改角色數據
    data_checker.save_file()    # 保存修改後的數據
