---------------Get Streamer Statistics READ ME--------------\n
ABOUT:
This projext was to understand the relationship from viewers displayed at the bottom of the streamer Vs Users in chat, but I leared I could get more information from a streamer.
This scipt will automatically get statistics from twitch.tv about a specifc streamer. The information includes: Streamer Name, Game, Followers, Viewers, Users In Chat. This File also creates a simple log file with given statistics, detail log of entire process, create and update an excel file with statsistics for specific streamer, and add own Streamer Name in "Streamers.txt"

HOW TO:
First, create a txt file name "Streamers" exaclty without Quotes (has to be txtfile)
In the "Streamers" Txt File input the Streamer name exactly from witch Url ex (https://www.twitch.tv/roflgator);roflgator, followed by newLine for each new streamer(Remove any "Blank" newLines after a new streamer)
Next, run the GetTwitchStatistics.bat, this will run the python script directly
A command prompt will be displayed with what processes are going on.
A file called "bob" will be created and updated, this will show a simple format for given statistics for Name, Game, Followers, Viewers, Date & Time, Twitch's Users In Chat.
A file called "LogFile" will be created, and updated, with detail infomration for each process while runing the script.
For each streamer that is in "Streamers" txt file, an Excel file and updated with that streamer statistics. (DO NOT KEEP EXCEL FILE OPEN WHEN SCRIPT IS RUNNING, WILL CRASH)
