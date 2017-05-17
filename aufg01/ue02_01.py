
# FUNCTIONS

#Nachkommastellen
decimals = 4

def charpairs(fileurl):
    """returns the numbers of chars in a text from a given file url."""


    #get text from file, transform to lowercase
    text = open(fileurl, 'r').read().lower()

##    print(fileurl)
##    file = open(fileurl, "r")
##    print(type(file))
##
##    text = file.read()
##    print(text)
##    print(type(text))

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

    # add percantage to char list
##    endlist = list()
##    for char in result[:30]:
##        temp = list(char)
##        temp.append(temp[1]/charnumber)
##        endlist.append(temp)

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
    
    #extract number 1-10 from filename
    filename = scorelist.pop(-1)
    number = filename.split('\\')[1].split('.')[0]
##    print(number)

    #now get the max score
    maxi = 0.0
    lang = ""
    for tupel in scorelist:
        if tupel[1] > maxi:
            maxi = tupel[1]
            lang = tupel[0]

    return (str(number) + " " + lang + "\n")


#--------------------------------------
#MAIN BODY

import glob

#get all txts from directory
filelist = glob.glob('txts/*.txt')

f = open('challenge.txt', 'w')

#write to file
for file in filelist:
    data = charpairs(file)
    scorelist = calculateScore(data)
    string = getMaxToString(scorelist)
    print(string)
    f.write(string)

f.close()
    


    





#Wait for user input to stop program
input("Press <ENTER> to continue")
