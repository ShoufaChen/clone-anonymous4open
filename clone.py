import urllib.request as urllib2
import re
from bs4 import BeautifulSoup
import os
import argparse

# pattern that is contained in the page when a file is too big
too_big_pattern = re.compile('too big to be anonymized')

def parse_args():
    parser = argparse.ArgumentParser(description='Clone from the https://anonymous.4open.science')
    parser.add_argument('--clone-dir', type=str, default='master',
                        help='master loacation')
    parser.add_argument('--target', type=str,
                        help='anonymous link you want to clone')
    return parser.parse_args()


def create_dir(name):
    if not os.path.exists(name):
        os.mkdir(name)

def pull_html(url):
    req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib2.urlopen(req).read()
    except urllib2.URLError as e:
        print(e)
        print(url)
    content = response.decode('utf-8')
    soup = BeautifulSoup(content, "lxml")

    return soup


def pull_trees(url):
    folder_soup = pull_html(url)
    trees = folder_soup.find_all('div', attrs={'class': 'tree'})
    return trees

def pull_blobs(url):
    blobs_soup = pull_html(url)
    blobs = blobs_soup.find_all('div', attrs={'class': 'blob'})
    return blobs

def clone_file(url, download, root_url='https://anonymous.4open.science'):
    blobs = pull_blobs(root_url+url)
    for blob in blobs:
        href = blob.a.get('href')
        split_href = href.split('/')
        file_name = '/'.join([download]+split_href[3:])

        print('Clone...  ', file_name)
        #used for debug
        #print('Clone...  ', file_name, href)

        ### Not support clone markdown files now  and LICENSE
        if split_href[-1].split('.')[-1] == 'md' or split_href[-1] =='LICENSE':
            continue

        blob_soup = pull_html(root_url+href)

		# skipping files that are too big
        if len(blob_soup.body.findAll(text=too_big_pattern)) != 0:
            print(f'WARNING: Skipping {file_name} as it is too big to be anonymized')
            continue

        source_code = blob_soup.find('code')
        with open(file_name, 'w') as f:
            f.write(source_code.get_text())

def clone_dirs(url, folders_url_lis, download, root_url='https://anonymous.4open.science'):
    trees = pull_trees(root_url+url)

    for t in trees:
        href = t.a.get('href')
        split_href = href.split('/')
        #folder_name = split_href[-2]
        folder_name = '/'.join([download]+split_href[3:-1])
        print('Clone...  ', folder_name)
        #print('Clone...   ', folder_name, href)
        create_dir(folder_name)

        folders_url_list.append(href)

    folders_url_list.remove(url)
    return folders_url_list


if __name__ == '__main__':
    args = parse_args()
    assert args.target, '\nPlese specifipy your target URL, \n e.g:    '\
            +'python clone.py --target https://anonymous.4open.science/r/840c8c57-3c32-451e-bf12-0e20be300389/'

    root_url = 'https://anonymous.4open.science'
    target_url = args.target.replace(root_url, '')

    create_dir(args.clone_dir)

    folders_url_list = [target_url]
    clone_file(target_url.replace(root_url, ''), args.clone_dir)
    folders_url_list = clone_dirs(target_url.replace(root_url, ''), folders_url_list, args.clone_dir)

    while len(folders_url_list):
        url = folders_url_list[0]
        clone_file(url, args.clone_dir)
        folders_url_list = clone_dirs(url, folders_url_list, args.clone_dir)

    print('==='*20)
    print('Successfully Clone to: {}'.format(args.clone_dir))
    print('==='*20)
