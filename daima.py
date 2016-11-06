# encoding: UTF-8
import sys  
import re  
import codecs  
import os  
import shutil  
import jieba  
import jieba.analyse
  
#�����Զ���ʵ�  
#jieba  

#Read file and cut  
def read_file_cut():   
    stopwords = {}.fromkeys([ line.strip() for line in open('E:\\dataMining\\chinese_stopword.txt') ])
    #create path
    #Ҫ�����ļ���·��
    path = "E:\\dataMining\\data\\"
    #������ɺ�д���ļ���·��
    respath="E:\\dataMining\\result\\"
    #isdir(s)�Ƿ���һ��Ŀ¼
    if os.path.isdir(respath):  #���respath���·������
        shutil.rmtree(respath, True)  #��ݹ��Ƴ����·��,os.removedirs(respath) ����ɾ���ǿ�Ŀ¼
    os.makedirs(respath)  #���½���һ��respath�Ķ༶Ŀ¼
        
        
    #����ԭʼ�ļ��ĸ���
    total="%d" % len(os.listdir("E:\\dataMining\\data"))
    #һ����total��txt�ļ�
    print total  
  
    num = 1
    total=int(total)
    while num<=total:
        name = "%d" % num   
        fileName = path + str(name) + ".txt"  
        resName = respath + str(name) + ".txt"  
        source = open(fileName, 'r')  #r��ʾֻ���ļ�
        #if os.path.exists(resName):  
         #   os.remove(resName) #remove(path)��ʾɾ���ļ� --removedirs(path)��ʾɾ���༶Ŀ¼
        #ʹ��codecsģ���ṩ�ķ�������ָ�������ʽ�ļ�
        #open(fname,mode,encoding,errors,buffering)
        result = codecs.open(resName, 'w', 'utf-8')  
        line = source.readline()  #��ȡһ��
        line = line.rstrip('\n')  #����β�ո� 
        while line!="":
            #line = unicode(line, "utf-8") #��unicodeת����utf-8,����д�뵽�ļ���
            output=''
            strr=''
            #�Ͼ� �����Խ������.......
            for i in re.split(u'��|��|-|_',line):
                strr=strr+i+'\t'
            #��ϴ���ı����� �����Խ������.......
            string = re.sub("[\.\��\/_,$%^*(+\"\']+|[+��������������~@#��%����&*����]+".decode("utf-8"),"",strr)
            #ͣ�ô���ϴ
            segs = jieba.cut(string,cut_all=False)
            for seg in segs:
                seg=seg.encode('utf-8')
                segs=[seg for seg in segs if seg not in stopwords]
                output = ' '.join(segs)#�ո�ƴ��
            print output
            result.write(output + '\r\n')
            line = source.readline()  
        else:  
            print 'End file: ' + str(num)  
            source.close()  
            result.close()  
        num = num + 1
    else:
	    print 'End All'  
  
#Run function  
if __name__ == '__main__':  
    read_file_cut()
