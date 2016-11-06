# 
3h: 中文
  前处理4：断句
  前处理8：标点清洗
  前处理12：停用词清洗

下面测试过了： 过程步骤是0,1,2,3
------------------------------------------------------------------------------------------ 
http://blog.csdn.net/pipisorry/article/details/25909899   re API文档
http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html
http://www.cnblogs.com/NeilHappy/archive/2012/07/20/2600111.html 易错点 python
-------------------------------------------------------------------------------------------
0.读取文件的处理办法
# encoding: UTF-8
import re
fileBefPro=open('E:\\dataMining\\data.txt')
fileAftPro=open('E:\\dataMining\\after.txt','a') 
iter_f=iter(fileBefPro)
for line in iter_f:#读一行就操作一行
    #在这里进行处理哈
    fileAftPro.write(str(line))
fileAftPro.close()
fileBefPro.close()
-------------------------------------------------------------------------------------------
1.断句
使用的是re中的split
split中使用中文分隔符：https://segmentfault.com/q/1010000002461248
# encoding: UTF-8
import re

str=u"【红豆杉】红豆杉作用与功效_红豆杉抗癌药品-健客网"
re.split(u'【|】|-|_', str)

for i in re.split(u'【|】|-|_',  str):
    print i

-------------------------------------------------------------------------------------------
2，清洗中文标点符号代码：http://blog.csdn.net/mach_learn/article/details/41744487
# encoding: UTF-8
import re
temp = "想要把一大段中文文本中所有的标点符号删除掉，然后分词制作语料库使用，大神们有没有办法呢？或者哪位大神有中文语料库给个链接好不好？我想做新闻的文本相似度分析，提取关键词的时候需要语料库。谢谢大神们~~~~~ "
temp = temp.decode("utf8")
string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),temp)
print string

或使用这个网址提供的3个办法：http://www.itstrike.cn/Question/5860b8a2-6c44-44f4-8726-c5a7603d44cc.html

--------------------------------------------------------------------------------------------
3.停用词清洗：http://blog.sina.com.cn/s/blog_bccfcaf90101ell5.html
http://blog.csdn.net/sanqima/article/details/50965439   在Python里安装Jieba中文分词组件
# encoding: UTF-8
import re
import jieba
#stopword=[line.strip().decode('utf-8') for line in open('E:\\dataMining\\chinese_stopword.txt').readlines()]

stopwords = {}.fromkeys([ line.rstrip() for line in open('E:\\dataMining\\chinese_stopword.txt') ])
segs = jieba.cut('听说你超级喜欢万众掘金小游戏啊啊啊,或者万一你不喜欢我咧', cut_all=False)
final=''
for seg in segs:
    seg=seg.encode('utf-8')
    if seg not in stopwords:
         final+=seg
print final

----------------------------------------------------------------------------------------------
上面我们处理的是单个文件哦
现在的问题：要是我们处理多个文件咧？
https://segmentfault.com/q/1010000005994107

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
    respath="E:\\dataMining\\data_Result\\"
    #isdir(s)是否是一个目录
    if os.path.isdir(respath):  #如果respath这个路径存在
        shutil.rmtree(respath, True)  #则递归移除这个路径
        #os.removedirs(respath) #不能删除非空目录
        os.makedirs(respath)  #重新建立一个respath的多级目录
    else:
        os.makedirs(respath)  #重新建立一个respath的多级目录

  
    num = 1  
    while num<=20:  
        name = "%d" % num   
        fileName = path + str(name) + ".txt"  
        resName = respath + str(name) + ".txt"  
        source = open(fileName, 'r')  #r表示只读文件
        if os.path.exists(resName):  
            os.remove(resName) #remove(path)表示删除文件 --removedirs(path)表示删除多级目录
        #使用codecs模块提供的方法创建指定编码格式文件
        #open(fname,mode,encoding,errors,buffering)
        result = codecs.open(resName, 'w', 'utf-8')  
        line = source.readline()  #读取一行
        line = line.rstrip('\n') #除首尾空格 
          
        while line!="":
            line = unicode(line, "utf-8") #将unicode转换成utf-8,才能写入到文件中
            output=''
            segs = jieba.cut(line,cut_all=False)
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
