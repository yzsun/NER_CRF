#coding=utf8

import sys
import os
import json



home_dir = os.path.dirname(__file__)



def writeData(file,word,tag,locTag):
    if len(word) > 0 and  word != "。" and word != "，":
        file.write(word + '\t' + tag  + '\t' +locTag +'\n')
    else:
        file.write('\n')

#填充地点标注，非地点的不添加
def get_local_tag(words_tags):
    '''
    :param words_tags: e.g.['上午/t','九时/t','二十分/t', '，/w','李鹏/nr','总理/n',.....]
    :return: locTAG:
    '''
    locTAG=['O']*len(words_tags)
    ix = 0
    while ix<=len(words_tags)-1:
        word_tag = words_tags[ix]
        if '[' not in word_tag and ']' not in word_tag:  # 单个词
            word,tag=word_tag.split('/')
            if tag=="ns":
                locTAG[ix]="LOC_S"
            # print locTAG[ix]
            ix+=1
        else:#发现词组 e.g.[华北/ns 电管局/n]nt
            start=end=ix
            while True: #找到词组(phrase)的结尾
                end+=1
                if ']' in words_tags[end]:break
            ix = end + 1
            phrase = words_tags[start:end+1] #get phrase e.g.["华北/ns", "电管局/n]nt"]
            if phrase[-1].split(']')[-1]=="ns": #如果整个词组标注为ns,则各词分解为LOC_B,LOC_I,...,LOC_E
                locTAG[start],locTAG[end]='LOC_B','LOC_E'
                locTAG[start+1:end]=['LOC_I']*(end-start-1)
            else:#如果整个词组非ns,则分别查看词组中各词,如同单个词
                for i in range(end-start):
                    word, tag = phrase[i].split('/')
                    if tag=='ns': locTAG[start+i]='LOC_S'
            # print  locTAG[ix:end+1]
    return locTAG  #['LOC_S', 'O', 'O', 'O,....]



def main():
    trainData = open(os.path.join(home_dir,'data', 'train.data'), 'w')
    testData = open(os.path.join(home_dir,'data', 'test.data'), 'w')
    with open( os.path.join(home_dir, 'data','people-daily.txt'),'r')  as file: #分词并标注的 语料库
        #line by line
        for row,line in enumerate(file):
            line=line.strip()
            if len(line)==0:continue #空行
            words_tags=line.split()[1:]  #行首为时间,e.g.19980101-01-004-001/m 李鹏/nr 在/p 北京/ns 考察/v 企业/n
            if len(words_tags)==0:continue #仅有时间,内容为空
            locTAG=get_local_tag(words_tags) #type list e.g.['LOC_S', 'O', 'O', 'O,....]

            print line
            print locTAG

            for i,word_tag in enumerate(words_tags):

                #去除词组的特殊格式,e.g. [香港/ns-->香港/ns   行政区/n]ns-->行政区/n
                if word_tag.find('[')>=0:word_tag = word_tag[word_tag.index('[')+1:]  #未find到,return -1
                if word_tag.find(']')>=0: word_tag = word_tag[:word_tag.index(']') ]

                word,tag=word_tag.split('/')

                saveFile = testData if (row+1)%5==0 else trainData
                writeData(saveFile,word,tag,locTAG[i])
            writeData(saveFile, '','','')




if __name__ == '__main__':    
    main()


