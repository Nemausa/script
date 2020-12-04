# coding:utf-8
# author Nemausa
# version : 1.0


import os
import re
import time
from concurrent.futures import ThreadPoolExecutor,  as_completed
from google_trans_new import google_translator

class translate_file:
    '''
    '''
    def __init__(self,lang_tgt) -> None:
        super().__init__()
        self.lang_tgt = lang_tgt
        self.li = []
        self.dic = {}
        self.pool = ThreadPoolExecutor(128)
        self.translator = google_translator()

        self.work()



    def run(self,input):
        time_start = time.time()

        self.read(input)
        self.write(input, input)

        time_end = time.time()
        print('time cost', time_end-time_start, 's')


    def mkdir(self, path):
        filename = os.path.basename(path)
        dir_path = path.replace(filename, '')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def read(self, input):
        with open(input, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            self.get(lines)
        self.translate_all()

    def write(self, input, output):
        self.mkdir('output/' + input)
        
        with open(input, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            with open('output/'+output, 'w', encoding='UTF-8') as w:
                replace_lines = self.replace(lines)
                w.writelines(replace_lines)

    def replace(self, lines):
        pat = re.compile(r'.*>(.*)<.*')
        replace_lines = []
        for line in lines:
            m = pat.match(line)
            if m is not None:
                line = line.replace(m.group(1), self.dic[m.group(1)])
            else:
                pass
            replace_lines.append(line)
        return replace_lines

    def get(self, lines):
        pat = re.compile(r'.*>(.*)<.*')
        for line in lines:
            m = pat.match(line)
            if m is not None:
                self.li.append(m.group(1))

    def translate(self, word):
        translate_text = self.translator.translate(word, self.lang_tgt)
        self.dic[word] = translate_text
        return translate_text

    def translate_all(self):
        all_task = [self.pool.submit(self.translate, (word)) for word in self.li]
        for future in as_completed(all_task):
            pass


    def work(self):
        is_exist = False
        folder = ''
        while not is_exist:
            folder = input('please input the folder include xml file: ')
            is_exist = os.path.exists(folder)


        g = os.walk(folder)
        for path, dir_list, file_list in g:
            for file_name in file_list:
                file = os.path.join(path, file_name)
                self.run(file)


lang = input('which language do you want: ')
translate = translate_file(lang)
