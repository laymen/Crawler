# encoding: UTF-8
import sys  
import re  
import codecs  
import os  
import shutil  
import jieba  
import jieba.analyse
  
#导入自定义词典  
#jieba  

#Read file and cut  
def read_file_cut():   
    stopwords = {}.fromkeys([ line.strip() for line in open('E:\\dataMining\\chinese_stopword.txt') ])
    #create path
    #要处理文件的路径
    path = "E:\\dataMining\\data\\"
    #处理完成后写入文件的路径
    respath="E:\\dataMining\\result\\"
    #isdir(s)是否是一个目录
    if os.path.isdir(respath):  #如果respath这个路径存在
        shutil.rmtree(respath, True)  #则递归移除这个路径,os.removedirs(respath) 不能删除非空目录
    os.makedirs(respath)  #重新建立一个respath的多级目录
        
        
    #读出原始文件的个数
    total="%d" % len(os.listdir("E:\\dataMining\\data"))
    #一共有total个txt文件
    print total  
  
    num = 1
    total=int(total)
    while num<=total:
        name = "%d" % num   
        fileName = path + str(name) + ".txt"  
        resName = respath + str(name) + ".txt"  
        source = open(fileName, 'r')  #r表示只读文件
        #if os.path.exists(resName):  
         #   os.remove(resName) #remove(path)表示删除文件 --removedirs(path)表示删除多级目录
        #使用codecs模块提供的方法创建指定编码格式文件
        #open(fname,mode,encoding,errors,buffering)
        result = codecs.open(resName, 'w', 'utf-8')  
        line = source.readline()  #读取一行
        line = line.rstrip('\n')  #除首尾空格 
        while line!="":
            #line = unicode(line, "utf-8") #将unicode转换成utf-8,才能写入到文件中
            output=''
            strr=''
            #断句 还可以接着添加.......
            for i in re.split(u'【|】|-|_',line):
                strr=strr+i+'\t'
            #清洗中文标点符号 还可以接着添加.......
            string = re.sub("[\.\！\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf-8"),"",strr)
            #停用词清洗
            segs = jieba.cut(string,cut_all=False)
            for seg in segs:
                seg=seg.encode('utf-8')
                segs=[seg for seg in segs if seg not in stopwords]
                output = ' '.join(segs)#空格拼接
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
