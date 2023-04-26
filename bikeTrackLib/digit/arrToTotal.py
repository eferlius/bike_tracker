# -*- coding: utf-8 -*-

def fromArrayOfDigitsToTotal(results, reverse = True):
    if reverse:
        results.reverse() # from units to tens to hundreds
    total = 0
    invalidValueFlag = False
    # it's not possible to have a valid value after an invalid one
    for r, i in zip(results, range(len(results))):
        if r >= 0 and r <= 9:
            if invalidValueFlag == False:
                total += r*10**i
            elif invalidValueFlag == True:
                return -1
        else:
            invalidValueFlag = True
    return total

