# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 17:53:39 2022

@author: -
"""

import requests
import MySQLdb

# Connect to MySQL57 Database
connection = MySQLdb.connect(host="localhost",user="Peseiden",password='DBAdminPassword11!!',db='census_ability')
cursor = connection.cursor()


# Variables
class_list = ['Berserker','Guardian','Bruiser','Monk','Paladin','Shadowknight',
              'Warlock','Wizard','Coercer','Illusionist','Conjuror','Necromancer',
              'Fury','Warden','Inquisitor','Templar','Defiler','Mystic',
              'Dirge','Troubador','Assassin','Ranger','Brigand','Swashbuckler',
              'Channeler','Beastlord']
# Loop through the 26 classes
for i in range(len(class_list)):
    # Query to send to MySQL57
    sqltwo= "INSERT IGNORE INTO ability_list_all(class,alternate_advancement,aoe_radius_meters,beneficial,cast_secs_hundredths,"\
    "chardiff,classes,cost,crc,deity,description,given_by,id,last_update,level,"\
    "max_targets,name,name_lower,recast_secs,recovery_secs_tenths,spellbook,target_type,tier,tier_name,ts,type,typeid)"\
    "VALUES"\
    f"('{class_list[i]}',%(alternate_advancement)s,%(aoe_radius_meters)s,%(beneficial)s,%(cast_secs_hundredths)s,"\
    "%(chardiff)s,%(classes)s,%(cost)s,%(crc)s,%(deity)s,%(description)s,%(given_by)s,%(id)s,%(last_update)s,%(level)s,"\
    "%(max_targets)s,%(name)s,%(name_lower)s,%(recast_secs)s,%(recovery_secs_tenths)s,%(spellbook)s,%(target_type)s,%(tier)s,%(tier_name)s,%(ts)s,%(type)s,%(typeid)s)"
    
    # Url
    ability_url = f"https://census.daybreakgames.com/s:turtlepunt05/json/get/eq2/spell/?level=[50&tier_name=Master&classes.{class_list[i].lower()}.displayname={class_list[i]}"\
                                  "&c:show=alternate_advancement,aoe_radius_meters,beneficial,cast_secs_hundredths,"\
                                  "chardiff,classes,cost,crc,deity,description,effect_list,given_by,id,last_update,level,"\
                                  "max_targets,name,name_lower,recast_secs,recovery_secs_tenths,spellbook,target_type,tier,tier_name,ts,type,typeid,description&c:limit=2000"
    ability_list = requests.get(ability_url)
    nl_dal = ability_list.json()
    nl_dal_list = nl_dal.get('spell_list')

    cursor.executemany(sqltwo, nl_dal_list)
    connection.commit()

    nl_el_effect = []
    sqlthree = "INSERT IGNORE INTO ability_effect(class,name,description,indentation) VALUES (%(class)s,%(name)s,%(description)s,%(indentation)s)"
    j = 0
    for j in range(len(nl_dal_list)):
        nl_el = dict()
        nl_el = nl_dal_list[j]
        nl_el_name = nl_el['name']
        nl_el_class = class_list[i]
        if 'effect_list' in nl_el:
            nl_el_effect = []
            nl_el_effect = nl_el['effect_list']
            k = 0
            for k in range(len(nl_el_effect)):
                nl_el_key = dict()
                nl_el_key = nl_el_effect[k]
                nl_el_key['name'] = nl_el_name
                nl_el_key['class'] = nl_el_class
                nl_el_effect[k] = nl_el_key
            cursor.executemany(sqlthree, nl_el_effect)
            connection.commit()