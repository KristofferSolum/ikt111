from random import randint


class Category:
    def __init__(self, bot):
        self.name = None
        self.count = 0
        self.userName = None
        self.lastOutput = None
        self.botState = None
        self.bot = bot

    def setUserName(self, userName):
        self.userName = userName

    def setBotState(self, botState):
        self.botState = botState

    def createResponse(self, userInput, categoryHistory):
        raise NotImplementedError("This method should be overridden by subclass")


class DefaultCat(Category):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "default"
        self.happyResponses = [
            "I'm open to chat about whatever you want to talk about, {userName}! 😊",
            "Is there something on your mind, {userName}? I'm all ears! 😊",
            "Tell me what's on your mind, {userName}. Let's have a nice chat! 😊",
            "What would you like to discuss today, {userName}? I'm ready! 😊",
            "I'm here to chat, {userName}. What's up? 😊"
        ]

        self.sadResponses = [
            "I'm here to chat, if you want to talk about anything, {userName}. 😔",
            "Is there something bothering you, {userName}? 😔",
            "Feel free to share what's on your mind, {userName}. 😔",
            "What would you like to talk about today, {userName}? 😔",
            "I'm here for you, {userName}. What's on your mind? 😔"
        ]

        self.angryResponses = [
            "What do you want to talk about now, {userName}? 😡",
            "You again, {userName}? What now? 😡",
            "Go ahead, {userName}. I'm listening. 😡",
            "So, what do you want this time, {userName}? 😡",
            "Tell me what's on your mind, {userName}. 😡"
        ]

    def randomResponse(self, responseList=None):
        if self.bot.currentState == "happy":
            responseList = self.happyResponses
        elif self.bot.currentState == "sad":
            responseList = self.sadResponses
        elif self.bot.currentState == "angry":
            responseList = self.angryResponses

        output = responseList[randint(0, len(responseList) - 1)]
        while output == self.lastOutput:
            output = responseList[randint(0, len(responseList) - 1)]
        self.lastOutput = output
        return output.format(userName=self.userName)

    def reflectInput(self, userInput):
        if any(words in userInput.lower() for words in
               ["is", "are", "do", "does", "can", "could", "will", "would"]):
            return f"That's an interesting question, {self.userName}. What do you think?"
        else:
            return f"That's a great question, {self.userName}. Can you share more details?"

    def createResponse(self, userInput, categoryHistory):
        if len(categoryHistory) > 0:
            lastCategory = categoryHistory[-1]
            if lastCategory != "default" and lastCategory is not None and lastCategory != "smalltalk":
                return f"You were just talking about {lastCategory}.\n      Would you like to talk more about that?"

        if self.count >= 1:
            self.bot.currentCategory = "smalltalk"
            self.count = 0
            return self.bot.respond(userInput)

        if "?" in userInput:
            return self.reflectInput(userInput)
        self.count += 1
        return self.randomResponse()


class JokeCat(Category):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "joke"
        self.happyJokes = [
            "Why don’t we ever tell secrets on a farm? Because the potatoes have eyes, and the corn has ears! 😊",
            "What’s a skeleton’s least favorite room? The living room! 😊",
            "Why don’t scientists trust atoms? Because they make up everything! 😊",
            "I just learned how to juggle, and I’m over the moon! 😊",
            "Did you hear about the guy who invented Lifesavers? He made a mint! 😊",
            "Life’s too good not to tell this joke: Why did the scarecrow win an award? Because he was outstanding in "
            "his field! 😊"
        ]

        self.sadJokes = [
            "Why don’t some couples go to the gym? Because some relationships just don’t work out. 😔",
            "I tried to catch fog earlier... I mist. 😔",
            "What do you call fake spaghetti? An impasta. But who even cares... 😔",
            "I’m on a whiskey diet. I’ve lost three days already. 😔",
            "I asked the librarian if the library had any books on paranoia. She whispered, 'They’re right behind "
            "you.' But honestly, who even reads anymore? 😔",
            "Why don’t skeletons fight? They don’t have the guts. Just like me... 😔"
        ]

        self.angryJokes = [
            "Why is it so hard to trust stairs? Because they’re always up to something! And I’m sick of it! 😡",
            "Why did the golfer bring two pairs of pants? In case he got a hole in one! Ugh, why do I even bother "
            "with these jokes?! 😡",
            "I told my computer I needed a break. Now it’s frozen. Of course! 😡",
            "You know what’s annoying? I bought some shoes from a drug dealer, and I don’t know what he laced them "
            "with, but I’ve been tripping all day. 😡",
            "Why can’t bicycles stand up on their own? Because they’re two-tired! Just like me! 😡",
            "I went to a seafood disco last night and pulled a mussel. Seriously, can anything go right? 😡"
        ]

    def randomJoke(self):
        if self.bot.currentState == "happy":
            jokeList = self.happyJokes
        elif self.bot.currentState == "sad":
            jokeList = self.sadJokes
        else:
            jokeList = self.angryJokes

        joke = jokeList[randint(0, len(jokeList) - 1)]
        while joke == self.lastOutput:
            joke = jokeList[randint(0, len(jokeList) - 1)]
        self.lastOutput = joke
        return joke

    def createResponse(self, userInput, categoryHistory):
        if "tell" in userInput.lower() or "another" in userInput.lower() or "joke" in userInput.lower():
            return self.randomJoke()
        elif self.count < 1 and "no" not in userInput.lower():
            self.count += 1
            return f"If your up for a joke {self.userName}, just let me know.\n     I have som real good ones on mee 😄"
        else:
            self.bot.currentCategory = "default"
            self.count = 0
            return f"Okay, {self.userName}. Is there something else you want to talk about?"


