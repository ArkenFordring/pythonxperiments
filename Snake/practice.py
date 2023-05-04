import random


# Bingo/Lottery Function. Uses numBingoRange for how many numbers in total, numBingoSelect for how many to choose.
def bingo(bingo_range, bingo_selected):
    bingo_numbers = [0] * bingo_range

    for listBingo in range(bingo_range):
        bingo_numbers[listBingo] = listBingo + 1

    player_choice = random.sample(bingo_numbers, bingo_selected)

    for bingoSelect in player_choice:
        print(bingoSelect, end=", ")


# Calling the Functions
if __name__ == '__main__':
    print('Range: ')
    myRange = input()
    print('Select: ')
    mySelected = input()
    print('Range is ' + str(myRange) + ' and Selected is ' + str(mySelected))
    bingo(int(myRange), int(mySelected))
