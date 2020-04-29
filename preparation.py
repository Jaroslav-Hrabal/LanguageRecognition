import re
import string
import unicodedata


    
def stripText(text):
    # To remove web links(http or https) from the text
    text = re.sub(r"http\S+", "", text) 
 
    # To remove hashtags (trend) from the text
    text = re.sub(r"#\S+", "", text) 
 
    # To remove user tags from text
    text = re.sub(r"@\S+", "", text) 
 
    # To remove re-tweet "RT"
    text = re.sub(r"RT", "", text) 
 
    # To remove digits 
    text = re.sub(r"\d+", "", text)
 
    # To remove new line character if any
    text = text.replace('\\n','')

    text = text.replace('\n', '').replace('\r', '')
 
    # To remove punctuation marks
    translate_table = dict((ord(char), None) for char in string.punctuation)
    text = text.translate(translate_table)
 
    # To convert text in lower case characters(case is language independent)
    text = text.lower()
    
    return text

def stripDia(text):
     return ''.join(c for c in unicodedata.normalize('NFD', text)
                  if unicodedata.category(c) != 'Mn')
def makeAlphabet():
    alphabet = {chr(i+96):i for i in range(1,27)}
    alphabet[' '] = 0
    alphabet['á'] = 27
    alphabet['č'] = 28
    alphabet['ď'] = 29
    alphabet['é'] = 30
    alphabet['ě'] = 31
    alphabet['í'] = 32
    alphabet['ň'] = 33
    alphabet['ó'] = 34
    alphabet['ř'] = 35
    alphabet['ť'] = 36
    alphabet['ů'] = 37
    alphabet['ú'] = 38
    alphabet['ý'] = 39
    alphabet['ž'] = 40
    alphabet['š'] = 41
    alphabet['<'] = 42
    return alphabet

