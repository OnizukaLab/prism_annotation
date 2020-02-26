
import os, json, re
import time, requests
from timeout_decorator import timeout, TimeoutError
from bs4 import BeautifulSoup
from collections import defaultdict
from pprint import pprint
import argparse


def make_folder(folder_path):
    try:
        os.mkdir(folder_path + 'article/')
    except:
        print('article folder is already existing')
        print('skipping mkdir process ')
    try:
        os.mkdir(folder_path + 'html/')
    except:
        print('html folder is already existing')
        print('skipping mkdir process ')


def get_annotation(folder_path, infile_name):
    text_name = folder_path + infile_name
    with open(text_name, 'r') as f:
        annotation_data = json.loads(f.read())
    return annotation_data

@timeout(3)
def get_res_code(url):
    response = requests.get(url, verify=False)
    response.encoding = response.apparent_encoding
    if response.encoding == 'Windows-1254':
        response.encoding = 'utf-8'
    return response

def get_response(url):
    time.sleep(1)
    try:
        response = get_res_code(url)
    except TimeoutError:
        response = 'timeout'
    except:
        response = 'error'
    return response


def write_html(response, url, folder_path):
    url = re.sub(r'[./:]', "", url)
    out_path = folder_path + 'html/' + url + '.txt'
    with open(out_path, 'w') as out:
        out.write(response.text)

def saved_html(annotation_data, folder_path):
    url_set = set()
    for i in range(len(annotation_data)):
        url = annotation_data[i]['url']
        if url in url_set:
            continue
        url_set.add(url)
        response = get_response(url)
        if response.status_code != 200:
            print('error. this url is not access')
            print(url)
            continue
        write_html(response, url, folder_path)
        # print(response.text)
        # break

def get_blog_data(bs, file_name):
    blog_data = None
    if 'ameblo' in file_name:
        id_list = ['entryBody']
        for id in id_list:
            blog_data = bs.find(id=id)
            if blog_data is not None:
                blog_data = blog_data.text
                break
    elif 'yahoo' in file_name:
        class_list = ['entryTd']
        for class_str in class_list:
            blog_data = bs.find(class_=class_str)
            if blog_data is not None:
                blog_data = blog_data.text
                break
    elif 'fc2' in file_name:
        class_list = ['entry_body', 'entry_text', 'entry-body', 'mainEntryBody',
                      'ently_text', 'entryText', 'write', 'body']
        for class_str in class_list:
            blog_data = bs.find_all(class_=class_str)
            if blog_data is None or len(blog_data) == 0:
                continue
            if class_str == 'body':
                if len(blog_data) == 2:
                    blog_data = blog_data[1]
                elif len(blog_data) == 3:
                    blog_data = blog_data[1]
                elif len(blog_data) > 3:
                    blog_data = blog_data[2]
                else:
                    blog_data = blog_data[0]
            else:
                if len(blog_data) == 2:
                    blog_data = blog_data[1]
                elif len(blog_data) > 2:
                    blog_data = blog_data[2]
                else:
                    blog_data = blog_data[0]
            blog_data = blog_data.text
            break

    elif 'livedoor' in file_name:
        class_list = ['article-body-inner', 'entry-body', 'main']
        for class_str in class_list:
            blog_data = bs.find_all(class_=class_str)
            if blog_data is None or len(blog_data) == 0:
                continue
            if len(blog_data) == 2:
                blog_data = blog_data[1]
            else:
                blog_data = blog_data[0]
            blog_data = blog_data.text
            break
    elif 'goo' in file_name:
        class_list = ['entry-body-text', 'etBody']
        for class_str in class_list:
            blog_data = bs.find(class_=class_str)
            if blog_data is not None:
                blog_data = blog_data.text
                break
    return blog_data

def check_line(line, file_name):
    flg = 1
    if 'ameblo' in file_name or 'yahoo' in file_name:
        pass
    elif 'fc2' in file_name:
        if 'function(d)' in line:
            flg = 0
        if '#fc2_text_ad' in line:
            flg = 0
    return flg


def change_text(tag_pattern, blog_data, file_name):
    text_data = ''
    tag_pattern.sub("", blog_data)
    for line in blog_data.split('\n'):
        if check_line(line, file_name):
            text_data += line + '\n'
        else:
            break
    return text_data


def shape(text_data):
    text_data = re.split('[\n。！？…：；:;]|・・+', text_data)
    for i in range(len(text_data))[::-1]:
        text_data[i] = text_data[i].strip()
        if 'http' in text_data[i]:
            break
        if text_data[i] == '':
            text_data.pop(i)
    text_data = '\n'.join(text_data)
    return text_data

def extract_textdata(folder_path):
    tag_pattern = re.compile(r"<[^>]*?>|")

    path1 = folder_path + 'html/'
    path1, dirs1, files1 = next(os.walk(path1))

    for file_name in files1:
        file_path = path1 + file_name
        text_path = folder_path + 'article/' + file_name

        with open(file_path, 'r') as f, open(text_path, 'w') as out:
            bs = BeautifulSoup(f.read(), 'html.parser')
            blog_data = get_blog_data(bs, file_name)
            text_data = change_text(tag_pattern, blog_data, file_name)
            shaping_text = shape(text_data)
            out.write(shaping_text)

def get_paragraph(url, folder_path):
    file_name = re.sub(r'[./:]', "", url)
    path_name = '{}article/{}.txt'.format(folder_path, file_name)
    with open(path_name, 'r') as f:
        lines = f.read().strip().split('\n')
    paragraph = defaultdict(str)
    for i in range(len(lines)):
        paragraph[str(i + 1)] = lines[i]
    return paragraph

def reshape_annotation_data(folder_path, annotation_data):
    for i in range(len(annotation_data))[::-1]:
        now_annotation = annotation_data[i]
        url = now_annotation['url']
        try:
            paragraph = get_paragraph(url, folder_path)
        except:
            print('this annotation is not existing. so remove the data.')
            pprint(url)
            annotation_data.pop(i)
            continue
        sentence = paragraph[now_annotation['sentence_idx']]
        start_idx = int(now_annotation['comment']['start_idx']) - 1
        end_idx = int(now_annotation['comment']['end_idx'])
        span = sentence[start_idx:end_idx]

        annotation_data[i]['comment']['span'] = span
        annotation_data[i]['sentence'] = sentence
        annotation_data[i]['paragraph'] = paragraph
    return annotation_data


def write_annotation(annotation_data, out_file, folder_path):
    out_path = folder_path + out_file
    with open(out_path, 'w', encoding='utf8') as out:
        json.dump(annotation_data, out, indent=4, ensure_ascii=False)


def start_proc(folder_path, infile_name, out_file):
    make_folder(folder_path)
    annotation_data = get_annotation(folder_path, infile_name)
    saved_html(annotation_data, folder_path)
    extract_textdata(folder_path)
    annotation_data = reshape_annotation_data(folder_path, annotation_data)
    write_annotation(annotation_data, out_file, folder_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_path', '-f', default='./trial/', type=str,
                        help='Please input folder path.')
    parser.add_argument('--infile_name', '-i', default='trial.json', type=str,
                        help='Please input json file name of input.')
    parser.add_argument('--out_file', '-o', default='annotation.json', type=str,
                        help='Please input json file name of output.')
    args = parser.parse_args()
    start_proc(args.folder_path, args.infile_name, args.out_file)

if __name__ == '__main__':
    main()