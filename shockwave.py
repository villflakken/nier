import pylab as pl

# Disclosure for the sake of the current git repo: 
# This code is borrowed from a kind-hearted soul on the internet, whose identity I have lost in the annals of time.

# Known values # Taken from URL: (https://nierautomata.wiki.fextralife.com/Shock+Wave)
factor0 = 1.
factor1 = 1.5
factor2 = 2.
factor3 = 2.5
factor4 = 3.75
factor5 = 5.
factor6 = 6.75
factor8 = 12.75
fs_known = pl.array([factor0, factor1, factor2, factor3, factor4, factor5, factor6, factor8])

# We know the +8 chip is also the damage limit, as it is called 'Very powerful shockwave';
# and if you try to stack some of chips on top of each other,
# then you will be notified when you overreach this limit.

# Note, how there are linear relationships between the values for ranks (0,1,2,3)[*], 
# and then a slightly increased linear relationship for ranks (3,4,5)[**],
# And then it is clear that the slope for ranks (5,6) is further increased.

# Hazarding a guess for the values on the missing chip:
# It wouldn't be far-fetched to assume that all three of the ranks (5,6,7)
# could have the same linear relatioship (form a straight line),
factor7lin = factor6 + (factor6 - factor5) #=> 8.5
# which is a simple model to make from a gamedev point of view.

# Then again, to reward players to upgrade to rank 7, they may also have made the upgrade from 6 to 7
# to show a similar increase in the slope of the graph, as the increase was shown from the first group[*]
# and then to the second[**]. 
### (Basically talking about if/how the damage output "ac/decelerates".) ###
acc1st = (factor4 - factor3) - (factor3 - factor2) #=> 0.75
acc2nd = (factor6 - factor5) - (factor5 - factor4) #=> 0.5

# What we want, is to know if the way that the 3rd increase has a linear
# relationship with the previous increases.
# Printing the changes to of the changes of the damage factor leads us to believe 
# that the amount of how much the linear increase changing,
# is declining for every time that the increase shifts:
# This could indicate that:
acc3rd     = acc2nd  + (acc2nd - acc1st) #=> 0.25
factor7acc = factor6 + ((factor6 - factor5) + acc3rd) #=> 8.75 # Basically 'Forward Euler' w/ acc.

# Or they may just have used a 'clean number'... This is currently unknown. 
# But could qualify as a 'good guess'.
factor7hyp = 9.

fs_lin = pl.array([factor0, factor1, factor2, factor3, factor4, factor5, factor6, factor7lin, factor8])
fs_acc = pl.array([factor0, factor1, factor2, factor3, factor4, factor5, factor6, factor7acc, factor8])
fs_hyp = pl.array([factor0, factor1, factor2, factor3, factor4, factor5, factor6, factor7hyp, factor8])
pl.figure()
pl.plot( [6,7,8],          fs_lin[6:9], linestyle=':', marker='o', color='red')
pl.plot( [6,7,8],          fs_hyp[6:9], linestyle=':', marker='o', color='cyan')
pl.plot( [6,7,8],          fs_acc[6:9], linestyle=':', marker='o', color='black')
pl.plot( [0,1,2,3,4,5,6], fs_known[:7], linestyle='-', marker='.', color='blue')
pl.plot(             [8],[fs_known[7]], linestyle='-', marker='.', color='blue')
pl.xlabel('Rank')
pl.ylabel('Shockwave damage output (normalized w.r.t. rank 0)')
pl.legend(["Lin. curve", "Hypoth. curve", "Acc. curve", "Known Points"])
pl.grid('on')
# pl.show()

def combomaker(dmg7mod):
    """
    takes a guess for a rank7 damage modifier, calculates combinations that reach damage cap
    """
    # var | factor | cost | rank
    rank0 = (1.      ,    4 , "0")
    rank1 = (1.5     ,    5 , "1")
    rank2 = (2.      ,    6 , "2")
    rank3 = (2.5     ,    7 , "3")
    rank4 = (3.75    ,    9 , "4")
    rank5 = (5.      ,   11 , "5")
    rank6 = (6.75    ,   14 , "6")
    rank7 = (dmg7mod ,   17 , "7")
    rank8 = (12.75   ,   21 , "8")
    Nchip = (0.      ,    0 , " ")

    ranklist = [rank0,rank1,rank2,rank3,rank4,rank5,rank6,rank7,rank8,Nchip]

    # Preferred ranks to choose, not concerned with cap
    rankeffc = []
    for item in ranklist[:-1]:
        rankeffc.append(item[0]/item[1])
        pass

    rankeffcimprov = []
    for i in range(1,len(rankeffc)):
        rankeffcimprov.append(rankeffc[i] - rankeffc[i-1])
        pass

    # Pure and simple, output yield vs. chip slot cost:
    preferredRanks         = pl.argsort(rankeffc)[::-1]

    # This is more important if you're considering shuffling other chips, to make
    # room for a potential higher rank:
    preferredRankIncreases = pl.argsort(rankeffcimprov)[::-1]+1
    print preferredRanks         #=> [8 7 6 5 4 3 2 1 0]
    print preferredRankIncreases #=> [8 4 1 5 2 7 6 3] 

    # Combinations
    combos  = []
    slotcap = 12.75

    for first in ranklist:
        dmgm1st = first[0]
        cost1st = first[1]
        rank1st = first[2]

        for second in ranklist:
            dmgm2nd = second[0]
            cost2nd = second[1]
            rank2nd = second[2]

            for third in ranklist:
                dmgm3rd = third[0]
                cost3rd = third[1]
                rank3rd = third[2]

                dmgmodtot = dmgm1st + dmgm2nd + dmgm3rd
                chipscost = cost1st + cost2nd + cost3rd

                if dmgmodtot == slotcap: # and chipscost <= rank8[1]:
                    rankscomb = rank1st + rank2nd + rank3rd

                    combos.append([dmgmodtot, chipscost, rankscomb])
    return combos


def guessworkprinter(rank7dmg_guesses):
    """
    prints results from guesses
    """
    if hasattr(rank7dmg_guesses, '__iter__'):
        pass
    else:
        rank7dmg_guesses = list(rank7dmg_guesses)
        pass

    for guess in rank7dmg_guesses:
        print "for +7 chip damage modifier at:", guess
        combos = combomaker(guess)
        for combo in combos:
            print combo
        print
    return 0


rank7dmg_guesses = 8.5, 8.75, 9.

guessworkprinter(rank7dmg_guesses)
