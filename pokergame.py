import string

file = "HH20160905 Betelgeuse II - 5-10 - Play Money No Limit Hold'em.txt"
path = ''#r"/Users/MZ/Library/Application Support/PokerStartsUK/HandHistory/B@TM0N/"
filepath = path+file


text = []

with open(filepath) as inputfile:
    for line in inputfile:
        text.append(line)


#print(len(text[1]))

for i in range(len(text)):
    if 'PokerStars Hand' in text[i]:
        ## hand initiator
        print('Hand: ',text[i][17:30],' at pos:' ,i )
    if 'Seat #' in text[i]:
        print("dealer is seat:" ,text[i][text[i].find('#')+1])
    if ': B@TM0N' in text[i] and 'chips' in text[i]:
        print('B@TM0N seat: ',text[i][text[i].find(': B@TM0N')-1])
        print('B@TM0N has ', int(text[i][text[i].find('(')+1:text[i].find('in chips')]),' chips')
    if ' big blind ' in text[i]:
        print('big blind is: ',text[i][text[i].find('big blind')+9:])





#xes
#No. Players
#MyPosition
#stack size
#pot size
#Hand Dealt
    #rank of hand dealt
#blind size to scale in terms of blinds
#pot size
#pre flop/ post-flop/ post turn/
#sum calls
# sum of raises


#y = (pot won - future in)/