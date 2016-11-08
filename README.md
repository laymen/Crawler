# 3h 数据清洗
## 1.读取文件的处理办法
encoding: UTF-8
import re
fileBefPro=open('E:\\dataMining\\data.txt')
fileAftPro=open('E:\\dataMining\\after.txt','a') 
iter_f=iter(fileBefPro)
for line in iter_f:#读一行就操作一行
    #在这里进行处理哈
    fileAftPro.write(str(line))
fileAftPro.close()
fileBefPro.close()
## 2.断句 
使用的是re中的split
根据标点符号进行断句，使用到了 [split中使用中文分隔符](https://segmentfault.com/q/1010000002461248)
## 3.标点符号清洗
就是指将文中的标点符号都清洗掉清洗 [清洗中文标点符号代码](http://blog.csdn.net/mach_learn/article/details/41744487)
## 4.停用词清洗
第一步在 在Python里安装Jieba中文分词组件 [安装办法点我](http://blog.csdn.net/sanqima/article/details/50965439)
[清洗办法参考博客](http://blog.sina.com.cn/s/blog_bccfcaf90101ell5.html)
## 5.处理多个文件
encoding: UTF-8
import sys  
import re  
import codecs  
import os  
import shutil  
import jieba  
import jieba.analyse
导入自定义词典  
jieba  

Read file and cut  
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
        while line != "":
            line = unicode(line, "utf-8")  # 将unicode转换成utf-8,才能写入到文件中
            #清洗标点符号
            str_cleaned = re.sub("[\.\！\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf-8"), "", line)

            #用jieba进行分词
            output = ''
            segs = jieba.cut(str_cleaned, cut_all=False)
            for seg in segs:
                seg = seg.encode('utf-8')
                if seg not in stopwords:
                    output += seg
            print output
            output += '\r\n'
            result.write(output.decode('utf8'))
            line = source.readline()
        else:
            print 'End file: ' + str(num)
            source.close()
            result.close()
        num += 1
     else:
        print 'End All'

## Run function
if __name__ == '__main__':
    read_file_cut()

# 3h 新浪微博模拟登录
见我csdn博客  [新浪微博模拟登录](http://blog.csdn.net/u010343650/article/details/52945630)
