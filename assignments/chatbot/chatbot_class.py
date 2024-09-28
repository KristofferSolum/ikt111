import chatbot_categories


class Bot:
    def __init__(self, botName):
        self.botName = botName
        self.userName = None,
        self.currentCategory = None
        self.categoryHistory = []
        self.currentState = "happy"
        self.stateCount = 4
        self.categories = {
            "default": chatbot_categories.DefaultCat(self),
            "joke": chatbot_categories.JokeCat(self),
            "advice": chatbot_categories.AdviceCat(self),
            "motivation": chatbot_categories.MotivationCat(self),
            "health": chatbot_categories.HealthCat(self),
            "smalltalk": chatbot_categories.SmallTalkCat(self),
            "sport": chatbot_categories.SportsCat(self),
            "movie": chatbot_categories.MoviesCat(self)
        }

    def updateState(self):
        if self.stateCount >= 2:
            self.currentState = "happy"
        elif self.stateCount >= -2:
            self.currentState = "sad"
        else:
            self.currentState = "angry"

    def updateStateCount(self, userInput):
        happyWords = ["good", "nice", "joke", "please", "haha", ":)", "great", "awesome", "love", "😊"]
        negativeWords = ["no", "bad", ":(", "hate", "terrible", "annoyed", "angry", "😡"]
        for word in userInput.split():
            for i in happyWords:
                if i in word.lower():
                    self.stateCount += 1
            for i in negativeWords:
                if i in word.lower():
                    self.stateCount -= 1

    def setNameAndState(self, name):
        self.userName = name
        for category in self.categories.values():
            category.setUserName(name)
            category.setBotState(self.currentState)

    def setCategory(self, category):
        self.currentCategory = category

    def addHistory(self):
        self.categoryHistory.append(self.currentCategory)

    def respond(self, userInput):
        if "joke" in userInput.lower():
            self.setCategory("joke")
        elif "advice" in userInput.lower():
            self.setCategory("advice")
        elif "motivat" in userInput.lower():
            self.setCategory("motivation")
        elif "health" in userInput.lower() or "wellness" in userInput.lower():
            self.setCategory("health")
        elif "sport" in userInput.lower() or "game" in userInput.lower() or "match" in userInput.lower():
            self.setCategory("sport")
        elif "movie" in userInput.lower() or "film" in userInput.lower():
            self.setCategory("movie")
        else:
            if not self.currentCategory:
                self.setCategory("default")
        response = self.categories[self.currentCategory].createResponse(userInput, self.categoryHistory)
        self.addHistory()
        return response

    def chatting(self):
        print(f"{self.botName}: Hello my name is {self.botName}!\n{self.botName}: Who am i speaking with?")
        userInput = str(input("You: "))

        self.setNameAndState(userInput[0].upper() + userInput[1:])

        print(f"{self.botName}: Nice to meet you {self.userName}")

        while True:
            userInput = str(input(f"{self.userName}: "))

            if ("bye" in userInput.lower() or "exit" in userInput.lower() or "have a" in userInput.lower() and "day"
                    in userInput.lower()):
                if self.currentState == "happy":
                    print(f"{self.botName}: It was so nice chatting with you, {self.userName}. Have a wonderful day! 😊")
                elif self.currentState == "sad":
                    print(f"{self.botName}: It was nice chatting with you, {self.userName}. Take care... 😔")
                elif self.currentState == "angry":
                    print(f"{self.botName}: Finally. Bye, {self.userName}. 😡")
                break

            # updating chatbot state to the chatbotCategories
            self.updateStateCount(userInput)
            self.updateState()
            for category in self.categories.values():
                category.setBotState(self.currentState)

            response = self.respond(userInput)
            print(f"{self.botName}: {response}")
