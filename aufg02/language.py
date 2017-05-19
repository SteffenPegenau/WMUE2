
# FUNCTIONS

def paircounter(text):
    """returns the numbers of charpairs in a text from a given string."""


##--------------------------------------------------------
##  SINGLE CHARACTERS
    
    #split string into single chars
    charlist = list(text.lower())


    
    chardict = {}
    for char in charlist:
        if(chardict.get(char, -1)) > 0:
            chardict.update({char: (chardict.get(char) + 1)})
        else:
            chardict.setdefault(char, 1)


##--------------------------------------------------------
##    DOUBLE CHARACTERS
##
##    # split string into list of chars
##    wordlist = text.lower().split()
##
##
##    #count occurrences in dictionary
##    #remember lastchar for finding charpairs
##    lastchar = ""
##    chardict = {}
##
##    for word in wordlist:
##        charlist = list(word)
##                
##        for char in charlist:
##            #if pair is not already in dictionary, add it
##            if (chardict.get(lastchar+char, -1)) > 0:
##                chardict.update({lastchar+char: (chardict.get(lastchar+char)+1)})
##            else:
##                chardict.setdefault(lastchar+char, 1)
##            #else:
##                #no charpair. Do nothing and continue through list
##
##            #update lastchar
##            lastchar = char
                    
##--------------------------------------------------------                    
            
            
    # create a sorted list from elements in dictionary
    result = sorted(chardict.items(), key=lambda x: x[1], reverse=True)
##    print("Listenlänge: " + str(len(result)))
    
##    print(result)

    #remove occurences from list, only charpairs, ordered by occurrence
    endlist = []
    for tupel in result:
        endlist.append(tupel[0])

    #print("endlist: " + str(endlist))

        
    #remove all chars not in [a-z] from list
    p = re.compile('[a-z]')     #regular expression
    i = 0                       #counter variable
    iSmallerListlength = True

    while iSmallerListlength:
        char = endlist[i]

        if p.match(char) == None:
            #remove non-matching char from list
            endlist.pop(i)
        else:
            #char matches RE
            i = i + 1

        if i >= len(endlist):
            #end reached, break while loop
            iSmallerListlength = False
    
            
    return endlist   
    


def calculateScore(chardict):
    """Vergleicht das dictionary mit den Häufigkeiten der Buchstaben/-paare
        in den verschiedenen Sprachen und berechnet einen Score. Der höchste
        Score gewinnt. """


    #check if single chars or charpairs
    if len(chardict[0][0]) == 1:
        #single chars, get single char distribution for reference
        filelist = glob.glob("language/uni/*.txt")

    elif len(chardict[0][0]) == 2:
        #charpairs, get charpair distribution for reference
        filelist = glob.glob("language/bi/*.txt")

    else:
        #three or more characters, not supported
        print("Format not supported.")
        return

    #load reference values into lists with tupel form
    #(language, [list])
    reference = []
    for file in filelist:
        language = file.split('\\')[-1].split(".")[0]
##        print(language)
        ref = open(file, "r").read().lower().split()
        reference.append((language, ref))
        
##    print(reference)

    #now compare position of data with reference position and calculate score
    resultlist = []

    # go through languages
    for reftupel in reference:
##        print("------------------ " + reftupel[0] + " below:")
        score = 0.0

        j = 0
        #now go through charpairs in dictionary
        for tupel in chardict:
            
            k = 0
            for pair in reftupel[1]:
                data = tupel[0]
                if data == pair:
                    #compare both positions
                    #break loop if matching pair is found to avoid duplicates
                    diff = abs(j - k)
                    score = score + 1/(diff + 1)
##                    print(data + " " + str(score))

                    break

                k = k + 1

            
            j = j + 1
        resultlist.append((reftupel[0], score))


    #print(resultlist)
    return resultlist

def getMaxToString(scorelist):
    """gets a list of tupels with (language, score) and returns a string with
       with the language that has the highest score"""

    #print(scorelist)
    scorelist.pop(-1)

    #now get the max score
    maxi = 0.0
    lang = ""
    for tupel in scorelist:
        if tupel[1] > maxi:
            maxi = tupel[1]
            lang = tupel[0]

    return (lang)


def getLanguage(url):
    """return a string containing the language of the given html-document"""

    with open(url) as fp:
        soup = BeautifulSoup(fp, "html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out


    pairs = paircounter(soup.get_text())
    scorel = calculateScore(pairs)
    res = getMaxToString(scorel)
    #print(res)
    return res


#--------------------------------------
#MAIN BODY

import glob
from bs4 import BeautifulSoup
import re
import os


filelist = glob.glob('html/*.html' )

german = 0
english = 0
spanish = 0
failed = 0
i = 1

for file in filelist:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(str(i) + "/" + str(len(filelist)))
    
    try:
        string = getLanguage(file)
        
    except Exception as e:
        string = "failed"

    if string == "german":
        german = german + 1
    elif string == "english":
        english = english + 1
    elif string == "spanish":
        spanish  = spanish + 1
    elif string == "failed":
        failed = failed + 1

    i = i + 1
    

print("Results from " + str(len(filelist)) + " files:")
print("German: " + str(german))
print("English: " + str(english))
print("Spanish: " + str(spanish))
print("Failed: " + str(failed))



#Wait for user input to terminate program
input("Press <ENTER> to continue")

