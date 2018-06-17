import os, json
from core.logger import debug_log


class json_db(object):
    def __init__(self, path, unique=[]):
        self.db_path = path
        self.unique = unique

        self._unique_tmp = {}
        self._data = {}
        self.load_db()

    def _update_index(self):
        data = self._data
        unique = self.unique

        if unique:
            for col in unique:
                #建立需要列值唯一的列索引
                col_index = []
                for key in data:
                    col_index.append(data[key][col])
                self._unique_tmp[col] = col_index

    def load_db(self):
        """加载json文件数据
        """
        db_path = self.db_path

        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='UTF-8') as db_file:
                self._data = json.load(db_file)
            self._update_index()
        else:
            self.save_db()

            return True

    def save_db(self):
        """数据保存为json文件
        """
        data, db_path = self._data, self.db_path

        with open(db_path, 'w', encoding='UTF-8') as db_file:
            json.dump(data, db_file, ensure_ascii=False, indent=4)

        self._update_index()
        return True

    def add(self, record):
        """
        return id 
        """
        data = self._data
        unique_tmp = self._unique_tmp

        #生成新id
        if not data:
            id = '1'
        else:
            id = str(int(max(data.keys())) + 1)

        for col in unique_tmp:
            if record.get(col) and record[col] in unique_tmp[col]:
                debug_log.error('%s内的“%s”已存在' % (record, record[col]))
                return None

        data[id] = record
        self.save_db()
        return id

    def delete(self, record_id):
        """
        return id 
        """
        data = self._data

        if data.get(record_id):
            del data[record_id]
            self.save_db()
            return record_id
        else:
            debug_log.error('ID:%s不存在' % record_id)
            return None

    def update(self, record_id, record_sub):
        """
        return id 
        """
        data = self._data

        if data.get(record_id):
            for key in record_sub:
                if data[record_id].get(key):
                    data[record_id][key] = record_sub[key]
                    self.save_db()
                    return record_id
                else:
                    debug_log.error('列“%s”不存在' % key)
        else:
            debug_log.error('ID:%s不存在' % record_id)

        return None

    def select(self, record_id, colunms=[]):
        data = self._data
        print(data)
        if data.get(record_id):
            result = [record_id]
            if not colunms:
                colunms = data[record_id].keys()
            for col in colunms:
                if data[record_id].get(col):
                    result.append(data[record_id][col])
                else:
                    debug_log.error('请求的列“%s”不存在' % col)
        else:
            debug_log.error('ID:%s不存在' % record_id)

        return result
