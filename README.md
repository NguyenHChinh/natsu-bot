# Natsu Discord Bot

Natsu's goal is to incorporate a wide range of features, such as quality-of-life Discord administrative tools, anime-related social commands, and niche game tools. Natsu is written using Discord.py and uses mySQL for its database. The bot uses Discord.py to implement functionality with Discord.


<br/><br/>

## Discord Tools

### coinflip.py

    A for-fun cog that allows user to virtually flip a coin

`coinflip` - outputs either "Heads" or "Tails" at random

### delete_msgs.py

    A discord administrative tool that allows a user marked as "admin" to delete _n_ messages prior to the command. The admin is prompted with a confirmation message with a checkmark reaction to confirm deletion.

`delete n` - deletes _n_ messages prior to the command

### essential.py

    A file used as a template for new cog files with basic features

`ping` - outputs "Pong!"

`amiadmin` - outputs "Yes, you are set as admin." if user id is same as admin id in config

### goodbye.py

    A discord administrative funnction where the bot sends a message to a designated channel per discord guild when a user from said guild leaves.

<br></br>

## Karuta Tools

### starboard.py

    A niche tool for the Discord card game __Karuta__. When a user reacts to a drop message with "⭐", it will take the image of the cards that are dropped and post them in a specified channel, as well as an embed that includes the original message content, a link to the message, the user who starred it, and the time the message got marked with "⭐". 

### karuta_valentines.py

    A niche tool for the Discord card game __Karuta__. Around Valentines, a limited-time event occurs where card drops have a chance of including one of four flowers: sunflower, rose, blossom, or tulip. The event encourages picking up flowers of each specific user's specialized type (determined at start of event). As such, when the bot detects that a flower has dropped, it will mention a role corrleated for each flower type.

In other words, if there are the roles "Sunflower", "Rose", "Blossom", and "Tulip" and a rose is detected within a drop, it will mention the role "Rose"

### karuta_wrongchannel.py

    A niche tool for the Discord card game __Karuta__. When any user uses a karuta command in a channel that is marked as part of this feature, it will notify the user that they're in the wrong channel, as well as a funny remark stating how many times they have done so before. These values are stored in counts.json. Afterwards, the user's original message, Karuta's reply message, and the bot's message are all deleted. 

<br></br>

## Anime and Manga Tools

### myanimelist.py

    Anime-related tools that works with the MyAnimeList API

`search <string>` - outputs link to MyAnimeList to anime retrieved from search

`setmal <string>` - sets user's ID to the string passed in, stored in mySQL database

`getmal` - retrieves string correlated to user who executed command

`mylist` - outputs an embed of animes from stored user's Anime List on MyAnimeList

<br></br>

## Video Game Tools

### lostark.py

    A niche tool that calculates the profitability and statistics of crafting certain materials in the Korean MMORPG video game __Lost Ark__. It utilizes the public API offered by lostarkmarket.online to retrieve the prices of market items in real time. 

`oreha <cost reduction> <time reduction>` - outputs an embed of statistics when crafting for both Basic Oreha Fusion Material and Superior Oreha Fusion Material, automatically retrieves prices of crafting ingredients from LostArkMarket API

`manual <cost of basic oreha> <cost of fish> <cost of natural pearl> <cost of oreha solar carp> <cost superior oreha> <cost reduction> <time reduction>` - outputs an embed of statistics when crafting for both Oreha Fusion Material and Superior Oreha Fusion Material, allows users to manually input price for each crafting ingredient

<br/><br/>

# TO-DO (in no particular order)

- karuta_valentines.py: add the ability to manage roles via command
- karuta_wrongchannel.py: add the ability to manage what channels have the feature enabled