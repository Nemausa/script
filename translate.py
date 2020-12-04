import time
import os
import re
from concurrent.futures import ThreadPoolExecutor,  as_completed
from google_trans_new import google_translator


li = []
dic = {}

pool = ThreadPoolExecutor(128)
translator = google_translator()

def mkdir(path):
    folder = os.path.exists(path)
    if folder:
        pass
    else:
        os.makedirs(path)   


def read():
    filename = 'strings.xml'
    with open(filename, 'r') as f:
        lines = f.readlines()
        get(lines)
    translate_all()

def write(input, output):
    mkdir('output')
    with open(input, 'r') as f:
        lines = f.readlines()
        with open('output/'+output, 'w') as w:
            replace_lines = replace(lines)
            w.writelines(replace_lines)
            

def replace(lines):
    pat = re.compile(r'.*>(.*)<.*')
    replace_lines = []
    for line in lines:
        m = pat.match(line)
        if m is not None:
            line = line.replace(m.group(1), dic[m.group(1)])
        else:
            pass
        replace_lines.append(line)
    return replace_lines

                 

def get(lines):
    pat = re.compile(r'.*>(.*)<.*')
    for line in lines:
        m = pat.match(line)
        if m is not None:
            li.append(m.group(1))

def translate(word):
    translate_text = translator.translate(word, lang_tgt='zh')
    dic[word] = translate_text
    return translate_text

def translate_all():
    all_task = [pool.submit(translate, (word)) for word in li]
    for future in as_completed(all_task):
        pass
        
    
    

def run():
    time_start = time.time()

    read()
    write('strings.xml', 'strings.xml')

    time_end = time.time()
    print('time cost', time_end-time_start, 's')
    

run()
