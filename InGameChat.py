# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 23:55:10 2022

@author: jucoe
"""

import nextcord
from nextcord import Interaction
from nextcord.ext import commands, tasks
import nest_asyncio
import os
import re

nest_asyncio.apply()

files = [r"C:\Users\Public\Daybreak Game Company\Installed Games\EverQuest II\logs\Varsoon\eq2log_Athina.txt"]
testingServerID = '1023026112089051156'

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = '!', intents = intents)



@tasks.loop(hours=24)
async def my_task_loop():
  print('Bot ready baby!')
  leftover_channel = client.get_channel(1023026112089051159)
  guild_channel = client.get_channel(1024403962696323112)
  general_channel = client.get_channel(1024409039431553126)
  lfg_channel = client.get_channel(1024409243459264583)
  auction_channel = client.get_channel(1024409082821611602)
  group_channel = client.get_channel(1024419561963016262)
  guild_event_channel = client.get_channel(1024536266731175996)
  for f in files:
      #Grab last line in log, run this before the loop
      with open(f, 'rb') as myfile:
          try:  # catch OSError in case of a one line file 
              myfile.seek(-2, os.SEEK_END)
              while myfile.read(1) != b'\n':
                  myfile.seek(-2, os.SEEK_CUR)
          except OSError:
              myfile.seek(0)
          last_line = myfile.readline().rstrip()
          myfile.close()
      
      #sleep(10)
      # # Grabs only updated logs up to last_line    
      #last_n_lines_append = []
      z = 0
      while z == 0:
          m = 0
          current_line = ''
          with open(f, 'rb') as myfile:
             #print(z)
             try:
                 myfile.seek(-1, os.SEEK_END)
                 last_pos = myfile.tell()
                 #current_line = myfile.readline().docode()
                 while current_line != last_line:
                    myfile.seek(last_pos)
                    myfile.seek(-1, os.SEEK_CUR)
                    last_pos = myfile.tell()
                    if myfile.read(1) == b'\n':
                        current_line = myfile.readline().rstrip()
                        #last_n_lines_append.append(current_line)
                        m += 1
             except OSError:
                 myfile.seek(0)
             updated_lines = myfile.readlines()
             if m == 1:
                 continue
             else:
                 last_line = updated_lines[m-2].rstrip()
                 for x in range(len(updated_lines)):
                     # More effecient, but needs fixed Regex method to pull guild chat that isn't from yourself

                     # Guild chat, not self
                     if re.match(r"^.+\[.+\].+:.+\\.*says to the guild, ?\".+\"",updated_lines[x].rstrip().decode()):
                         #r"^.+\[(.+)\].+:(.+\\).+ says to the guild, ?(\".+\")" 
                         guild_chat_clean = re.findall(r"^.+\[(.+)\].+:(.+)\\.*says to the guild, ?\"(.+)\"",updated_lines[x].rstrip().decode())
                         guild_chat_clean_con = ' '.join(map(str,guild_chat_clean))
                         await guild_channel.send(guild_chat_clean_con)
                     # Guild chat, self
                     elif re.match(r"^.+\[.+\] You say to the guild, ?\".+\"",updated_lines[x].rstrip().decode()):
                         #r"^.+\[(.+)\].+:(.+\\).+ says to the guild, ?(\".+\")" 
                         guild_chat_self_clean = re.findall(r"^.+\[(.+)\] (You) say to the guild, ?\"(.+)\"",updated_lines[x].rstrip().decode())
                         guild_chat_self_clean_con = ' '.join(map(str,guild_chat_self_clean))
                         await guild_channel.send(guild_chat_self_clean_con)
                         
                     # Group chat, not self
                     elif re.match(r"^.+\[.+\].*:.+\\.*says to the group, ?\".+\"",updated_lines[x].rstrip().decode()):
                         group_chat_clean = re.findall(r"^.+\[(.+)\] .*:(.+)\\.*says to the group, ?\"(.+)\"",updated_lines[x].rstrip().decode())
                         group_chat_clean_con = ' '.join(map(str,group_chat_clean))
                         #r"^.+\[(.+)\].+:(.+\\).+ says to the guild, ?(\".+\")"
                         await group_channel.send(group_chat_clean_con)
                     # Group chat, self
                     elif re.match(r"^.+\[.+\] You say to the group, ?\".+\"",updated_lines[x].rstrip().decode()):
                         group_chat_self_clean = re.findall(r"^.+\[(.+)\] (You) say to the group, ?\"(.+)\"",updated_lines[x].rstrip().decode())
                         group_chat_self_clean_con = ' '.join(map(str,group_chat_self_clean))
                         #r"^.+\[(.+)\].+:(.+\\).+ says to the guild, ?(\".+\")"
                         await group_channel.send(group_chat_self_clean_con)
                         
                     # General chat, not self
                     elif re.match(r"^.+\[.+\].*:.+\\.*tells General \(\d\), ?\".+\"",updated_lines[x].rstrip().decode()):
                         general_chat_clean = re.findall(r"^.+\[(.+)\].*:(.+)\\.*tells General \(\d\), ?\"(.+)\"",updated_lines[x].rstrip().decode())
                         general_chat_clean_con = ' '.join(map(str,general_chat_clean))
                         await general_channel.send(general_chat_clean_con)
                     # General chat, self
                     elif re.match(r"^.+\[.+\] You tell General \(\d\), ?\".+\"",updated_lines[x].rstrip().decode()):
                         general_chat_self_clean = re.findall(r"^.+\[(.+)\] (You) tell General \(\d\), ?\"(.+)\"",updated_lines[x].rstrip().decode())
                         general_chat_self_clean_con = ' '.join(map(str,general_chat_self_clean))
                         await general_channel.send(general_chat_self_clean_con)
                       
                     # LFG, not self
                     elif re.match(r"^.+\[.+\].*:.+\\.*tells LFG ?\(\d*\), ?\".+\"",updated_lines[x].rstrip().decode()):
                         lfg_chat_clean = re.findall(r"^.+\[(.+)\].*:(.+)\\.*tells LFG ?\(\d*\), ?\"(.+)\"",updated_lines[x].rstrip().decode())
                         lfg_chat_clean_con = ' '.join(map(str,lfg_chat_clean))
                         await lfg_channel.send(lfg_chat_clean_con)
                     # LFG, self
                     elif re.match(r"^.+\[.+\] You tell LFG ?\(\d*\), ?\".+\"",updated_lines[x].rstrip().decode()):
                         lfg_chat_self_clean = re.findall(r"^.+\[(.+)\] (You) tells LFG ?\(\d*\), ?\"(.+)\"",updated_lines[x].rstrip().decode())
                         lfg_chat_self_clean_con = ' '.join(map(str,lfg_chat_self_clean))
                         await lfg_channel.send(lfg_chat_self_clean_con)
                         
                     # Auction, not self
                     elif re.match(r"^.+\[.+\].*:.+\\.*auctions, ?\".+\"",updated_lines[x].rstrip().decode()):
                         auction_chat_clean = re.findall(r"^.+\[(.+)\].*:(.+)\\.*auctions, ?\"(.+)\"",updated_lines[x].rstrip().decode())
                         auction_chat_clean_con = ' '.join(map(str,auction_chat_clean))
                         await auction_channel.send(auction_chat_clean_con)
                     # Auction, self
                     elif re.match(r"^.+\[.+\] You auction, ?\".+\"",updated_lines[x].rstrip().decode()):
                         auction_chat_self_clean = re.findall(r"^.+\[(.+)\] (You) auction, ?\"(.+)\"",updated_lines[x].rstrip().decode())
                         auction_chat_self_clean_con = ' '.join(map(str,auction_chat_self_clean))
                         await auction_channel.send(auction_chat_self_clean_con)
                         
                     # Guild Events
                     elif re.match(r"^.+\[.+\] Guildmate: .+ has logged .+",updated_lines[x].rstrip().decode()):
                         guild_event_chat_self_clean = re.findall(r"^.+\[(.+)\] (Guildmate: .+ has logged .+)",updated_lines[x].rstrip().decode())
                         guild_event_chat_self_clean_con = ' '.join(map(str,guild_event_chat_self_clean))
                         await guild_event_channel.send(guild_event_chat_self_clean_con)
                     elif re.match(r"^.+\[.+\] .+ earned the achievement.+",updated_lines[x].rstrip().decode()):
                         guild_event_chat_self_clean = re.findall(r"^.+\[.+\] (.+ earned the achievement.+)",updated_lines[x].rstrip().decode())
                         guild_event_chat_self_clean_con = ' '.join(map(str,guild_event_chat_self_clean))
                         await guild_event_channel.send(guild_event_chat_self_clean_con)
                     
                     else:
                         continue
                     #print(updated_lines)
          myfile.close()
          
@my_task_loop.before_loop
async def before_my_task_loop():
    print('Waiting for ready')
    await client.wait_until_ready()
    
    
    
my_task_loop.start()
    
client.run('MTAyMzA2OTE0NTM2Mjg3ODQ4NA.GabCjR.EeObrOUDA1UGXx1N4ses2-h9nOaVgJ2xQi2V2c')