import requests
import re
from bs4 import BeautifulSoup
import os
from time import strftime

url = 'https://yande.re/post'

def htmlContent(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.content
    except:
        traceback.print_exc()
        return ""

def save_pics(links):
    for i, path in links:
        r = htmlContent(i)
        with open(path, 'wb') as f:
            f.write(r)

def parse_per_page(url, dirpath, num):
    soup = BeautifulSoup(htmlContent(url), 'html.parser')
    a = soup.find_all('a', attrs={'class': 'directlink largeimg'})
    link_list = []
    for i in a:
        link = i.get('href')
        link_list.append((link, dirpath+'/'+str(num)+'.'+link.split('.')[-1]))
        num += 1
    save_pics(link_list)
    return num

def menu_sel():
    print("{:>60}".format("*"*55))
    print("     **{:^51}**".format("Options"))
    print("{:>60}".format("*"*55))
    print("     **{:<18}{:<12}{:>3}**".format("", "1.到上次爬取时首页的首张(慎用)", ""))
    print("     **{:<18}{:<12}{:>19}**".format("", "2.前___页", ""))
    print("     **{:<18}{:<12}{:>18}**".format("", "3.任意页", ""))
    print("     **{:<18}{:<12}{:>19}**".format("", "4.__到__页", ""))
    print("     **{:<18}{:<12}{:>19}**".format("", "5.退出", ""))
    print("{:>60}\n".format("*"*55))
    got = re.match('[1-5]', input("输入选择:"))
    if got:
        return int(got.group())
    return False

def parse_per_page_op1(url, dirpath, num, latest_link):
    soup = BeautifulSoup(htmlContent(url), 'html.parser')
    a = soup.find_all('a', attrs={'class': 'directlink largeimg'})
    link_list = []
    flag = False
    for i in a:
        link = i.get('href')
        if latest_link == link:
            flag = True
            break
        link_list.append((link, dirpath+'/'+str(num)+'.'+link.split('.')[-1]))
        num += 1
    save_pics(link_list)
    return num, flag

def op_1():
    latest_link = log_latest_r()
    if not latest_link:
        print("首次爬取没必要用该功能\n\n")
    else:
        i = 0
        gen = read_gen()
        if gen:
            date = get_date()
            dirpath = gen + '/' + date
            if not os.path.exists(dirpath):
                mk_dir()
            num = log_num_r(dirpath+'/log_num.txt')
            num_s = num
            while True:
                url_in = url + "?page=" + str(i+1)
                num, flag = parse_per_page_op1(url_in, dirpath, num, latest_link)
                if num-num_s:
                    print("\n已下载第"+str(i+1)+"页")
                    if flag:
                        break
                    i += 1
                else:
                    print("\n无新图片可爬取(即首页首张未更新)")
                    break
            print('\n共爬取{}张\n\n'.format(str(num-num_s)))
            log_num_w(dirpath+'/log_num.txt', num)
        else:
            print("根目录不存在\n\n")

def op_2():
    got = re.match('\d', input("\n\n到多少页?   "))
    if got:
        gen = read_gen()
        if gen:
            date = get_date()
            dirpath = gen + '/' + date
            if not os.path.exists(dirpath):
                mk_dir()
            num = log_num_r(dirpath+'/log_num.txt')
            num_s = num
            for i in range(int(got.group())):
                url_in = url + "?page=" + str(i+1)
                num = parse_per_page(url_in, dirpath, num)
                print("已下载第"+str(i+1)+"页")
            print('\n共爬取{}张\n\n'.format(str(num-num_s)))
            log_num_w(dirpath+'/log_num.txt', num)
        else:
            print("根目录不存在\n\n")
    else:
        print("请合法输入\n\n")

def op_3():
    got = re.match('\d', input("\n\n哪页?   "))
    if got:
        gen = read_gen()
        if gen:
            date = get_date()
            dirpath = gen + '/' + date
            if not os.path.exists(dirpath):
                mk_dir()
            num = log_num_r(dirpath+'/log_num.txt')
            num_s = num
            url_in = url + "?page=" + got.group()
            num = parse_per_page(url_in, dirpath, num)
            print("已下载第"+got.group()+"页")
            print('\n共爬取{}张\n\n'.format(str(num-num_s)))
            log_num_w(dirpath+'/log_num.txt', num)
        else:
            print("根目录不存在\n\n")
    else:
        print("请合法输入\n\n")

def op_4():
    got1 = re.match('\d', input("\n\n起始页?   "))
    got2 = re.match('\d', input("\n\n结束页?   "))
    if got1 and got2:
        gen = read_gen()
        if gen:
            date = get_date()
            dirpath = gen + '/' + date
            if not os.path.exists(dirpath):
                mk_dir()
            num = log_num_r(dirpath+'/log_num.txt')
            num_s = num
            for i in range(int(got1.group()), int(got2.group())+1):
                url_in = url + "?page=" + str(i+1)
                num = parse_per_page(url_in, dirpath, num)
                print("已下载第"+str(i+1)+"页")
            print('\n共爬取{}张\n\n'.format(str(num-num_s)))
            log_num_w(dirpath+'/log_num.txt', num)
        else:
            print("根目录不存在\n\n")
    else:
        print("请合法输入\n\n")

############################################################

def get_date():
    return strftime("%Y%m%d")

def read_gen():
    gen = 'gen_dir.txt'
    if os.path.exists(gen):
        with open(gen, 'r') as f:
            f.readline()
            return f.readline()
    return ""

def mk_dir():
    name = get_date()
    gen = read_gen()
    if gen:
        dirpath = gen + '/' + name
        os.mkdir(dirpath)
        log_num_w(dirpath+'/log_num.txt', 0)

def log_num_w(fp, num):
    with open(fp, 'w') as f:
        f.write(str(num))

def log_num_r(fp):
    with open(fp, 'r') as f:
        return int(f.readline())

def log_latest_w(link):
    with open('log_latest.txt', 'w') as f:
        f.write(link)

def log_latest_r():
    with open('log_latest.txt', 'r') as f:
        return f.readline()

############################################################

def main():
    while True:
        op = menu_sel()
        if not op:
            print("请合法输入\n\n")
        else:
            if op == 1:
                op_1()
            elif op == 2:
                op_2()
            elif op == 3:
                op_3()
            elif op == 4:
                op_4()
            else:
                break
            soup = BeautifulSoup(htmlContent(url), 'html.parser')
            latest_link = soup.find('a', attrs={'class': 'directlink largeimg'}).get('href')
            log_latest_w(latest_link)

############################################################

main()
