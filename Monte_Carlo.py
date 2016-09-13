import numpy as np
import csv
import pandas as pd


def calc_score(hand):  # assign a calc_score to the hand so it can be compared with other hands
    card_ranks_original = '23456789TJQKA'
    original_suits = 'CDHS'
    rcounts = {card_ranks_original.find(r): ''.join(hand).count(r) for r, _ in hand}.items()
    score, card_ranks = zip(*sorted((cnt, rank) for rank, cnt in rcounts)[::-1])

    potential_threeofakind = score[0] == 3
    potential_twopair = score == (2, 2, 1, 1, 1)
    potential_pair = score == (2, 1, 1, 1, 1, 1)

    if score[0:2] == (3, 2) or score[0:2] == (3, 3):  # fullhouse (three of a kind and pair, or two three of a kind)
        card_ranks = (card_ranks[0], card_ranks[1])
        score = (3, 2)
    elif score[0:4] == (2, 2, 2, 1):  # special case: convert three pair to two pair
        score = (2, 2, 1)  # as three pair are not worth more than two pair
        sortedCrdRanks = sorted(card_ranks, reverse=True)  # avoid for example 11,8,6,7
        card_ranks = (sortedCrdRanks[0], sortedCrdRanks[1], sortedCrdRanks[2], sortedCrdRanks[3])
    elif score[0] == 4:  # four of a kind
        score = (4,)
        sortedCrdRanks = sorted(card_ranks, reverse=True)  # avoid for example 11,8,9
        card_ranks = (sortedCrdRanks[0], sortedCrdRanks[1])
    elif len(score) >= 5:  # high card, flush, straight and straight flush
        # straight
        if 12 in card_ranks:  # adjust if 5 high straight
            card_ranks += (-1,)
        sortedCrdRanks = sorted(card_ranks, reverse=True)  # sort again as if pairs the first rank matches the pair
        for i in range(len(sortedCrdRanks) - 4):
            straight = sortedCrdRanks[i] - sortedCrdRanks[i + 4] == 4
            if straight:
                card_ranks = (
                    sortedCrdRanks[i], sortedCrdRanks[i + 1], sortedCrdRanks[i + 2], sortedCrdRanks[i + 3],
                    sortedCrdRanks[i + 4])
                break

        # flush
        suits = [s for _, s in hand]
        flush = max(suits.count(s) for s in suits) >= 5
        if flush:
            for flushSuit in original_suits:  # get the suit of the flush
                if suits.count(flushSuit) >= 5:
                    break

            flushHand = [k for k in hand if flushSuit in k]
            rcountsFlush = {card_ranks_original.find(r): ''.join(flushHand).count(r) for r, _ in flushHand}.items()
            score, card_ranks = zip(*sorted((cnt, rank) for rank, cnt in rcountsFlush)[::-1])
            card_ranks = tuple(
                sorted(card_ranks, reverse=True))  # ignore original sorting where pairs had influence

            # check for straight in flush
            if 12 in card_ranks and not -1 in card_ranks:  # adjust if 5 high straight
                card_ranks += (-1,)
            for i in range(len(card_ranks) - 4):
                straight = card_ranks[i] - card_ranks[i + 4] == 4
                if straight:
                    break

        # no pair, straight, flush, or straight flush
        score = ([(1,), (3, 1, 2)], [(3, 1, 3), (5,)])[flush][straight]

    if score == (1,) and potential_threeofakind:
        score = (3, 1)
    elif score == (1,) and potential_twopair:
        score = (2, 2, 1)
    elif score == (1,) and potential_pair:
        score = (2, 1, 1)

    if score[0] == 5:
        hand_type = "StraightFlush"
        # crdRanks=crdRanks[:5] # five card rule makes no difference {:5] would be incorrect
    elif score[0] == 4:
        hand_type = "FoufOfAKind"
        # crdRanks=crdRanks[:2] # already implemented above
    elif score[0:2] == (3, 2):
        hand_type = "FullHouse"
        # crdRanks=crdRanks[:2] # already implmeneted above
    elif score[0:3] == (3, 1, 3):
        hand_type = "Flush"
        card_ranks = card_ranks[:5]
    elif score[0:3] == (3, 1, 2):
        hand_type = "Straight"
        card_ranks = card_ranks[:5]
    elif score[0:2] == (3, 1):
        hand_type = "ThreeOfAKind"
        card_ranks = card_ranks[:3]
    elif score[0:2] == (2, 2):
        hand_type = "TwoPair"
        card_ranks = card_ranks[:3]
    elif score[0] == 2:
        hand_type = "Pair"
        card_ranks = card_ranks[:4]
    elif score[0] == 1:
        hand_type = "HighCard"
        card_ranks = card_ranks[:5]
    else:
        raise Exception('Card Type error!')

    #print score, card_ranks, hand_type
    return score, card_ranks, hand_type


