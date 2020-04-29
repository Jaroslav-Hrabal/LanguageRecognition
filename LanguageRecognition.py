import numpy as np
import re
import string
import math
import preparation as prep
import table as tb
import fasttext

def readFromFile(file_path):
    f=open(file_path, "r", encoding="utf8")
    if f.mode == 'r':
        contents =f.read()
        return contents
    return ""

def trainData(data):
    #remove diacritics and special symbols
    text = prep.stripText(data)
    
    # make 3D table of trigrams from the text
    table = tb.countTrigrams(data)
    
    # smooth table
    table = tb.smoothTable(table)
    return table    

def testData(text, table1, table2):
    lm1 = tb.calculateLM(text,table1)
    lm2 = tb.calculateLM(text,table2)
    if lm1>lm2:
        return 1
    if lm2>lm1:
        return 2
    if lm1==lm2:
        return 1.5
    else:
        return 0

def testText(text1, table1, table2, expected):
    print("Testing text:")
    print("expected result = ")
    print(expected)
    print("given result : ")
    result = testData(text1,table1,table2)
    print(result)
    if result==expected:
       print("Test successful")
       return 1
    elif result == 0:
        print("Error")
        return 0
    else:
        print("Test failed")
        return 0


def prepareText(data):
    text = prep.stripText(data)
    return text

def prepareSimpleText(data):
    text = prep.stripText(data)
    text = prep.stripDia(data)
    return text

def testFastText(predictions,cond):
    if predictions[0] == cond:
        print("Test successful")
        return 1
    else:
        print("Test failed")
        return 0
    