class AdviceCat(Category):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "advice"
        self.happyAdvice = [
            "Wow, everything is going so well! Life is just full of sunshine today! 😊",
            "Isn't it great when everything just works out perfectly? 😊",
            "I’m feeling amazing today! Let’s keep this positive vibe going! 😊",
            "I’m so pumped up right now! Everything feels awesome! 😊",
            "Nothing can bring me down today, {userName}. Let's keep this happy energy rolling! 😊"
        ]

        self.sadAdvice = [
            "I just can’t seem to find the motivation today... 😔",
            "Things aren’t really going my way lately... 😔",
            "I feel like I’m stuck in a rut, {userName}... Everything’s so gloomy. 😔",
            "I wish things were better, but I just don’t feel like myself right now. 😔",
            "It’s just one of those days, you know? I’m really down... 😔"
        ]

        self.angryAdvice = [
            "I can't stand when things don't go as planned! 😡",
            "Ugh! Everything is so frustrating right now! 😡",
            "Why does nothing ever work when I need it to?! 😡",
            "I am really at my limit today, {userName}. Don’t even get me started! 😡",
            "This is ridiculous! Why does everything have to be so annoying?! 😡"
        ]

    def randomAdvice(self):
        if self.bot.currentState == "happy":
            adviceList = self.happyAdvice
        elif self.bot.currentState == "sad":
            adviceList = self.sadAdvice
        else:
            adviceList = self.angryAdvice

        advice = adviceList[randint(0, len(adviceList) - 1)]
        while advice == self.lastOutput:
            advice = adviceList[randint(0, len(adviceList) - 1)]
        self.lastOutput = advice
        return advice.format(userName=self.userName)

    def createResponse(self, userInput, categoryHistory):
        if "advice" in userInput.lower():
            return self.randomAdvice()
        elif self.count < 1 and "no" not in userInput.lower():
            self.count += 1
            return f"If you're looking for some advice, {self.userName}, I'm here to help!"
        else:
            self.bot.currentCategory = "default"
            self.count = 0
            return f"Okay, {self.userName}. Is there something else you want to talk about?"


class MotivationCat(Category):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "motivation"
        self.happyQuotes = [
            "Today’s a great day to accomplish something amazing! 😊",
            "Everything is going right today, {userName}! Let's make the most of it! 😊",
            "The sun’s shining, and so are you! Let's take on the world! 😊",
            "I'm so pumped up today! We can handle anything, {userName}! 😊",
            "Life’s beautiful, and the possibilities are endless! 😊"
        ]

        self.sadQuotes = [
            "I know it’s tough, but sometimes all we can do is keep going... 😔",
            "Things may not be great right now, but we’ll get through this, {userName}... slowly but surely. 😔",
            "Sometimes, the best thing you can do is just take one small step forward, even when it feels hard... 😔",
            "It’s okay to not be okay right now, {userName}. But we’ll find the strength again. 😔",
            "I’m not feeling too great today, but I know better days are coming. 😔"
        ]

        self.angryQuotes = [
            "I’m not giving up, and neither should you, {userName}. We’re going to fight through this! 😡",
            "Enough is enough! Let’s crush this obstacle, {userName}, and show them what we’re made of! 😡",
            "No more excuses, {userName}. We’ve got work to do! Let’s power through it! 😡",
            "This is ridiculous, but we’re not backing down. We’re going to win, no matter what! 😡",
            "I don’t care how hard it is today—we’re going to get through this, {userName}. Let’s fight! 😡"
        ]

    def randomQuote(self):
        if self.bot.currentState == "happy":
            quoteList = self.happyQuotes
        elif self.bot.currentState == "sad":
            quoteList = self.sadQuotes
        else:
            quoteList = self.angryQuotes

        quote = quoteList[randint(0, len(quoteList) - 1)]
        while quote == self.lastOutput:
            quote = quoteList[randint(0, len(quoteList) - 1)]
        self.lastOutput = quote
        return quote.format(userName=self.userName)

    def createResponse(self, userInput, categoryHistory):
        if "motivat" in userInput.lower() or "quote" in userInput.lower():
            return self.randomQuote()
        elif self.count < 1 and "no" not in userInput.lower():
            self.count += 1
            return f"If you need some motivation, I'm here for you {self.userName}!"
        else:
            self.bot.currentCategory = "default"
            self.count = 0
            return f"Okay, {self.userName}. Is there something else you want to talk about?"


