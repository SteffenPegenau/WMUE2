
# FUNCTIONS

def paircounter(text):
    """returns the numbers of charpairs in a text from a given string."""


    #get text from file, transform to lowercase
##    text = open(fileurl, 'r').read().lower()

    # split string into list of chars
    wordlist = text.lower().split()
##    charlist = list(text)
##    charnumber = len(charlist)
    


    #count occurrences in dictionary
    #remember lastchar for finding charpairs
    lastchar = ""
    chardict = {}

    for word in wordlist:
        charlist = list(word)
                
        for char in charlist:
            #if pair is not already in dictionary, add it
            if (chardict.get(lastchar+char, -1)) > 0:
                chardict.update({lastchar+char: (chardict.get(lastchar+char)+1)})
            else:
                chardict.setdefault(lastchar+char, 1)
            #else:
                #no charpair. Do nothing and continue through list

            #update lastchar
            lastchar = char
                    
                    
            
            
    # create a sorted list from elements in dictionary
    result = sorted(chardict.items(), key=lambda x: x[1], reverse=True)
##    print("Listenlänge: " + str(len(result)))
    
##    print(result)

    #remove occurences from list, only charpairs, ordered by occurrence
    endlist = []
    for tupel in result:
        endlist.append(tupel[0])

##    print(endlist)
    return endlist   
    

def charpairs(fileurl):
    """returns the numbers of chars in a text from a given file url."""


    #get text from file, transform to lowercase
    text = open(fileurl, 'r').read().lower()

    # split text at spaces
    charlist = text.split()
    charnumber = len(charlist)

##    print((type(charlist)))


    #count occurrences in dictionary
    #remember lastchar for finding charpairs
    #lastchar = ""
    chardict = {}
    for char in charlist:
        
        #transform returns to "\n"
        if char == "\n":
            char = r"\n"

        #go through charpairs and save them to dictionary
        if(chardict.get(char, -1)) > 0:
            chardict.update({char: (chardict.get(char)+1)})
        else:
            chardict.setdefault(char, 1)

        #update lastchar
        #lastchar = char

     
    # create a sorted list from elements in dictionary
    result = sorted(chardict.items(), key=lambda x: x[1], reverse=True)
    #print("Listenlänge: " + str(len(result)))
    
    
    #print(result[:30])


    #append data filename at last position
    result.append(fileurl)
##    print(result)
    return result

def calculateScore(chardict):
    """Vergleicht das dictionary mit den Häufigkeiten der Buchstaben/-paare
        in den verschiedenen Sprachen und berechnet einen Score. Der höchste
        Score gewinnt. """

    #pop last element (fileurl) from list
    filename = chardict.pop(-1)
##    print(filename)

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

    i = 0

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
        i = i + 1

    #append filename at last position
    resultlist.append(filename)
    #print(resultlist)
    return resultlist

def getMaxToString(scorelist):
    """gets a list of tupels with (language, score) and returns a string with
       with the language that has the highest score"""

    print(scorelist)
    scorelist.pop(-1)

    #now get the max score
    maxi = 0.0
    lang = ""
    for tupel in scorelist:
        if tupel[1] > maxi:
            maxi = tupel[1]
            lang = tupel[0]

    return (lang)


#--------------------------------------
#MAIN BODY

import glob
from bs4 import BeautifulSoup

def getLanguage(url):

    

    #get all txts from directory
    filelist = glob.glob('txts/*.txt')

    with open(url) as fp:
        soup = BeautifulSoup(fp, "html.parser")

    pairs = paircounter(soup.get_text())
    scorel = calculateScore(pairs)
    res = getMaxToString(scorel)
    print(res)
    return res

    


getLanguage("foo.html")