def eval_best_hand(hands):  # evaluate which hand is best
    scores = [(i, calc_score(hand)) for i, hand in enumerate(hands)]
    #print scores
    winner = sorted(scores, key=lambda x: x[1], reverse=True)[0][0]
    #print winner
    #print hands[winner], scores[winner][1][-1]
    return winner , hands[winner], scores[winner][1][-1]


def create_card_deck():
    # type: () -> object
    values = "23456789TJQKA"
    suites = "CDHS"
    Deck = []
    [Deck.append(x + y) for x in values for y in suites]
    return Deck

def create_suit_deck(suit):
    # type: () -> object
    values = "23456789TJQKA"
    suites = suit
    Deck = []
    [Deck.append(x + y) for x in values for y in suites]
    return Deck


def run_sim(P1,NumPlayers,B1):

    Player_cards = P1[:]
    Board = B1[:]

    #Create deck
    deck = None
    deck = create_card_deck()

    #remove cards on board from remaining cards in the deck before assigning player cards
    for a in range(len(Board)):
        deck.pop(deck.index(Board[a]))

    #remove player cards from deck
    for i in range(len(Player_cards)):
        deck.pop(deck.index(Player_cards[i]))

    #assign cards to players
    players = []
    for j in range(NumPlayers):
        #select two cards from the deck without duplicate cards
        cardNums = np.random.choice(len(deck),2,replace=False)
        hand = [deck[cardNums[0]],deck[cardNums[1]]]
        players.append(hand)
        deck.pop(deck.index(hand[0]))
        deck.pop(deck.index(hand[1]))



    #assign rest of the board
    boardnums = np.random.choice(len(deck), 5-len(Board), replace=False)
    for b in range(0,5-len(Board)):
        Board.append(deck[boardnums[b]])



    handlist = []
    playershand = Player_cards
    for c in range(len(Board)):
        playershand.append(Board[c])
        for d in range(NumPlayers):
           players[d].append(Board[c])

    handlist = [None]*(NumPlayers+1)
    handlist[0]= playershand
    handlist[1:] = players


    scores = []
    for i in range(len(handlist)):
        scores.append(calc_score(handlist[i]))

    #print scores
    #print 'hands: ', handlist
    global wins
    winornot,winninghand,winningscore =eval_best_hand(handlist)
    if winornot == 0:
        wins +=1


def sim(c1,c2):
    player1_hand = [c1,c2]
    board = []


    for i in range(0,1500):
        run_sim(player1_hand, 1, board)



suit1 = create_suit_deck('H')
suit2 = create_suit_deck('C')

listing = []

for i in range(0,13):
    for j in range(0,13):
        wins = 0
        sim(suit1[i],suit2[j])
        x= (float(wins)/1500 , str(suit1[i]+' '+  suit2[j]))
        print x
        listing.append(x)

df = pd.DataFrame(listing, columns = ('win%','Hand'))
df.to_csv('rankings.csv')





#print suit1, suit2




#global wins
#wins = 0
#sim()







"""
player1_hand = ['AH','AD']
player2_hand = ['TS','TD']
Flop = ('AC','AS','TD')
Turn = ['2C']
River = ['4D']


for i in range(len(Flop)):
    player1_hand.append(Flop[i])
    player2_hand.append(Flop[i])

HandsList = player1_hand ,player2_hand

a,b=  eval_best_hand(HandsList)

winner = HandsList.index(a)

print winner, HandsList

#print calc_score(player1_hand)

"""