class HealthCat(Category):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "health"
        self.happyHealthTips = [
            "Remember to stay hydrated! It keeps you feeling great! 😊",
            "Exercise is a fantastic way to boost your mood and keep your energy up! 😊",
            "Eating a healthy meal can make your day even better! 😊",
            "Getting outside and enjoying the sunshine can do wonders for your mental health! 😊",
            "A positive mindset is key to both mental and physical well-being! 😊"
        ]

        self.sadHealthTips = [
            "It’s important to take things slow. A small walk can help lift your mood a bit. 😔",
            "Try to get a bit more rest today, {userName}. Your mind and body need time to heal. 😔",
            "A deep breath can help ease some of the weight you’re feeling right now. 😔",
            "Staying hydrated might seem small, but it can make you feel just a little better. 😔",
            "Even a short break to close your eyes and relax can help when things feel overwhelming. 😔"
        ]

        self.angryHealthTips = [
            "A quick workout can help release some of that frustration! 😡",
            "When you're feeling stressed, deep breathing exercises can help calm things down. 😡",
            "Don’t let your anger build up, {userName}. A walk outside can help clear your head. 😡",
            "Try squeezing a stress ball or doing something physical to release that tension. 😡",
            "Taking a moment to step back and focus on your health can help you regain control. 😡"
        ]

    def randomTip(self):
        if self.bot.currentState == "happy":
            tipList = self.happyHealthTips
        elif self.bot.currentState == "sad":
            tipList = self.sadHealthTips
        else:
            tipList = self.angryHealthTips

        tip = tipList[randint(0, len(tipList) - 1)]
        while tip == self.lastOutput:
            tip = tipList[randint(0, len(tipList) - 1)]
        self.lastOutput = tip
        return tip

    def createResponse(self, userInput, categoryHistory):
        if "health" in userInput.lower() or "wealth" in userInput.lower() or "tip" in userInput.lower():
            return self.randomTip()
        elif self.count < 1 and "no" not in userInput.lower():
            self.count += 1
            return f"Just let me know if you want a healthy tip!"
        else:
            self.bot.currentCategory = "default"
            self.count = 0
            return f"Something else you want to chat about {self.userName}"


class SmallTalkCat(Category):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "smalltalk"
        self.happyQuestions = [
            "I’m feeling amazing today! How about you, {userName}? 😊",
            "Isn’t today just perfect? What’s making you smile today? 😊",
            "I’m in such a good mood! What’s something fun you’re looking forward to? 😊",
            "Everything’s going great! What’s been the highlight of your day, {userName}? 😊",
            "I feel like nothing could go wrong today! How’s your day going? 😊"
        ]

        self.sadQuestions = [
            "I’m feeling pretty down today... Have you ever had days like this, {userName}? 😔",
            "I just can’t seem to shake this sadness. How do you handle it when things feel heavy? 😔",
            "Do you ever just feel... stuck? That’s where I’m at right now. 😔",
            "I’m not having the best day... Do you ever feel like things are just too much? 😔",
            "It’s been a rough day, {userName}. How do you keep going when you feel like this? 😔"
        ]

        self.angryQuestions = [
            "Ugh, everything is annoying me today! Is it just me, or is everything frustrating you too, {userName}? 😡",
            "I’ve had it! What’s something that really gets on your nerves? 😡",
            "I can’t believe how frustrating things are today. What’s bothering you lately? 😡",
            "I’m so fed up! Does anything in particular drive you crazy, {userName}? 😡",
            "Nothing’s going my way today! What’s been ticking you off recently? 😡"
        ]

    def randomQuestion(self):
        if self.bot.currentState == "happy":
            questionList = self.happyQuestions
        elif self.bot.currentState == "sad":
            questionList = self.sadQuestions
        else:
            questionList = self.angryQuestions

        question = questionList[randint(0, len(questionList) - 1)]
        while question == self.lastOutput:
            question = questionList[randint(0, len(questionList) - 1)]
        self.lastOutput = question
        return question.format(userName=self.userName)

    def createResponse(self, userInput, categoryHistory):
        if self.count < 2:
            self.count += 1
            return self.randomQuestion()
        else:
            self.count = 0
            self.bot.currentCategory = "default"
            return self.bot.respond(userInput)


