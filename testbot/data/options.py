"""
Settings and options for the bot.
---
"""

# The prefix for the bot (str). Define a list of stings for multiple prefixes.
# ie: `["?", "!", "pls "]`
prefix = ["?", "? ", "pls "]

# The prefix to use for display purposes (ex: status message).
display_prefix = "?"

# Whether the bot should print full stacktraces for normal exceptions: `True`,
# or be nice and only print small messages: `False` (the default).
debug = False

# A tuple of user IDs that should be considered "bot owners".
# * Those users will have full control over the bot.
# ! This MUST be a tuple of integers. Single element tuple: `(123,)`
owners_uids = (200102491231092736,)

# The extensions to load when running the bot.
exts = ['ae7q', 'base', 'fun', 'grid', 'ham', 'image', 'morse', 'qrz', 'study', 'weather', 'dbconv']

# Either "time", "random", or "fixed" (first item in statuses)
status_mode = "time"

# Random statuses pool
statuses = ["with lids on the air", "with fire"]

# Timezone for the status (string)
status_tz = 'US/Eastern'
# The text to put in the "playing" status, with start and stop times
time_statuses = [('with lids on 3.840', (00, 00), (6, 00)),
                 ('with lids on 7.200', (6, 00), (10, 00)),
                 ('with lids on 14.313', (10, 00), (18, 00)),
                 ('with lids on 7.200', (18, 00), (20, 00)),
                 ('with lids on 3.840', (20, 00), (23, 59))]

# append " | {display_prefix}help" to the Discord playing status
show_help = True

# Emoji IDs and keywords for emoji reactions
# Use the format {emoji_id (int): ('tuple', 'of', 'lowercase', 'keywords')}
msg_reacts = {473524356270522369: ('uwu',),
              584170691369107456: ('owo', '0w0'),
              658699411425329192: ('xd',)}

# A :pika: emote's ID, None for no emote :c
pika = 658733876176355338
