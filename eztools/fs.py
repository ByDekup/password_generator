import re, json, datetime as dt
from .utils import safe_run, run_once

def file_write(filepath: str, text: str, mode: str):
    try:
        with open(filepath, mode, encoding='utf-8') as f:
            if 'r' in mode: return f.read()
            else: f.write(text)
    except Exception as e: raise e

class Cacher:
    def __init__(self, path: str):
        """path: просто напишите __file__ если это обычный python скрипт"""
        self.path=path
        self.ppt1='"""<'
        self.ppt2='>"""'
        self.pattern=rf'{re.escape(self.ppt1)}(.*?){re.escape(self.ppt2)}'

    def save_cache(self, data: dict):
        data=json.dumps(data, ensure_ascii=False, indent=4)
        before=file_write(self.path, "", 'r')
        res=re.search(self.pattern, before, re.DOTALL)
        char="\n\n"
        new_cache = f'{char}{self.ppt1}{data}{self.ppt2}'
        if res is None: file_write(self.path, before.rstrip()+new_cache, "w"); return None
        else:
            noncache=before[:res.start()].rstrip()
            file_write(self.path, noncache+new_cache, 'w')
            return True

    def load_cache(self, key: str = "*"):
        """:param key: для получения всех данных введите * или не указывайте этот аргумент"""
        data=file_write(self.path, "", 'r')
        res = re.search(self.pattern, data, re.DOTALL)
        if res:
            obj = res.group(1).strip()
            return (json.loads(obj))[key] if not key == "*" else json.loads(obj)
        else: return None

class EZlogger:
    class Branch:
        def __init__(self, name: str):
            self.name = name.upper()

        def create(self, level_name: str):
            lvl_val = EZlogger.Branch(f"{self.name}.{level_name.upper()}")
            setattr(self, level_name.upper(), lvl_val)
            return lvl_val
        
        def __str__(self):
            return self.name
    suc = None
    def __init__(self, filepath):
        self.filepath = filepath
        self._write_logs("Скрипт начал свою работу", "START")

    def _write_logs(self, message, type):
        curdt = dt.date.today()
        curt = dt.datetime.now().strftime("%H:%M:%S")
        with open(self.filepath, "a", encoding="utf-8") as logs:
            logs.write(f'[{curdt} {curt}] [{type}] {message}\n')

    @safe_run()
    def add(self, level: str | Branch, message: str = "default message") -> bool:
        """
        Позволяет написать кастомный лог
        \nparams:\n\tlevel: Тип сообщения (INFO, ERROR, FINISH, START, WARNING, END)
            \n\tmessage: Текст лога
        \nreturns:\n\tВозвращает True если успешно, иначе False
        """
        if level == "END": self._write_logs("Скрипт закончил работу", "END")
        else: self._write_logs(message, level)
    @safe_run()
    def clear(self):
        with open(self.filepath, "w", encoding="utf-8") as logsfc: logsfc.write("")

    def info(self, msg): self.add("INFO", msg)
    def error(self, msg): self.add("ERROR", msg)
    def finish(self, msg): self.add("FINISH", msg)
    def start(self, msg): self.add("START", msg)
    def warning(self, msg): self.add("WARNING", msg)
    @run_once 
    def end(self): self.add("END")
    @safe_run()
    def inner(self):
        """выводит в консоль все логи"""
        with open(self.filepath, 'r', encoding='utf-8') as logs: print(logs.read())