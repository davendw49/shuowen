import re
import sys
import pydocx
import codecs
import pymysql
import pypandoc
import argparse
from tqdm import tqdm
from bs4 import BeautifulSoup

def p_discriminate(p):
    if str(p).find("img") != -1:
        return (0, "pic")
    else:
        return (1, "book")
    
class tuban():
    '''
    a tuban class represents a tuban's basic structural information including imgs and the number of tuban
    '''
    def __init__(self, input_file, output_file):
        '''
        init the class
        para: input_file: the file need to be rearrange 
        pare: output_file: the file after rearrange
        '''
        self.tuban_html = pydocx.PyDocX.to_html(input_file)
        self.tuban_soup = BeautifulSoup(self.tuban_html, features="lxml")
        self.input = input_file
        self.output = output_file
        self.errors = []
        self.character = {}
        self.ch_dict = {}
        self.p_list = self.tuban_soup.select('p')
    
    def parse(self):
        '''
        parse the file (html form)
        para: self
        '''
        p_list = self.p_list
        flag = 0
        # if the pre_stage = 1 means that the situation is booknum, 0 means the pictures
        pre_stage = 0
        pre_tag = 0
        this_booknum = ""
        this_character = []
        pre_num = ""
        for p in tqdm(p_list):
            if flag%2 == 0:
                this_booknum = ""
            else:
                this_character = []
            if flag%2 == 0:
                stage = p_discriminate(p)[0]
                if stage == 1:
                    if stage != pre_stage:
                        this_booknum = p.text
                        pre_stage = stage
                    else:
                        self.errors.append(("error 1 多重简号或者换行符有误", pre_num, p.text, "flag="+str(flag)))
                        return flag
                else:
                    self.errors.append(("error 2 缺省简号或者字体截图中换行符有误", pre_num, p.text, "flag="+str(flag)))
                    return flag
            else:
                stage = p_discriminate(p)[0]
                if stage == 0:
                    children = p.children
                    tag = 1 # 0: character, 1:image
                    cflag = 0
                    for child in children:
                        # if str(child)
                        if cflag%2 ==0:
                            if str(child).find("img") == -1:
                                tag = 0
                                pre_tag = tag
                                tmp_pair_character = str(child).strip()
                            else:
                                self.errors.append(("error 3 出现连续文字结点", this_booknum, p.text, "flag="+str(flag)))
                                return flag
                        else:
                            if str(child).find("img") != -1:
                                tag = 1
                                if tag != pre_tag:
                                    tmp_pair_image = str(child)
                                else:
                                    self.errors.append(("error 4 出现连续图片", this_booknum, p.text, "flag="+str(flag)))
                                    return flag
                            else:
                                self.errors.append(("error 5 出现连续文字结点", this_booknum, str(child), "flag="+str(flag)))
                                return flag
                
                            if len(tmp_pair_character)!=0 and len(tmp_pair_image)!=0:
                                this_character.append((tmp_pair_character, tmp_pair_image))
                        cflag+=1
                    pre_stage = stage
                else:
                    self.errors.append(("error 6 多重简号或者换行符有误", this_booknum, p.text, "flag=",flag))
                    return flag
                    # flag-=1
            
            if len(this_booknum)!=0 and len(this_character)!=0 and flag%2==1:
                # print(flag, len(this_booknum),len(this_character))
                self.character[this_booknum] = this_character
            pre_num = this_booknum
            flag += 1
    
    def array2dict(self):
        array = self.character
        self.ch_dict = {}
        for k in array.keys():
            for item in array[k]:
                if item[0] not in self.ch_dict.keys():
                    self.ch_dict[item[0]] = []
                    self.ch_dict[item[0]].append((item[1], k))
                else:
                    self.ch_dict[item[0]].append((item[1], k))
                    
    def get_error(self):
        return self.errors
    
    def get_output_html(self):
        f = open(self.output, "w", encoding="utf8")
        for k in self.ch_dict.keys():
            print("<p>"+k+"</p>", file=f)
            print("<p>", end="", file=f)
            for item in self.ch_dict[k]:
                print(item[0], end="", file=f)
                print(item[1], end=",", file=f)
            print("</p>", file=f)
        f.close()
        
    def get_output_docx(self):
        output = pypandoc.convert_file(self.output, 'docx', outputfile="out.docx", extra_args=["-M8GB", "+RTS", "-K4096m", "-RTS"])
        
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--in_path', default="../data/084.docx", help='input file path')
    parser.add_argument('-o', '--out_path', default="res01.html", help='output file path')
    args = parser.parse_args()
    tb = tuban(args.in_path, args.out_path)
    tb.parse()
    tb.array2dict()
    tb.get_output_html()
    tb.get_output_docx()