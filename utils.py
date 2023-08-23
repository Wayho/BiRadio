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

def lower_delete_all_char_and_emoj(text,char):
    """
    转小写，删除所有字符,emoj=[XXX]，比如空格
    """
    textnew = delete_emoj(text)
    while len(text)!=len(textnew):
        text = textnew
        textnew = delete_emoj(text)
    text = text.lower()
    list=text.split(char)
    listnew=[i for i in list if i!='' ]
    return ''.join(listnew)

def delete_emoj(text,char_s='[',char_e=']'):
    """
    删除emoj=[XXX]
    """
    start = text.find(char_s)
    end =  text.find(char_e)
    if -1!=start and -1!=end:
        return text[:start] + text[end+1:]
    return text
############################################################

if __name__ == '__main__':
    print(lower_delete_all_char_and_emoj('I love u[dog]ad[ff]',' '))
    print(delete_emoj('ad[dog]ad[ff]AD'))
        