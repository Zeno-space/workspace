import os, json
from core.logger import debug_log


class JsonDb(object):
    def __init__(self, path, unique=[]):
        self.db_path = path
        self.unique = unique

        self.id_index = []
        self._unique_tmp = {}
        self._data = {}

        self.load_db()

    def _update_index(self):
        data = self._data
        unique = self.unique

        self.id_index = list(data.keys())

        if unique:
            for col in unique:
                #建立需要列值唯一的列索引
                col_index = []
                for id in data:
                    col_index.append(data[id][col])
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
        id_index = self.id_index

        #生成新id
        if not id_index:
            id = '1'
        else:
            id = str(int(max(id_index)) + 1)

        for col in unique_tmp:
            if record.get(col) and record[col] in unique_tmp[col]:
                debug_log.error('%s内的“%s”已存在' % (record, record[col]))
                return None

        data[id] = record
        debug_log.debug(record)
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
        result = {}
        if data.get(record_id):
            result[record_id] = {}
            if not colunms:
                colunms = data[record_id].keys()
            for col in colunms:
                if data[record_id].get(col) is not None:
                    result[record_id][col] = data[record_id][col]
                else:
                    debug_log.error('请求的列“%s”不存在' % col)
        else:
            debug_log.error('ID:%s不存在' % record_id)
        return result

    def where(self, condition, operator='='):
        """返回符合条件的id集合，id_set
        """
        data = self._data
        id_index = self.id_index

        def compare(value_s, value_t, op=operator):
            """比较传入参数value_s，value_t，是否符合op关系（大小，等于，like等）
            """
            if op in ['=', '>', '<', '>=', '<=']:
                op = '==' if op == '=' else op
                if isinstance(value_t, str) and isinstance(value_s, str):
                    eval_str = '\'%s\'' % value_s + op + '\'%s\'' % value_t
                else:
                    eval_str = str(value_s) + op + str(value_t)
                return True if eval(eval_str) else False
            elif op == 'like':
                return True if value_s in value_t else False

        if condition:
            id_set = set()
            for id in data:
                key, source = condition
                targe = data[id][key] if key != 'id' else id
                if compare(source, targe):
                    id_set.add(id)
        else:
            id_set = set(id_index)  #没有条件，则返回全部ID

        return id_set

    def find(self, condition_dict):
        """找出符合condition_dict中所有条件数据的其中一个。

        如果条件中包含唯一列，则结果必唯一。
        """
        from functools import reduce
        data = self._data

        id_set_list = []
        for key in condition_dict:
            id_set_list.append(self.where((key, condition_dict[key])))
        id_list = list(reduce(lambda x,y:x&y, id_set_list))

        return data[id_list[0]] if id_list else {}
