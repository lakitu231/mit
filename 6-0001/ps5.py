# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
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

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
            
    def get_guid(self):
        return self.guid
        
    def get_title(self):
        return self.title
        
    def get_description(self):
        return self.description
        
    def get_link(self):
        return self.link
        
    def get_pubdate(self):
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
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
        
    def is_phrase_in(self, text):
        match_first = []
        
        # Remove punctuations from text and convert text into a list
        search_text = text.lower()
        for punc in string.punctuation:
            search_text = search_text.replace(punc, ' ')
        search_text = search_text.split()
        
        # Find matching consecutive words in phrase and text
        list_phrase = self.phrase.split()
        if list_phrase[0] in search_text:
            if len(list_phrase) == 1:
                return True
            for i in range(len(search_text)):
                if search_text[i] == list_phrase[0]:
                    match_first.append(' '.join(search_text[i:i + len(list_phrase)]))
            if self.phrase in match_first:
                return True
                
        return False


# Problem 3
class TitleTrigger(PhraseTrigger):    
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())
        
# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
    def __init__(self, pubdate):
        #self.pubdate =  datetime.strptime(pubdate, "%d %b %Y %H:%M:%S")

        try:
            self.pubdate = datetime.strptime(pubdate, "%d %b %Y %H:%M:%S")
            self.pubdate.replace(tzinfo=pytz.timezone("EST"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            self.pubdate = datetime.strptime(pubdate, "%d %b %Y %H:%M:%S")


# Problem 6
        
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        try:
            return story.get_pubdate() < self.pubdate
        except TypeError:
            return story.get_pubdate() < self.pubdate.replace(tzinfo=pytz.timezone("EST"))

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        try:
            return story.get_pubdate() > self.pubdate
        except TypeError:
            return story.get_pubdate() > self.pubdate.replace(tzinfo=pytz.timezone("EST"))
        
        
# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, trigg1, trigg2):
        self.trigg1 = trigg1
        self.trigg2 = trigg2
        
    def evaluate(self, story):
        return self.trigg1.evaluate(story) and self.trigg2.evaluate(story)


# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigg1, trigg2):
        self.trigg1 = trigg1
        self.trigg2 = trigg2
        
    def evaluate(self, story):
        return self.trigg1.evaluate(story) or self.trigg2.evaluate(story)



#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    
    triggered_stories = []
   
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) and story not in triggered_stories:
                triggered_stories.append(story)
        
    return triggered_stories


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
    
    trigg_list = []
    trigg_names = {}
    
    trigg_types = {'TITLE': TitleTrigger,
                   'DESCRIPTION': DescriptionTrigger,
                   'AFTER': AfterTrigger,
                   'BEFORE': BeforeTrigger,
                   'NOT': NotTrigger,
                   'AND': AndTrigger,
                   'OR': OrTrigger}
    
    single_triggers = ['TITLE', 'DESCRIPTION', 'AFTER', 'BEFORE', 'NOT']
    composite_triggers = ['AND', 'OR']
    
    for line in lines:
        args = line.split(',')
        
        if args[1] in single_triggers:
            trigg_names[args[0]] = trigg_types[args[1]](args[2])
            
        if args[1] in composite_triggers:
            trigg_names[args[0]] = trigg_types[args[1]](trigg_names[args[2]], trigg_names[args[3]])
        
        if args[0] == 'ADD':
            for name in args[1:]:
                trigg_list.append(trigg_names[name])
    
    # print(lines) # for now, print it so you see what it contains!
    
    return trigg_list



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("election")
        # t2 = DescriptionTrigger("Trump")
        # t3 = DescriptionTrigger("Clinton")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

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

            # Yahoo news gives AttributeError: object has no attribute 'description'
            # # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

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
