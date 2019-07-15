#--------------IEX Finance Config ------
iex_auth_token = "[IEX AUTH TOKEN HERE]"

#--------------Reddit Configs-----------
target_subreddit = "testingground4bots"

# -------------Bot Configs--------------
bot = "bot1"
bot_signature = "^(I am a bot, and this action was performed automatically.)"
time_between_loops = 100 # The number of seconds the program sleeps before checking posts again.
post_samples = 5 # The number of posts the program will check comments for.
comment_reply_skeleton = "-----------------------\n\n{name} ({tag}): \n\nCurrent Price: {cp}\n\nYear to Date: {ytd}\n\n-----------------------"


#-------------File Configs-------------
alpha_locale_document = "data/alpha_locale.txt" # File which indexes NASDAQ file.
comments = "data/comments_replied_to.txt" # File location for parent comments.
stock_selection = "data/nasdaq.csv" # File which stores ticker selections.