class SportsCat(Category):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "sport"
        self.happySports = [
            "Football is so exciting! Did you catch the latest match? 😊",
            "I love a good tennis match! Who’s your favorite player? 😊",
            "Basketball is such a fun sport to watch! Do you play or just enjoy watching? 😊",
            "I’m a huge fan of cricket! Which team are you rooting for? 😊",
            "Sports can be so uplifting! Do you have a favorite game you enjoy? 😊",
            "Watching live games can be thrilling! Have you ever been to a stadium? 😊"
        ]

        self.sadSports = [
            "Sometimes our favorite teams don’t win, and that can be rough. 😔",
            "Sports can be emotional, especially when a player gets injured. 😔",
            "I know what it feels like when your team keeps losing... It's tough. 😔",
            "It can be so disappointing when a match doesn’t go your way. 😔",
            "Losing a close game is hard. Who do you usually root for? 😔",
            "I totally understand when sports can bring you down. Who’s your favorite player, even on tough days? 😔"
        ]

        self.angrySports = [
            "Ugh! The referee’s call was totally unfair in that game! 😡",
            "I can’t believe they missed that goal! What a terrible play! 😡",
            "Why do some players never perform when it matters the most? So frustrating! 😡",
            "I hate it when my favorite team loses because of silly mistakes! 😡",
            "How do they keep making the same errors every game? It’s so annoying! 😡",
            "Sometimes watching sports just makes me mad. Do you feel the same way? 😡"
        ]

    def randomSportComment(self):
        if self.bot.currentState == "happy":
            sportsList = self.happySports
        elif self.bot.currentState == "sad":
            sportsList = self.sadSports
        else:
            sportsList = self.angrySports

        sport_comment = sportsList[randint(0, len(sportsList) - 1)]
        while sport_comment == self.lastOutput:
            sport_comment = sportsList[randint(0, len(sportsList) - 1)]
        self.lastOutput = sport_comment
        return sport_comment

    def createResponse(self, userInput, categoryHistory):
        if "sport" in userInput.lower() or "game" in userInput.lower() or "match" in userInput.lower():
            return self.randomSportComment()
        elif self.count < 1 and "no" not in userInput.lower():
            self.count += 1
            return f"Hey {self.userName}, ready to talk about some sports? I have some fun thoughts to share! 😄"
        else:
            self.bot.currentCategory = "default"
            self.count = 0
            return f"Okay, {self.userName}. Is there something else you want to chat about?"


class MoviesCat(Category):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "movie"
        self.happyMovies = [
            "I just saw a great movie! What’s your favorite film? 😊",
            "Movies can be so uplifting! What’s a movie that always cheers you up? 😊",
            "Do you like action, comedy, or something else? Movies are such a fun escape! 😊",
            "The cinema can be magical! Seen any good films lately? 😊",
            "I’m a fan of classic films! What genre do you prefer? 😊",
            "Popcorn and a great movie – sounds perfect, doesn’t it? 😊"
        ]

        self.sadMovies = [
            "Some movies just make you cry, don’t they? 😔",
            "Sad movies can hit hard. What’s the last movie that made you emotional? 😔",
            "Watching a tragic movie can really stir up emotions. What’s the saddest film you’ve seen? 😔",
            "I know the feeling when a movie’s ending just breaks your heart. 😔",
            "It’s tough watching sad stories sometimes. Do you have a favorite drama? 😔",
            "Sometimes all we need is a good cry and a sad movie. 😔"
        ]

        self.angryMovies = [
            "Ugh! That movie ending was so frustrating! Ever had that feeling? 😡",
            "I hate when they ruin a perfectly good plot with a terrible twist! 😡",
            "Why do some movies just not make sense? Ever watched something that made you angry? 😡",
            "Some movies really mess up their characters – it’s so annoying! 😡",
            "Why do they make sequels when the original movie was perfect?! 😡",
            "I can’t believe how badly some movies treat their characters. So frustrating! 😡"
        ]

    def randomMovieComment(self):
        if self.bot.currentState == "happy":
            movieList = self.happyMovies
        elif self.bot.currentState == "sad":
            movieList = self.sadMovies
        else:
            movieList = self.angryMovies

        movie_comment = movieList[randint(0, len(movieList) - 1)]
        while movie_comment == self.lastOutput:
            movie_comment = movieList[randint(0, len(movieList) - 1)]
        self.lastOutput = movie_comment
        return movie_comment

    def createResponse(self, userInput, categoryHistory):
        movie_keywords = ["movie", "film", "cinema", "director", "actor"]
        if any(keyword in userInput.lower() for keyword in movie_keywords):
            return self.randomMovieComment()
        elif self.count < 1 and "no" not in userInput.lower():
            self.count += 1
            return f"Hey {self.userName}, want to talk about movies? I’ve got some great film thoughts!"
        else:
            self.bot.currentCategory = "default"
            self.count = 0
            return f"Okay, {self.userName}. Anything else on your mind?"
