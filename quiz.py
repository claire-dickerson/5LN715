import random
from operator import attrgetter

class Quiz:
    def __init__(self, name):
        self.name = name
        self.questions = []
    def add_question(self, ques):
        self.questions.append(ques)
    
    def do(self):
        counter = 0
        print(self.name)
        print(12 * '=')
        for question in self.questions: 
            (user,correct) = question.ask()
            if int(user) == int(correct):
                counter += 1
                print ('Correct!')
            else:
                print('Sorry, no. Correct answer: ',correct)
            print('')    
        print('You answered', counter, 'out of', len(self.questions), 'correctly!')
        if counter == len(self.questions):
            return True
        else:
            return False
    
    def do_until_right(self):
        correct = False
        while not correct:
            correct = self.do()
            print('')
 
ALTERNATIVES = 4   
 
class Question:  
    def __init__(self, ques, answer):
        self.ques = ques
        self.answer = answer
        self.wronganswers = []
        
    def add_wrong(self, wrong):
        new = WrongAnswer(wrong)
        self.wronganswers.append(new)
        
    def ask(self):
        print(self.ques)
        allanswers = []
        if len(self.wronganswers) > (ALTERNATIVES - 1):
            self.wronganswers = sorted(self.wronganswers, key = attrgetter('s'), reverse = True)
            allanswers = [self.answer] + self.wronganswers[: ALTERNATIVES -1]
        else:
            allanswers.append(self.answer)
            allanswers.extend(self.wronganswers)
        random.shuffle(allanswers)
        for i, ans in enumerate(allanswers, start=1):
            if type(ans) == str:
                right_ans = i
                print(str(i) + ': ' + str(ans))
            else:
                ans.displays += 1
                ans.calculate_s()
                print(str(i) + ': ' + str(ans.wrongans))
        user_ans = input('What is your answer? ')
        if int(user_ans) != right_ans:
            allanswers[int(user_ans)-1].choice += 1
            allanswers[int(user_ans)-1].calculate_s()
        return (user_ans, right_ans)
    
class IntQuestion(Question):
    def ask(self):
        print(self.ques)
        user = int(input('Which is your answer? '))
        return (user, self.answer)

class WrongAnswer():
    def __init__(self, wrongans):
        self.wrongans = wrongans
        self.displays = 0
        self.choice = 0
        self.s = 1
        
    def calculate_s(self):
        self.s = (2 * self.choice + 1) / (self.displays + 1)
                
def create_quiz_from_file(filename):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            command, data = line.split(' ', 1)
            data = data.strip()
            if command == 'name':
                quiz = Quiz(data)
            elif command == 'q' or command == 'iq':
                text = data
                q_type = command
            elif command == 'a':
                if q_type == 'q':
                    question = Question(text, data)
                elif q_type == 'iq':
                    question = IntQuestion(text, data)
                quiz.add_question(question)
            elif command == 'w':
                question.add_wrong(data)
    return quiz
    

