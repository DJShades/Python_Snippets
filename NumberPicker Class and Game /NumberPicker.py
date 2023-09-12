import random
import time

class NumberPicker:
    def __init__(self, lower: int, upper: int):
        # Range() doesn't work if higher value first, so flip values if necessary...
        if lower > upper:
            lower, upper = upper, lower
        self._numbers = list(range(lower,upper))
        self._picked = []
        self.total = upper - lower

    def pick(self) -> int | bool:
        if self._numbers != []:
            number = random.choice(self._numbers)
            self._numbers.pop(self._numbers.index(number))
            self._picked.append(number)
            return number

    def picked(self) -> list | bool:
        if self._picked != []:
            return self._picked

    def last(self) -> int | bool:
        if len(self._picked) > 1:
            return self._picked[-2]

    def available(self) -> list | bool:
        if self._numbers != []:
            return self._numbers

# Tests

# numbers = NumberPicker(1,6)
# for _ in range(numbers.total):
#     print(f' Available numbers: {numbers.available()}')
#     print(f'     Number picked: {numbers.pick()}')
#     print(f'Last picked number: {numbers.last()}')
#     print(f'All picked numbers: {numbers.picked()}\n')

# #What happens if we try to pick after no numbers left?
# print(numbers.pick(),'\n')
        
# numbers = NumberPicker(11,5)
# while numbers.available():
#     print(f' Available numbers: {numbers.available()}')
#     print(f'     Number picked: {numbers.pick()}')
#     print(f'Last picked number: {numbers.last()}')
#     print(f'All picked numbers: {numbers.picked()}\n')

def guesser(lower: int, upper: int, target: int) -> None:
    guess = None
    numbers = NumberPicker(lower,upper)
    while guess != target:
        guess = numbers.pick()
        if guess != target:
            print(f'{guess} is not your chosen number. Let me try again.')
        else:
            print(f'Your number is {guess}!')

def higher_or_lower(upper=None,lower=None):
    if type(upper) == str:
        print('Python can\'t play Higher or Lower with letters. Try a number instead!')
    elif type(upper) == float:
        print('Decimal places? We\'d be here forever! Try a whole number instead.')
    elif type(upper) == int:
        if upper < 2:
            print('Sorry, Python needs at least 2 numbers to play this game!')
        else:           
            # Make our numbers object...
            numbers = NumberPicker(1,upper+1)
            # Pick a number to start...
            number = numbers.pick()

            correct_answers = 0
            correct = 'Python chose correctly!'
            incorrect = 'Python chose incorrectly!'

            print(f'The first number is {number}, will the next be higher or lower?')
            time.sleep(2)
            
            while numbers.available():
                # Python makes an informed "guess" if the current number is the lowest
                # or highest available, otherwise it is a complete guess.
                if number < numbers.available()[0]:
                    pythons_choice = True
                elif number > numbers.available()[-1]:
                    pythons_choice = False
                else:
                    pythons_choice = random.choice([True,False])
            
                if pythons_choice:
                    print('Python chooses higher')
                else:
                    print('Python chooses lower')
                time.sleep(1)
            
                number = numbers.pick()
                print(f'The new number is {number}')
                time.sleep(1)
            
                # There's probably a far better way to do this...
                if number > numbers.last():
                    if pythons_choice:
                        msg = 'Python chose wisely!'
                        correct_answers += 1
                    else:
                        msg = 'Python chose poorly!'
                else:
                    if pythons_choice:
                        msg = 'Python chose poorly!'
                    else:
                        msg = 'Python chose wisely!'
                        correct_answers += 1
                print(msg,'\n')
                time.sleep(2)

                if numbers.available():
                    print(f'The current number is now {number}, will the next number be higher or lower?')
                    time.sleep(3)
            else:
                print(f'Python got {correct_answers} answers correct!')
    else:
        print('You\'re just being silly now. Python needs a (whole) number to play Higher or Lower!')
            
# Start a game...

#guesser(0,500,420)
higher_or_lower(12)
