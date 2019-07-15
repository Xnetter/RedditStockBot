import praw
import re
from stocks import Stocks
from settings import *
import os
import csv
import time
from rebuild import rebuild_alpha_sheet


def parseForTagCommand(comment_body): #parses comments for stock tickers preceded by a ! ex: !BKS
	tags = re.findall(r'(?<=\s!)[A-Z]{1,5}(?=[\s\W])', comment_body) #regular expression for finding stock and ignoring false data
	tags_chunked = comment_body.split() #Regex can't find first string and last string because they do not have whitespace or characters on both sides.
	first = ""
	last = ""
	if(tags_chunked): #Checks the first and last "Word" in the comment, if they exist
		last = tags_chunked.pop()
		if(last[0] == '!' and last.isupper() and (len(last) < 6 and len(last) >0) and last[1:].isalpha()):
			tags.append(last[1:])
		if(tags_chunked):
			first = tags_chunked.pop(0)
			if(first[0] == '!' and first.isupper() and (len(first) < 6 and len(first) >0) and first[1:].isalpha()):
				tags.append(first[1:])
	return tags


def main(): 
	while(True):
		#Creates an alpha reference sheet if none exists
		#(Alphabetizes the search query for speed)
		#This can be done manually by running rebuild.py
		char = "A"
		if not os.path.isfile(alpha_locale_document): #check if the file exists
			rebuild_alpha_sheet(char)	
		#Logs comments already replied to
		if not os.path.isfile(comments):
			comments_replied_to = [] #first time running bot
		else: 
			with open(comments, "r") as c_file:
				comments_replied_to = c_file.read() #read the comments that have been already replied to
				comments_replied_to = comments_replied_to.split("\n")
				comments_replied_to = list(filter(None, comments_replied_to))
		parse_and_reply(comments_replied_to)

		time.sleep(time_between_loops)


def parse_and_reply(comments_replied_to):
	reddit = praw.Reddit(bot) 
	r_target = reddit.subreddit(target_subreddit)
	r_all = reddit.subreddit("all")
	for submission in r_target.hot(limit = post_samples):#iterates through posts in hot, top, new, etc.
		print(submission.title)
		submission.comments.replace_more(limit=None) #resolves all "more comments" so all comments are checked.
		for comment in submission.comments.list(): #Check every comment on the post
				if comment.id not in comments_replied_to: #If we haven't replied to this comment
					currentTags = list(set(parseForTagCommand(comment.body)))#find tags and remove duplicate tags in comment
					stockObjects = []
					for tag in currentTags:
						stock = Stocks(tag)
						if stock.name: #Stock only exists if it has a name
							stockObjects.append(stock)
					reply = ""#allows for the postage of several stocks on one comment
					for st in stockObjects:
						#REPLY TO COMMENT
						reply += comment_reply_skeleton.format(
							tag = st.tag,
							name = st.name,
							cp = st.price,
							# headline = st.headline,
							# op = st.open,
							# cl = st.close,
							# yh = st.year_high,
							# yl = st.year_low,
							# url = st.headline_hyper,
							ytd = st.year_change)+"\n\n"
					if(len(reply)>0):#if there are stock objects, and reply exists
						my_reply = comment.reply(reply + bot_signature)
						comments_replied_to.append(my_reply.id)#Ensure that the program does not reply to itself
						print("Replying to... " + comment.body)#Command prompt
						comments_replied_to.append(comment.id)
		with open(comments, "w") as c_file:
			for comment_id in comments_replied_to:
				c_file.write(comment_id + "\n")#Log comments replied to


if __name__ == "__main__":
	main()