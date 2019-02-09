# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Anthony Lem
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):

    def __init__(self, guid, title, description, link, pubdate):
        """Stores guid, title, description, link and pubdate as data attributes."""
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        """Returns the value of guid."""
        return self.guid

    def get_title(self):
        """Returns the value of title."""
        return self.title

    def get_description(self):
        """Returns the value of description."""
        return self.description

    def get_link(self):
        """Returns the value of link."""
        return self.link

    def get_pubdate(self):
        """Returns the value of pubdate."""
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger

class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        """Stores phrase as a data attribute."""
        #Test to see if the phrase is valid before storing it.
        valid = True
        for punctuation in string.punctuation:
            if punctuation in phrase:
                print("Not a valid phrase. Please remove punctuation.")
                valid = False
        if "  " in phrase:
            print("Not a valid phrase. Please remove excess spaces.")
            valid = False
        if valid:
            self.phrase = phrase

    def is_phrase_in(self, text):
        """
        Text is a string.
        This function will return True if the phrase is in the given text and
        False otherwise.
        """
        phrase = self.phrase.lower()
        test_text = text.lower()
        for punctuation in string.punctuation:
            if punctuation in test_text:
                test_text = test_text.replace(punctuation, " ")
        split_text = test_text.split()
        split_phrase = phrase.split()
        counter = 0
        for word1 in split_phrase:
            for word2 in split_text:
                if word1 == word2:
                    counter += 1
                    break
        if counter == len(split_phrase):
            normal_text = " ".join(split_text)
            return phrase in normal_text
        else:
            return False

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):

    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.is_phrase_in(story.get_title())
        
# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):

    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):

    def __init__(self, time):
        """
        Time is a string.
        Stores time as a datetime object.
        """
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        #The format of time must match the format
        #%a = weekday as locale's abbreviated name (ie. Sun, Mon...)
        #%d = day of the month as a zero-padded decimal number (ie. 01, 02...)
        #%b = month as locale's abbreviated name (ie. Jan, Feb...)
        #%Y = Year with century as a decmial number (ie. 0001, 2013...)
        #%H = Hour (24-hour clock) as a zero-padded decimal number (ie. 00, 23...)
        #%M = Minute as a zero-padded decimal number (ie. 00, 59...)
        #&S = Second as a zero-padded number (ie. 00, 59...)
        #%Z = Time zone name (empty string if the object is naive) (ie. UTC, EST...)

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):

    def __init__(self, time):
        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        """
        Returns True to generate an alert if the story was published before the
        time flag.
        """
        if story.get_pubdate().tzinfo != None:
            self.time = self.time.replace(tzinfo = pytz.timezone("EST"))
        #tzinfo stands for "time zone info"
        #pytz is the standard library
        #These two lines are important so that an aware datetime is created (it has a time zone) if the pubdate is aware, allowing the two to be compared
        return story.get_pubdate() < self.time

class AfterTrigger(TimeTrigger):

    def __init__(self, time):
        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        """
        Returns True to generate an alert if the story was published before the
        time flag.
        """
        if story.get_pubdate().tzinfo != None:
            self.time = self.time.replace(tzinfo = pytz.timezone("EST"))
        return story.get_pubdate() > self.time

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):

    def __init__(self, trigger):
        """
        Trigger is a type of trigger.
        Stores trigger as a data attribute.
        """
        self.trigger = trigger

    def evaluate(self, news):
        """
        News is a NewsStory.
        Produces a boolean output opposite of another trigger's.
        """
        return not self.trigger.evaluate(news)

# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):

    def __init__(self, trigger1, other_trigger):
        """
        Both triggers are types of triggers.
        Stores triggers 1 and other_trigger as data attributes.
        """
        self.trigger1 = trigger1
        self.other_trigger = other_trigger

    def evaluate(self, news):
        """
        Input: news is a NewsStory.
        Output: returns True only if triggers 1 and 2 would both return True on news,
        """
        return self.trigger1.evaluate(news) & self.other_trigger.evaluate(news)

# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        """
        Triggers 1 and 2 are both types of triggers.
        Stores triggers 1 and 2 as data attributes.
        """
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, news):
        """
        Input: news is a NewsStory.
        Output: returns True if either triggers 1 and 2 would return True on news,
        """
        return self.trigger1.evaluate(news) or self.trigger2.evaluate(news)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)

    #Create an empty list
    reports = []
    #Iterate over the triggerlist testing to see which story in stories returns True
    for trigger in triggerlist:
        for story in stories:
    #Append every story that returns True to the empty list
            if trigger.evaluate(story):
                reports.append(story)
    #Return that list
    return reports
    #return stories


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    triggers = []
    created_triggers = {}
    trigger_type = {"DESCRIPTION":DescriptionTrigger, "TITLE":TitleTrigger, "BEFORE":BeforeTrigger, "AFTER":AfterTrigger, "NOT":NotTrigger, "AND":AndTrigger, "OR":OrTrigger}
    for line in lines:
        line = line.split(",")
        print(line)
        if line[0] != "ADD":
            if line[1] != "AND" and line[1] != "OR":
                trigger = trigger_type[line[1]](line[2])
            else:
                trigger = trigger_type[line[1]](created_triggers[line[2]], created_triggers[line[3]])
            created_triggers[line[0]] = trigger
        else:
            for e in line[1:]:
                triggers.append(created_triggers[e])
    return triggers

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
##        t1 = TitleTrigger("election")
##        t2 = DescriptionTrigger("Trump")
##        t3 = DescriptionTrigger("Clinton")
##        t4 = AndTrigger(t2, t3)
##        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

