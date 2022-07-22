"""
# Author  : Jason Connie
# Updated : July 2022

Code to simulate shuffling a deck of cards with mathematically deterministic faro shuffles, 
as outlined in the related paper "Perfect and Semi-Perfect Shuffles"

(It is clearest what is going on when a live card demo is given to accompany the code's simulations)


NOTE: Getting the names of the cards will only work for a deck that is 64 or less in length. This is 
      because card names are a specific labeling convention for real-world playing cards, and decks 
      never exceed 64 in practice. For arrays larger than 64, 'cards' can be labeled simply with integer 
      indices rather than by '4C' or 'AH', and the 'deck_name' method would not need to be called.
      
      Though the 'in-faro' and 'out-faro' can be applied to decks that are a multiple of 2 in length, 
      the 'double' and 'straddled' faros can only be applied to decks that are a multiple of 4 in length.
      This is a natural constraint, as the double and straddled faros can be thought of as applying a 
      permutation of length 4 to pieces of the deck (see the paper for details). As such, these shuffles 
      should only be applied to a deck that is a multiple of 4 in length.

"""


import numpy as np

# We save the names of the seven shuffles as variables, so that we can input the shuffle names as either strings or variable names
fi  = 'fi'  # Corresponds to the in faro
fo  = 'fo'  # Corresponds to the out faro
si  = 'si'  # Corresponds to the in straddle faro
so  = 'so'  # Corresponds to the out straddle faro
di  = 'di'  # Corresponds to the in double faro
do  = 'do'  # Corresponds to the out double faro
rfo = 'rfo' # Corresponds to the reverse out faro



###############################################################################################
#  The following 7 methods are our deterministic faro-based shuffles                          #
#  For all shuffles, p is the position of the individual card we are moving, indexing from 0  #
#  For all shuffles, N is the decksize                                                        #
###############################################################################################

""" Reverse out faro """
def reverse_f_out(p, N):
    mid = N//2
    if (p%2==0):
        return p//2
    else:
        return mid + p//2


""" Out faro """
def f_out(p, N):
    if (p>=0 and p<(N-1)):
        return (2*p)%(N-1)
    else:
        return N-1    


""" In faro"""
def f_in(p, N):
    return (2*p+1)%(N+1)


""" Double out faro """
def d_out(p, N):
    if (p==(N-1)):
        return N-1
    
    elif (p<N/2):
        if (p%2==0):
            return (2*p)      
        else:
            return (2*p-1)    

    else:
        if (p%2==0):
            return (2*p+1)%(N-1)        
        else:
            return (2*p)%(N-1)        


""" Double in faro """
def d_in(p, N):
    if (p<N/2):
        if (p%2==0):
            return (2*p+2)
        else:
            return (2*p+1)

    else:
        if (p%2==0):
            return (2*p+1)%(N+1)        
        else:
            return (2*p)%(N+1)


""" Straddled double out faro """
def s_out(p, N):
    if (p<N/2):
        if (p%2==0):
            return (2*p)
        else:
            return (2*p+1)

    else:
        if (p%2==0):
            return (2*p+2)%(N+1)        
        else:
            return (2*p+1)%(N+1)
  

""" Straddled double in faro """
def s_in(p, N):
    if (p<N/2):
        if (p%2==0):
            return (2*p+1)
        else:
            return (2*p)

    else:
        if (p%2==0):
            return (2*p+1)%(N+1)        
        else:
            return (2*p+2)%(N+1)



######################################################################
##   The following methods are all about using the above shuffles   ##
##  As well as getting the final order of the deck after shuffling  ##
######################################################################
            
""" Method to apply one of our seven shuffles to the entire inputted deck    
    Any string that isn't a shuffle name results in the deck being returned as is
"""
def shuffle(faro_type, deck):
    N = len(deck)
    
    faro_type = faro_type.lower()
    
    if (faro_type=='fo'):
        return [f_out(x,N) for x in deck]
    elif (faro_type=='fi'):
        return [f_in(x,N)  for x in deck]
    elif (faro_type=='do'):
        return [d_out(x,N) for x in deck]
    elif (faro_type=='di'):
        return [d_in(x,N)  for x in deck]
    elif (faro_type=='so'):
        return [s_out(x,N) for x in deck]
    elif (faro_type=='si'):
        return [s_in(x,N)  for x in deck]
    elif (faro_type=='rfo'):
        return [reverse_f_out(x,N) for x in deck]
    else:
        return deck




""" Method to take as input a list of faro shuffles as well as a deck for the shuffles to be applied to.
    Examples:
        - 'faro_list = [fi,fo,si]' would apply an inner faro, an outer faro and a straddle inner faro in that order
        - 'faro_list = []' would just return the deck without any shuffles being applied
"""
def shuffle_sequence(faro_list, deck):

    for i in range(len(faro_list)):
        deck = shuffle(faro_list[i], deck)
    
    return deck




""" Method to return the name of a card, given its card value and the size of the deck
    In a deck of 52 cards for example, 'card_val=13' would return 'AC' (the Ace of Clubs)
    
    Deck size should be a multiple of four, and no greater than 64
"""
def card_name(card_val, deck_size):
    # If the deck size is inappropriate, we print a warning message and return None
    if (deck_size>64):
        print("Card names don't exist for such unreasonably large decks!")
        return None
    if (deck_size<0):
        print("That is not a meaningful number of cards.")
        return None
    if (deck_size%4 != 0):
        print("You need a deck that can be divided into four suits.")
        return None
      
    suit_size = int(deck_size/4)
    
    values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K','14','15','16']
    suits  = ['H','C','D','S']            # Suit order can of course be changed
    
    card = values[card_val%suit_size]+'.'
    card += suits[card_val//suit_size]
    
    return card




""" Prints out the name of every card in the deck, in order. 
    Only callable for deck lengths that are a multiple of 4, and for lengths that are 64 or less 
"""
def deck_name(deck):
    deck_size = len(deck)

    # If the deck size is inappropriate, we print a warning message and return None
    if (deck_size>64):
        print("Card names don't exist for such unreasonably large decks!")
        return None
    if (deck_size%4 != 0):
        print("You need a deck that can be divided into four suits.")
        return None
    
    proper_deck = [None]*deck_size
    
    for i in range(deck_size):
        j = deck[i]
        proper_deck[j] = i
    
    names = [card_name(x, deck_size) for x in proper_deck]
    print('\nThe deck after shuffling is:\n')
    
    tmp = ''
    for i in range(deck_size):
        tmp = tmp+ names[i] + ', '
        
    tmp = tmp[0:len(tmp)-2]
    
    print(tmp)
    
    return None






if __name__=='__main__':
    # First shuffle sequence, on a fresh deck
    deck = np.array(range(52))
    shuf_deck = shuffle_sequence([fo,fo,fo,fo,fo,fo,fo,fo], deck)   # 8 out faros return a 52 card deck to its original order!
    deck_name(shuf_deck)


    # Second shuffle sequence, on a fresh deck
    deck = np.array(range(32))
    shuf_deck = shuffle_sequence([fi,fi,so,fo,di], deck)
    deck_name(shuf_deck)
    
