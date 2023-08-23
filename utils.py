# coding=utf-8
print('utils v5.8.0:')

def delete_all_char(text,char):
    """
    删除所有字符，比如空格
    """
    list=text.split(char)
    listnew=[i for i in list if i!='' ]
    return ''.join(listnew)

def lower_delete_all_char(text,char):
    """
    转小写，删除所有字符，比如空格
    """
    text = text.lower()
    list=text.split(char)
    listnew=[i for i in list if i!='' ]
    return ''.join(listnew)
############################################################

if __name__ == '__main__':
    delete_all_char('I love u')
        