if __name__ == '__main__':
    
    #load text
    dataset1 = readFromFile("./sampledata1.txt")
    dataset2 = readFromFile("./sampledata2.txt")
    
    #train data - receive a probability table
    table1 = trainData(dataset1)
    table2 = trainData(dataset2)
    tableD1 = trainData(prepareSimpleText(dataset1))
    tableD2 = trainData(prepareSimpleText(dataset2))
    
    #preparing testing data
    text1 = prepareText("a toto je první přiklad na testováni")
    text2 = prepareText("Druhý příklad textu pro rozpoznání jazyka který je napsaný v češtině. A obsahuje několik vět. Jako například tato poslední")
    text3 = prepareText("Pôvod mena Dúbravka je založený na povestiach. Jedna hovorí, že meno dostala podľa veľkých dubových lesov, ktoré tu kedysi boli. Iná hovorí o tom, že chorvátska princezná Dúbravka, ktorá utekala pred Turkami, tu bola zajatá. Tretia je o tom, že drevorubači, ktorí rúbali v lese drevo, mali so sebou psov. Tí sa po lese naháňali. Jeden z nich sa schoval do bútľavého stromu a odtiaľ štekal. Drevorubači si medzi sebou hovorili, že dub hafká. Z toho vznikol názov Dúbravka.")
    text4 = prepareText("Po rekonštrukcii starého súboru obchodov vznikol Obchodný dom Saratov, v ktorom je viac ako 30 prevádzok a okrem iného aj potraviny Billa, predajňa elektrospotrebičov, drogéria, pošta, lekárne, módne butiky, papiernictvo, kvetinárstvo, kaviareň a stánok s domácou a zahraničnou tlačou.")
    text5 = prepareText(readFromFile("./sampledata5.txt"))
    text6 = prepareText(readFromFile("./sampledata6.txt"))
    text7 = prepareText(readFromFile("./sampledata7.txt"))
    text8 = prepareText(readFromFile("./sampledata8.txt"))
    text9 = prepareText(readFromFile("./sampledata9.txt"))
    
    textD1 = prepareSimpleText(text1)
    textD2 = prepareSimpleText(text2)
    textD3 = prepareSimpleText(text3)
    textD4 = prepareSimpleText(text4)
    textD5 = prepareSimpleText(text5)
    textD6 = prepareSimpleText(text6)
    textD7 = prepareSimpleText(text7)
    textD8 = prepareSimpleText(text8)
    textD9 = prepareSimpleText(text9)
    
    #testing data with diacritics
    successRate = 0
    count = 0        
    print("Testing texts with diacritics:")
    successRate += testText(text1,table1,table2,1)
    count+=1
    successRate += testText(text2,table1,table2,1)
    count+=1
    successRate += testText(text3,table1,table2,2)
    count+=1
    successRate += testText(text4,table1,table2,2)
    count+=1
    successRate += testText(text5,table1,table2,1)
    count+=1
    successRate += testText(text6,table1,table2,1)
    count+=1
    successRate += testText(text7,table1,table2,2)
    count+=1
    successRate += testText(text8,table1,table2,2)
    count+=1
    successRate += testText(text9,table1,table2,2)
    count+=1
    print("Success rate in %: ")
    print(100*successRate/count)
    print()
    print()

    #testing data without diacritics
    successRate = 0
    count = 0        
    print("Testing texts without diacritics:")
    successRate += testText(textD1,tableD1,tableD2,1)
    count+=1
    successRate += testText(textD2,tableD1,tableD2,1)
    count+=1
    successRate += testText(textD3,tableD1,tableD2,2)
    count+=1
    successRate += testText(textD4,tableD1,tableD2,2)
    count+=1
    successRate += testText(textD5,tableD1,tableD2,1)
    count+=1
    successRate += testText(textD6,tableD1,tableD2,1)
    count+=1
    successRate += testText(textD7,tableD1,tableD2,2)
    count+=1
    successRate += testText(textD8,tableD1,tableD2,2)
    count+=1
    successRate += testText(textD9,tableD1,tableD2,2)
    count+=1
    print("Success rate in %: ")
    print(100*successRate/count)
    print()
    print()

    #testing text with fasttext for comparison
    PRETRAINED_MODEL_PATH = './lid.176.bin'
    model = fasttext.load_model(PRETRAINED_MODEL_PATH)

    successRate = 0
    count = 0 
    check = ['',('__label__cs',),('__label__sk',)]
    sentences = text1
    predictions = model.predict(sentences)
    print("testing CZ text: ")
    print(predictions)
    successRate += testFastText(predictions, check[1])
    count+=1


    sentences = text2
    predictions = model.predict(sentences)
    print("testing CZ text: ")
    print(predictions)
    successRate += testFastText(predictions, check[1])
    count+=1


    sentences = text3
    predictions = model.predict(sentences)
    print("testing Sk text: ")
    print(predictions)
    successRate += testFastText(predictions, check[2])
    count+=1



    sentences = text4
    predictions = model.predict(sentences)
    print("testing SK text: ")
    print(predictions)
    successRate += testFastText(predictions, check[2])
    count+=1



    sentences = text5
    predictions = model.predict(sentences)
    print("testing CZ text: ")
    print(predictions)
    successRate += testFastText(predictions, check[1])
    count+=1



    sentences = text6
    predictions = model.predict(sentences)
    print("testing CZ text: ")
    print(predictions)
    successRate += testFastText(predictions, check[1])
    count+=1



    sentences = text7
    predictions = model.predict(sentences)
    print("testing SK text: ")
    print(predictions)
    successRate += testFastText(predictions, check[2])
    count+=1



    sentences = text8
    predictions = model.predict(sentences)
    print("testing SK text: ")
    print(predictions)
    successRate += testFastText(predictions, check[2])
    count+=1



    sentences = text9
    predictions = model.predict(sentences)
    print("testing SK text: ")
    print(predictions)
    successRate += testFastText(predictions, check[2])
    count+=1



    sentences = textD1
    predictions = model.predict(sentences)
    print("testing CZ text: ")
    print(predictions)
    successRate += testFastText(predictions, check[1])
    count+=1



    sentences = textD2
    predictions = model.predict(sentences)
    print("testing CZ text: ")
    print(predictions)
    successRate += testFastText(predictions, check[1])
    count+=1



    sentences = textD3
    predictions = model.predict(sentences)
    print("testing Sk text: ")
    print(predictions)
    successRate += testFastText(predictions, check[2])
    count+=1



    sentences = textD4
    predictions = model.predict(sentences)
    print("testing SK text: ")
    print(predictions)
    successRate += testFastText(predictions, check[2])
    count+=1



    sentences = textD5
    predictions = model.predict(sentences)
    print("testing CZ text: ")
    print(predictions)
    successRate += testFastText(predictions, check[1])
    count+=1



    sentences = textD6
    predictions = model.predict(sentences)
    print("testing CZ text: ")
    print(predictions)
    successRate += testFastText(predictions, check[1])
    count+=1



    sentences = textD7
    predictions = model.predict(sentences)
    print("testing SK text: ")
    print(predictions)
    successRate += testFastText(predictions, check[2])
    count+=1



    sentences = textD8
    predictions = model.predict(sentences)
    print("testing SK text: ")
    print(predictions)
    successRate += testFastText(predictions, check[2])
    count+=1



    sentences = textD9
    predictions = model.predict(sentences)
    print("testing SK text: ")
    print(predictions)
    successRate += testFastText(predictions, check[2])
    count+=1

    print("Success rate in %: ")
    print(100*successRate/count)
    print()
    print()

