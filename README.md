# MMO-Enhancement-Scripts
AbilityList
  Taps into the EverQuestII api to gather ability lists for all classes to be used in analysis for raids

BrokerTrendsSSP
  Takes and stores snapshots of price and quantity of chosen items being sold on the broker. The script uses OpenCV to process the images and then uses pytesseract to extract the price and quantity text from the processed    
  image. It then stores this in a new line separated with newlines.

CurrencyConvert
  Companion script to BrokerTrendsSSP. This script splits the price string out into separate currencies such as platinum, gold, silver, and copper values. 

InGameChat
  EverQuestII logs most actions in game to a .txt file. The log dump latency is about every one or two seconds. This script opens the .txt file and reads the file from the end up to where the .txt file previously ended before the new dump. It then sends the chat log data to a Discord server. Depending on what type of log it is it then gets separated into different channels which allows for ingame chat to be streamed with little latency to Discord.
