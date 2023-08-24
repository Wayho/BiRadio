# coding=utf-8
import re
PUNC = ' \\\~`!#$%^&*()_+-=|\';":/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《【】吗哈哦噢喔哇呀啪啦呐哪吧喀咯咖咔呿嘎啥额耶么呢噻{}'  #第一个字符空格，第二字符\\\
print('utils v5.8.1:',PUNC)

def lower_delete_all_char(text,char):
    """
    转小写，删除所有字符，比如空格
    用于数据库中歌名回读
    """
    text = text.lower()
    list=text.split(char)
    listnew=[i for i in list if i!='' ]
    return ''.join(listnew)

def lower_delete_punctuation_and_emoj(text):
    """
    转小写，删除删除标点括号、语气词,emoj=[XXX]
    """
    textnew = delete_emoj(text)
    while len(text)!=len(textnew):
        text = textnew
        textnew = delete_emoj(text)
    text = text.lower()
    return delete_punctuation(text)

def delete_emoj(text,char_s='[',char_e=']'):
    """
    删除emoj=[XXX]
    """
    start = text.find(char_s)
    end =  text.find(char_e)
    if -1!=start and -1!=end:
        return text[:start] + text[end+1:]
    return text

def delete_punctuation(text):
    """
    删除标点括号、语气词，除了[]
    """
    return re.sub(r"[%s]+" %PUNC, "",text)
############################################################

if __name__ == '__main__':
    print(lower_delete_all_char_and_emoj('I love u[dog]ad[ff]',' '))
    print(delete_emoj('ad[dog]ad[ff]AD'))
        