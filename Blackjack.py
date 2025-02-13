import random
import time

# Constant values for card Deck
cardValues = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, "Jack":10, "Queen":10, "King":10, "Ace":11}
suites = ["hearts", "spades", "clubs", "diamonds"]
# Creates a full card deck
def newCardDeck():
    cardDeck = {suite : cardValues.copy() for suite in suites}
    return cardDeck

# prompts user if they want to hit or stand, and returns value
def hitOrStand():
    userInput = input("Would you like to \"hit\" or \"stand\"?\n").lower()
    while userInput not in ["hit", "stand"]:
        userInput = input("That is not a valid input.\nWould you like to \"hit\" or \"stand\"?\n").lower()
    return userInput

def get_valid_input(prompt, valid_options):
    user_input = input(prompt).lower()
    while user_input not in valid_options:
        user_input = input("Invalid input. " + prompt).lower()
    return user_input

# gets a random card and removes it from the deck, returns deck, and all values of the card
def getCard(cardDeck):
    suite = random.choice(list(cardDeck.keys()))
    card = random.choice(list(cardDeck[suite].keys()))
    cardValue = cardDeck[suite][card]
    cardDeck[suite].pop(card)
    returnDict = {
        "card deck" : cardDeck,
        "suite" : suite,
        "card" : card,
        "card value" : cardValue
    }
    return returnDict

# gives returns two cards as a list to a player
def startingHand(cardDeck):
    playerCardList = []
    for i in range(2):
        returnDict = getCard(cardDeck)
        cardDeck = returnDict["card deck"]
        suite = returnDict["suite"]
        card = returnDict['card']
        cardValue = returnDict['card value']
        playerCardList.append([card, cardValue, suite])
        returnDict = {
            "card deck" : cardDeck,
            "player card list" : playerCardList
        }
    return returnDict

# gets the score from a player's card list and prints and returns the value
def getScore(cardList, name = "Dealer"):
    score = 0
    for element in cardList:
        score += element[1]
    if score > 21:
        for card in cardList:
            if card[1] == 11:
                score -= 10
    print(f"{name}'s score: {score}")
    print()
    return score

# Prints the card list of a player
def printCardList(cardList, numberOfCards, name = "Dealer"):
    print(f"{name}'s cards:")
    for index in range(0,numberOfCards):
        print(cardList[index][0], "of", cardList[index][2])
    print()

# gets result of the game between two players, and a bet if it applies
def gameResult(playerScore, dealerScore, name, bet = 0):
    returnDict = {"bet" : bet, "winner" : ""}
    if playerScore == True and dealerScore == True:
        print(f"{name} and dealer both have blackjack. It's a tie.")
    elif playerScore == True:
        print(f"{name} wins, {name} has blackjack")
        returnDict["winner"] = "player"
        returnDict["bet"] *= 1.5
    elif dealerScore == True:
        print(f"{name} loses, dealer has blackjack")
        returnDict["winner"] = "dealer"
        returnDict["bet"] = 0
    elif playerScore > 21:
        print(f"{name} loses! {name} broke.")
        returnDict["winner"] = "dealer"
        returnDict["bet"] = 0
    elif dealerScore > 21:
        print(f"{name} won! The dealer broke.")
        returnDict["winner"] = "player"
        returnDict["bet"] *= 2
    elif playerScore > dealerScore:
        print(f"{name} won! {name} has a higher score than the dealer.")
        returnDict["winner"] = "player"
        returnDict["bet"] *= 2
    elif playerScore < dealerScore:
        print(f"{name} loses! The dealer has a higher score than {name}.")
        returnDict["winner"] = "dealer"
        returnDict["bet"] = 0
    else:
        print("It's a tie!")
    return returnDict

# Dealer logic is to hit if score is less than or equal to 16
def dealerLogic(dealerScore):
    while dealerScore <= 16:
        return "hit"

# hits only if player score is less than 10 over the dealer's first card
def myLogic(score, dealerFirstCardValue):
    if score - dealerFirstCardValue < 10:
        return "hit"
    else:
        return ""

# takes input as a bet, only allowing players to bet as much money as they have, removing it from their total money
def getBet(playerMoney):
    print("Player money:", playerMoney)
    bet = int(input("How much money would you like to bet?"))
    while bet > playerMoney:
        bet = int(input("You do not have that much money.\nHow much money would you like to bet?"))
    playerMoney -= bet
    returnDict = {
        "player money" : playerMoney,
        "bet" : bet
    }
    return returnDict

# hits a card for a player, removes card from deck and returns deck and the card (card, value, and suite)
def hit(playerType, playerCardList, cardDeck):
    returnDict = getCard(cardDeck)
    cardDeck = returnDict["card deck"]
    suite = returnDict["suite"]
    card = returnDict['card']
    cardValue = returnDict['card value']
    playerCardList.append([card, cardValue, suite])
    printCardList(playerCardList, len(playerCardList), playerType)
    returnDict = {
        "player card list" : playerCardList,
        "card deck" : cardDeck
    }
    return returnDict

