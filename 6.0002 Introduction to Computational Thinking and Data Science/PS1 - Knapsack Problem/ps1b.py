###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Anthony
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    if (egg_weights, target_weight) in memo:
##        print("memo")
        result = memo[(egg_weights, target_weight)]
    elif target_weight == 0:
##        print("target_weight = 0")
        result = 0
    elif len(egg_weights) > 1:
        if egg_weights[-1] > target_weight:
            #Explore right branch only
##            print("right branch only")
            result = dp_make_weight(egg_weights[:-1], target_weight, memo)
        else:
            #Explore left branch
##            print("left!")
##            print(target_weight - egg_weights[-1])
            took_egg = dp_make_weight(egg_weights, target_weight - egg_weights[-1], memo)
            took_egg += 1
            #Explore right branch
##            print("right!")
            not_took = dp_make_weight(egg_weights[:-1], target_weight, memo)
            not_took += 1
            #Choose better branch
            if took_egg < not_took:
                result = took_egg
            else:
                result = not_took
    else:
##        print("result is target_weight =", target_weight)
        result = target_weight
    memo[(egg_weights, target_weight)] = result
##    print(result)
    return result    

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
