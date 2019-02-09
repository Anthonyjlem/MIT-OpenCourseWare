# Problem Set 4A
# Name: Anthony Lem
# Collaborators: 
# Time Spent: 

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    #A function to take the first letter of a sequence of letters and insert it
    #in-between every other letter as well as in front and behind the other
    #letters.
    def inserter(short_sequence, sequence):
        permutations = []
        for i in range(len(short_sequence)):
            new_permutation = list(short_sequence[:])
            new_permutation.insert(i, sequence[0])
            permutations.append("".join(new_permutation))
        copy_sequence = list(short_sequence[:])
        copy_sequence.append(sequence[0])
        permutations.append("".join(copy_sequence))
        return permutations
        
    #The base case is if our sequence is one letter long.
    if len(sequence) == 1:
        return list(sequence)
    #If the input is not the base case:
    else:
        #Simplify the input and call it recursively to reach the base case.
        reduced_sequence = list(sequence[1:])
        next_permutations = get_permutations(reduced_sequence)
        #Generate all possible permutations starting from our base case and
        #insert the first letter of the sequence everywhere possible.
        permutations = []
        for permutation in next_permutations:
            other_permutations = inserter(permutation, sequence)
            permutations += other_permutations
        return permutations

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    print(get_permutations("abcde"))
    print(len(get_permutations("abcde")))