# Setup for playing a hand for a character
def playHand(playerType, dealerFirstCard, cardDeck, playerCardList = ""):
    print(f"It's {playerType}'s Turn\n")
    if playerType != "Dealer":
        returnDict = startingHand(cardDeck)
        cardDeck = returnDict["card deck"]
        playerCardList = returnDict["player card list"]
    printCardList(playerCardList, len(playerCardList), playerType)
    score = getScore(playerCardList, playerType)
    if score == 21:
        print(f"Blackjack! {playerType} wins!")
        return True
    action = "hit"
    time.sleep(1)
    while action == "hit" and score < 21:
        if playerType != "Computer" and playerType != "Dealer":
            action = hitOrStand()
        elif playerType == "Computer":
            action = myLogic(score, dealerFirstCard[1])
        else:
            action = dealerLogic(score)
        if action == "hit":
            returnDict = hit(playerType, playerCardList, cardDeck)
            playerCardList = returnDict['player card list']
            cardDeck = returnDict['card deck']
        score = getScore(playerCardList, playerType)
        if score > 21:
            break
    return score

# Setup for single player game with player and dealer
def singlePlayerGame(name, playerMoney, playerWins):
    cardDeck = newCardDeck()
    returnDict = getBet(playerMoney)
    playerMoney = returnDict['player money']
    bet = returnDict['bet']
    returnDict = startingHand(cardDeck)
    cardDeck = returnDict["card deck"]
    dealerCardList = returnDict["player card list"]
    print()
    printCardList(dealerCardList, 1) # printing dealer first card
    playerScore = playHand(name, dealerCardList[0], cardDeck)
    dealerScore = playHand("Dealer", dealerCardList[0], cardDeck, dealerCardList)
    print("player score =", playerScore)
    print("dealer score =", dealerScore)
    winnerBetDict = gameResult(playerScore, dealerScore, name, bet)
    playerMoney += winnerBetDict["bet"]
    returnDict = {"player money" : playerMoney, "player wins" : playerWins}
    return returnDict

# Setup for multiplayer game with player, computer, and dealer
def multiPlayerGame(name, playerMoney, playerWins, computerWins):
    returnDict = getBet(playerMoney)
    playerMoney = returnDict['player money']
    bet = returnDict['bet']
    cardDeck = newCardDeck()
    returnDict = startingHand(cardDeck)
    cardDeck = returnDict["card deck"]
    dealerCardList = returnDict["player card list"]
    print()
    printCardList(dealerCardList, 1) # print dealer's first card
    playerScore = playHand(name, dealerCardList[0], cardDeck)
    computerScore = playHand("Computer", dealerCardList[0], cardDeck)
    dealerScore = playHand("Dealer", dealerCardList[0], cardDeck, dealerCardList)

    print("player score =", playerScore)
    print("computer score =", computerScore)
    print("dealer score =", dealerScore)
    playerScore, dealerScore, name, bet
    winnerBetDict = gameResult(playerScore, dealerScore, name, bet)
    playerMoney += winnerBetDict["bet"]
    if winnerBetDict["winner"] == "player":
        playerWins += 1
    computerWinnerBetDict = gameResult(computerScore, dealerScore, "Computer", bet)
    if computerWinnerBetDict["winner"] == "player":
        computerWins += 1
    returnDict = {"player money" : playerMoney, "player wins" : playerWins, "computer wins" : computerWins}
    return returnDict

# Gets single player or multiplayer input
def singleOrMultiPlayer():
    userInput = input("\"Single player\" or \"Multiplayer\"\n").capitalize()
    while userInput not in ["Single player", "Signle player", "Sinlge player", "Multiplayer", "Mutliplayer"]:    # I'm accepting of gamer spelling
        userInput = input("Please enter a valid response. \"Single player\" or \"Multiplayer\"\n").capitalize()
    return userInput

# Gets input for play again or not
def playAgain():
    playAgain = input("Would you like to play again? (Yes) / (No)\n").capitalize()
    while playAgain not in ["Yes", "No"]:
        playAgain = input("That is not a valid input.\nWould you like to play again? (Yes) / (No)\n").capitalize()
    if playAgain == "No":
        return False
    else:
        return True


if __name__ == "__main__":
    playerWins = 0
    computerWins = 0
    playerMoney = 100
    wins = {"Player Wins" : 0, "Computer Wins" : 0}
    game = True
    name = input("What is your name?\n").capitalize()
    while game:
        gameType = singleOrMultiPlayer()
        if gameType == "Single player":
            returnDict = singlePlayerGame(name, playerMoney, playerWins)
        else:
            returnDict = multiPlayerGame(name, playerMoney, playerWins, computerWins)
            computerWins = returnDict["computer wins"]
            playerMoney = returnDict
        playerMoney = returnDict["player money"]
        playerWins = returnDict["player wins"]
        print("Player money:", playerMoney)
        game = playAgain()
    print("player wins:", playerWins)
    print("Computer wins:", computerWins)
    print("Wins are just for the multiplayer mode. It shows whether the player or computer is better.")