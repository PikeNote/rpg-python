from __future__ import print_function
import builtins as __builtin__
inventory = {"weapons":[],"items":[],"armor":[]}
directions = ['north','west','east','south']
location = 'Hall'
health = 100
coins = 100
mobsKilled = []
equipped_weapon="None"
equipped_armor="None"
quest = []

newMap = """
                                +---+
         +----------------------+ S +------------------+
         |                      +-+-+                  |
         |                        |                    |
       +-+-+    +---+    +---+  +-+-+  +---+  +---+  +-+-+   +---+
       | Sr+----+ P +----+ B +--+ H +--+ Br+--+ Lb+--+ H +---+ A |
       +-+-+    +---+    +---+  +-+-+  +---+  +-+-+  +-+-+   +---+
         |                        |             |      |
+---+  +-+-+                    +-+-+  +---+    |    +-+-+   +---+
|Pr +--+ L +-------------------+ Lr +--+ Mr +----+   | H +---+ B |
+---+  +-+-+                    +-+-+  +---+         +-+-+   +---+
         |                        |                    |
       +-+-+     +---+   +---+  +-+-+  +---+  +---+  +-+-+   +---+
       | Ba|     | O +---+ F +--+ H +--+ D |  | D +--+ H +---+ B |
       +---+     +---+   +---+  +-+-+  +---+  +---+  +---+   +---+
                                  |
                         +---+  +-+-+  +---+  +---+
                         | V +--+ B +--+ S +--+ O |
                         +---+  +-+-+  +---+  +---+
                                  |
                                +-+-+
                                | Br|
                                +---+	

* = Player               Lr = Library               P = Secret Passage
H = Hall                 Mr = Master Bedroom        
S = Shop                 Br = Bathroom 
Pr = Parlor              D = Dungeon
B = Bedroom              Lb = Lab
O = Outside              Sr = Study Room
S = Storage Room         Ba = Basement
V = Baldwin's Vault      A = Armory
"""

errMsg = False
import random
import replit
import json
import requests
import sys, select
import math 
from time import sleep
import traceback
import re

def replacenth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return newString

def print(args, **kwargs):
  return newPrint(args)

def newPrint(word):
  if ("	" in word):
    __builtin__.print(word)
  else:
    for char in word:
      sleep(0.025)
      sys.stdout.write(char)
      sys.stdout.flush()

wordsFile = open("words.json", 'r')
wordData= wordsFile.read()

getList = requests.get('https://raw.githubusercontent.com/words/an-array-of-english-words/master/words.json')
wordsList = json.loads(wordData)

wordsFile.close()

gameData = {

#when the user types a direction they go to a room in the hall
  "rooms":{


    "Hall":{
      "uniChar":'H', #that good?
      "mapCount":4,
      "north":"Library",
      "south":"Bedroom",
      "east":"Dungeon",
      "west":"Front Door"
    },
    #Going south when in the library takes you to the hall
    #Going North takes you to Hall 2
    "Library":{
      "uniChar":'Lr', 
      "mapCount":1,
      "south":"Hall",
      "north":"Hall #2",
      "east":"Master Bedroom",
      "west":"Living Room",
      #calls trigger to search
      "trigger":{
        "search":{
          #When the user types a number they get either nothing or Excalibur.
          "1":{
            "item":"nothing",
            "prompt":"You have found nothing in the book!"
          },
          "2":{
            "item":"Excalibur",
            "prompt":"You found a glowing key in one of the books.\nThe key seems to unlock a chest behind one of the bookshelves\nInside, you see a fancy sword.\n\n"
          },
          "3":{
            "item":"nothing",
            "prompt":"You have found nothing in the book!"
          }
        },
        "activated":'false',
        "prompt":"You step into a library with three seperate books.\nWhat book would you choose? \n(Enter an number between 1-3)\n"
      }
    },
    "Master Bedroom":{
      "uniChar":'Mr', 
      "mapCount":1,
      "west": "Library",
      "east":"Lab",
      "trigger":{
        "npc":"Adorable Puppy",
        "prompt":"You walk into a room, with a cute little puppy jumping on the bed.\n\nWould you like to interact with it?",
        "activated":"false"
      }
    },
    "Living Room":{
      "uniChar":'L', 
      "mapCount":1,
      "north":"Study Room",
      "south":"Basement",
      "east":"Library",
      "west":"Parlor"
    },
    "Basement":{
      "uniChar":'Ba', 
      "mapCount":1,
      "north":"Living Room",
      "trigger":{

      }
    },
    "Parlor":{
      "uniChar":'Pr', 
      "mapCount":1,
      "east":"Living Room",
      "south":"Someroom",
      "trigger":{
        "npc":"Lone Ghost",
        "prompt":"The parlor is creaky,abandoned,and chilly. \n You hear a faint woosh and moan.\n\nIt's a ghost! Do you dare talk to it? \n",
        "activated":"false"
      }
    },
    "Study Room":{
      "uniChar":'Sr', 
      "mapCount":1,
      "south":"Living Room",
      "west":"Study Room Passage",
      "north":"Shop",
      "trigger":{
        "prompt": "Entering the study room, you find a piano, ornately decorated and crafted with an elegant mahogany. Do you play it?",
        "activated":"false"
      }
    },

    "Lab":{
      "uniChar":'Lb',
      "mapCount":1,
      "south":"Master Bedroom",
      "east":"Hall #3",
      "west":"Bathroom #2",
      "trigger":{
        "activated":"false",
        "item":"Gooey Armor",
        "prompt2":"You look around the mysterious lab and you stumble upon a piece of gooey armor. It's squishy, but durable.\n",
        "prompt":"The hiss of chemicals and bubbling fills your ear as you enter the lab. Do you look around?"
      }
    },
    
    #Again, go in a certain direction and go to a certain room
    "Hall #2":{
      "uniChar":'H', 
      "mapCount":1,
      "west":"Bedroom #2",
      "east":"Bathroom #2",
      "north":"Shop",
      "south":"Library",
      "trigger":{
        "item":"Mysterious Pendant"
      }
    },
    "Front Door":{
      "uniChar":'F', 
      "mapCount":1,
      "east":"Hall",
      "west":"Outside",
      "trigger":{
        "activated":"false",
        "traps":["Spike Trap","Dart Trap", "Incinerator"],
        "prompt":"You walk up to a ominous front door of the building.\nThere is a button that appears to open the door.\nWill you press it?\n"
      }
    },
    #Certain direction, certain room.
    "Bedroom":{
      "uniChar":'B', 
      "mapCount":4,
      "north":"Hall",
      "south":"Bathroom",
      "east":"Storage Room",
      "west": "Baldwin's Vault",
      "trigger":{
        "activated":"false",
        "item":"Steel Armor",
        "prompt2":"You carefully look around the bedroom and you stumble upon a piece of iron armor. It seems like it is pretty sturdy..\n",
        "prompt":"You open the door and set your eyes on a seemingly calm bedroom. \nDo you want to look around?\n\n",
        "activated":"false"
      }
    },
    "Baldwin's Vault":{
      "uniChar":'V', 
      "mapCount":1,
      "east":"Bedroom",
      "trigger":{
        "npc":"Baldwin the Hairless",
        "prompt":"You walk into a shiny room and you see a guy who looks like Mr.Clean in the corner.\n\nWould you like to chat?\n",
        "activated":"false"
      }
    },
    "Bedroom #4":{
      "uniChar":'B', 
      "mapCount":3,
      "west":"Hall #5",
      "trigger":{
        "npc":"Old Woman",
        "prompt":"You walk into a bedroom with an old lady sitting by the bedside, seemingly just staring in to the void..\n",
        "activated":"false"
      }
    },
    "Storage Room":{
      "uniChar":'S', 
      "mapCount":1,
      "west":"Bedroom",
      "east":"Outside",
      "trigger":{
        "activated":"false",
        "prompt": "You think you see a faint glimmering in the storeroom. It could be dangerous, but it could also be a grand reward. \nDo you take your chances?\n\n",
    
        "item":"Staff of Lightning",

        "prompt2":"You receive the Staff of Lightning!",
      }
     },
    "Bathroom":{
      "uniChar":'Br', 
      "mapCount":1,
      "north":"Bedroom",
      "trigger":{
        "item": "Toilet Knuckles",
        "prompt2":"Reluctantly reaching your hand into the toilet, you find a pair of ornate brass knuckles.",
        "prompt":"You think there's an item in the toilet bowl but...do you really want to reach in there?th?\n\n",
        "activated":"false"
      }
    },
    "Outside":{
      "uniChar":'O', 
      "mapCount":1,
      "trigger":{
        "prompt":"The outside! You think you've made it! Finally, an escape from this tortorous place.\nHowever...a sinking, uneasy feeling fills your heart.\nAre you sure you want to leave?",
      }
     },
    "Bedroom #2":{
      "uniChar":'B', 
      "mapCount":1,
      "east":"Hall #2",
      "west":"Study Room Passage",
      "trigger":{
        "item": "Apple",
        "prompt2":"You carefully look around the bedroom and you stumble upon an apple on the nightstand.",
        "prompt":"You open the door and set your eyes on a seemingly calm bedroom. \nDo you want to look around?\n\n",
        "activated":"false"
      }
    },
    "Dungeon #2":{
      "uniChar":'D', 
      "mapCount":2,
      "east":"Hall #5",
      "trigger":{
        "mob":"A mob turns around and slowly walks towards you.\nWould you like to run?\n\n",
        "prompt": "\n\nYou slowly creep into the dungeon as you hear faint sounds of screams screeching louder and louder.\n\n",
        "triggeredCount":0
      },
      # Mob health, lootables, stats
      "mob":{
        "Cyclops":{
          "health":130,
          "attack":15,
          "name":"Cyclops",
          "lootPool":["Steel Armor", "Wooden Club With Spikes", "Heal Pot","Full Restore"],
          "gold":45
        },
        "Gremlin":{
          "health":80,
          "attack":13,
          "name":"Gremlin",
          "lootPool":["Leather Armor", "Wooden Club With Spikes", "Wooden Pole","Apple"],
          "gold":45
        },
        "Warlock":{
          "health":100,
          "attack":15,
          "name":"Warlock",
          "lootPool":["Steel Armor", "Golden Apple", "Wooden Pole","Potion of Healing"],
          "gold":45
        },
        "Elemental Spirit":{
          "health":50,
          "attack":30,
          "name":"Elemental Spirit",
          "lootPool":["Platinum Armor", "Golden Apple", "Heal Pot","Full Restore"],
          "gold":20
        },
        "Slime":{
          "health":50,
          "attack":8,
          "name":"Slime",
          "lootPool":["Leather Armor", "Apple", "Heal Pot","Broken Glass Bottle","Wooden Pole"],
          "gold":20
        },
        "Giant Worm":{
          "health":145,
          "attack":15,
          "name":"Giant Worm",
          "lootPool":["Steel Armor", "Steel Sword","Wooden Pole","Wormy Sword", "Heal Pot","Full Restore"],
          "gold":50
        },
        "Rabid Hound":{
          "health":120,
          "attack":12,
          "name":"Rabid Hound",
          "lootPool":["Apple", "Wooden Pole", "Pots and Pans", "Broken Glass Bottle"],
          "gold":35
        },
        "Ninja":{
          "health":100,
          "attack":10,
          "name":"Ninja",
          "lootPool":["Heal Pot", "Dagger","Lether Armor"],
          "gold":20
        }
      },

    },
    "Bathroom #2":{
      "uniChar":'Br', 
      "mapCount":1,
      "west":"Hall #2",
      "east":"Lab",
      "item": "Mop",
        "prompt2":"You found a mop! It's beyond you who would've left it in a bathroom.",
        "prompt":"Oh, what's this? \nThere seems to be a long, skinny thing lying behind the curtain. \nDo you open them and see what it is?",
        "activated":"false"
    },

    "Study Room Passage":{
      "uniChar":'P', 
      "mapCount":1,
      "west":"Study Room",
      "east":"Bedroom #2"
    },
    
    "Shop":{
      "uniChar":'S', 
      "mapCount":1,
      "south":"Hall #2",
      "east":"Hall #3",
      "west":"Study Room",
      #costs of items defined
      "trigger":{
        "items":{
          "Excalibur":50,
          "Steel Armor":20,
          "Apple":3,
          "Heal Pot":7,
          "Broken Glass Bottle":3,
          "Platinum Armor": 40,
          "Leather Armor":5
        },
        "prompt":"You have arrived in the shop"
      }
    },
    "Hall #3":{
      "uniChar":'H', 
      "north":"Shop",
      "mapCount":2,
      "west":"Lab",
      "south":"Hall #4",
      "east":"Armory",
      "item": "Koolaid",
        "prompt2":"You found the Koolaid! Still, what could that odd noise have been?",
        "prompt":"There's a groaning sound emenating from behind the thin walls. \nIf it were to be a mob, it could kill you nigh instantly because of how cramped it is. \nDo you take your chances?",
        "activated":"false"
    },
    "Bedroom #3":{
      "uniChar":'B', 
      "west":"Hall #4",
      "mapCount":2,
      "trigger":{
        "npc":"Skeleton",
        "prompt":"A skeleton sits on the bed of the dark bedroom, yelling loudly about how he's missing something and wants it back. \nYou silently feel bad for the mobs which probably have to deal with him. \nDo you speak to the skeleton?",
        "activated":"false"
      }
    },
    "Armory":{
      "uniChar":'A', 
      "west":"Hall #3",
      "mapCount":1,
      "item":"Rapier",
      "prompt2":"You pick up a rapier from the floor that you're sure wasn't there before. Pointy, springy, and great for fighting! But just thinking of that armor gives you the creeps.",
        "prompt":"The sound of metal scraping fills the room. \nYou see a suit of armor doing an odd pose, and you think it wasn't doing it a second ago. \nDo you approach it?",
        "activated":"false"
    },

    "Hall #4":{
      "uniChar":'H', 
      "north":"Hall #3",
      "south":"Hall #5",
      "east":"Bedroom #3",
      "mapCount":3,
      "trigger":{
        "activated":"false",
        "traps":["Magic Trap","Poison Trap", "Lightning Trap"],
        "prompt":"A shining, extraordinarily sharp sword lays on a table in the hallway.\nIt seems to be calling your name.\nWill you take it?\n"
       
      }
    },

    "Hall #5":{
      "uniChar":'H', 
      "north":"Hall #4",
      "mapCount":5,
      "east":"Bedroom #4",
      "west":"Dungeon #2",
      "trigger":{
        "activated":"false",
        "traps":["Snare Trap","Trapdoor", "Falling Net"],
        "prompt":"You swear that one of the floorboards in this hallway looks off.\nIt's an off-white color compared to the dreary ash brown floors.\nCheck what lies underneath?\n"
      }
    },

    "Dungeon":{
      "uniChar":'D', 
      "mapCount":2,
      "trigger":{
        "mob":"A mob turns around and slowly walks towards you.\nWould you like to run?\n\n",
        "prompt": "\n\nYou slowly creep into the dungeon as you hear faint sounds of screams screeching louder and louder.\n\n",
        "triggeredCount":0
      },
      "west":"Hall",
      # Mob health, lootables, stats
      "mob":{
        "Cyclops":{
          "health":130,
          "attack":15,
          "name":"Cyclops",
          "lootPool":["Steel Armor", "Wooden Club With Spikes", "Heal Pot","Full Restore"],
          "gold":45
        },
        "Gremlin":{
          "health":80,
          "attack":13,
          "name":"Gremlin",
          "lootPool":["Leather Armor", "Wooden Club With Spikes", "Wooden Pole","Apple"],
          "gold":45
        },
        "Warlock":{
          "health":100,
          "attack":15,
          "name":"Warlock",
          "lootPool":["Steel Armor", "Golden Apple", "Wooden Pole","Potion of Healing"],
          "gold":45
        },
        "Elemental Spirit":{
          "health":50,
          "attack":30,
          "name":"Elemental Spirit",
          "lootPool":["Platinum Armor", "Golden Apple", "Heal Pot","Full Restore"],
          "gold":20
        },
        "Slime":{
          "health":50,
          "attack":8,
          "name":"Slime",
          "lootPool":["Leather Armor", "Apple", "Heal Pot","Broken Glass Bottle","Wooden Pole"],
          "gold":20
        },
        "Giant Worm":{
          "health":145,
          "attack":15,
          "name":"Giant Worm",
          "lootPool":["Steel Armor", "Steel Sword","Wooden Pole","Wormy Sword", "Heal Pot","Full Restore"],
          "gold":50
        },
        "Rabid Hound":{
          "health":120,
          "attack":12,
          "name":"Rabid Hound",
          "lootPool":["Apple", "Wooden Pole", "Pots and Pans", "Broken Glass Bottle"],
          "gold":35
        },
        "Ninja":{
          "health":100,
          "attack":10,
          "name":"Ninja",
          "lootPool":["Heal Pot", "Dagger","Lether Armor"],
          "gold":20
        }
      },
    },
  },
  "items":{
    "healing":{
      #Healing items that includes how much they heal
      "Heal Pot":{
        "health": 15
      },
      "Full Restore":{
        "health":100
      },
       "Potion of Healing":{
        "health":30
      },
       "Golden Apple":{
        "health":50
      },
      "Apple":{
        "health": 5
      },
      "Koolaid":{
        "health": 40
      }
    },
    "attack":{
      #Attacking items that includes how much damage they do
      "Excalibur":20,
      "Wooden Pole":5,
      "Hand":1,
      "Steel Sword":15,
      "Dagger":10,
      "Wormy Sword":12,
      "Toilet Knuckles": 10,
      "Baldwin's Dagger":15,
      "Broken Glass Bottle":5,
      "Wooden Club With Spikes":18,
      "Staff of Lightning": 17,
      "Skeletal Hand": 5,
      "Rapier":12,
      "Mop":13,
      "Pointy Fork":10,

    },
    "armor":{
      #Armor items that includes how mcuh damage they block
      "Leather Armor":10,
      "Steel Armor":20,
      "Diamond Armor":30,
      "Pots and pans":15,
      "Platinum Armor":20,
      "Mysterious Pendant":25,
      "Ghastly Armor": 21,
      "Gooey Armor":20
    }
  },

  "traps":{
    "Spike Trap":30,
    "Incinerator":20,
    "Dart Trap": 15,
    "Poison Trap":12,
    "Trapdoor": 30,
    "Snare Trap":10,
    "Falling Net":5,
    "Magic Trap":35,
    "Lightning Trap":30
  },
  "npc":{
    "Baldwin the Hairless":{
      "health": 50,
      "attack": 11,
      "gold": 20,
      "name":"Baldwin the Hairless",
      "activated":"false",
      'dialogue':{
        "Hello sir, who may you be?":{
            "item":"Baldwin's Dagger",
            "I am Baldwin the Hairless, warrior of light and a lost soul much like you. I hear of a monster seperating families roaming these halls.\nPlease be careful traveler.\nHere, have this present.":True
        },
        "You look like Mr.Clean, heck off, I don't like your commericals.":{
          "aggro":True,
          "prompt":"Come here you little brat, I'll show you who the real Mr.Clean is...."
        }
      }
    },
    "Adorable Puppy":{
      "health":50,
      "attack":5,
      "name":"Adorable Puppy",
      "gold":1,
      "activated":"false",
      'dialogue':{
        "Aww, and who may you be?":"Bark! Bark! The puppy looks at you wagging its tail and gleefully runs circles around your legs",
        "Kill ITTT":{
          "aggro":True,
          "prompt":"Wooof?"
        }
      }
    },
    "Old Woman":{
      "health":12,
      "attack":2,
      "gold":1,
      "name":"Old Woman",
      "activated":False,
      "dialogue":{
        "Hello there, are you ok?":{
          "quest":True,
          "Ah yes.., I am doing just fine..\nI've been roaming this place for quite some time..\nYou see I am getting quite old but for some reason the keys G, D, and F are always offtune for some reason..\nMaybe its just me..":True
        },
        "You must be an evil woman..\nDie!!":{
          "aggro":True,
          "prompt":"Wait no, I am no even woman!"
        }
      }
    },
    "Lone Ghost":{
      "health":1,
      "attack":1,
      "gold":1,
      "name":"Lone Ghost",
      "activated":"false",
      'dialogue':{
        "Ah! A ghost! Although, I don't really know if that's a surprise with all I've seen here.":{
          "item":"Ghastly Armor",
          "Please do not fear me, I'm quite friendly. \nHere, have this armor as a sign of my goodwill!":True
        },
        "Agh!\nWhat are you?\nDie!":{
          "aggro":True,
          "prompt":"Wait no, I am friendly!"
        }
      }
    },
    "Skeleton":{
      "health":40,
      "attack":15,
      "gold":30,
      "activated":False,
      "dialogue":{
        "Hello sir, do you need something? You seem particularty angry..":{
          "item":"Skeletal Hand",
          "No, I'm good. I had an issue this morning but don't worry about it.\nHere, have my hand. It may help you around this place.":True
        },
        "You look like you're a particularly rude skeleton! Prepare to face your maker!":{
          "aggro":True,
          "prompt":"What? How dare you, dastard! I'll show you what this 'rude skeleton' can do!"
        } 
      }
    },
     "boss":{
       "hp": 300,
       "attack":15
     }
}
}





print("""
==================================
Dungeon Escape V1.0 Deluxe Edition
==================================
""")

print("""
Story
  You blacked out after a strange figure came up to you..
  You woke up in what seems to be a hall
  There seems to be four direction you can go.
  
Your Objective:
  Kill the final boss in one of the rooms...

  Watch out for traps and keep a look out for items along your journey...
  Good Luck...
""")

input('\nPress enter to continue.')

def mobDrop(mob):
  global coins
  global mobsKilled
  mobsKilled.append(mob)
  DialogueList = list(gameData['npc'].keys())
  if (mob['name'] not in DialogueList):
    itemToDrop = random.choice(list(gameData['rooms'][location]['mob'][mob['name']]['lootPool']))
    inventory['weapons'].append(itemToDrop)
    goldEarned = gameData['rooms'][location]['mob'][mob['name']]['gold']
    coins += goldEarned
    print (f"You have picked up {itemToDrop} from the {mob['name']}\nYou have also picked up {goldEarned}")
    input("\n\nPress enter to continue!")
  else:
    goldEarned = gameData['npc'][mob['name']]['gold']
    coins += goldEarned
    print (f"You have picked up {goldEarned} gold from the {mob['name']}\n")
    input("\n\nPress enter to continue!")
  askDirection()
  

def resetgame(prompt): 
  global location
  global equipped_armor
  global equipped_weapon
  global inventory
  global health 
  global errMsg
  replit.clear()

  for char in prompt:
    sleep(0.05)
    sys.stdout.write(char)
    sys.stdout.flush()
  input("\nPress anything to restart the game!")

  location = 'Hall'
  equipped_weapon="None"
  equipped_armor="None"
  inventory = {"weapons":[],"items":[],"armor":[]}
  health = 100
  askDirection()

def combat(mob):
  global errMsg
  if (errMsg):
    errMsg = False
  else:
    replit.clear()
  global coins
  global health
  global equipped_armor
  global equipped_weapon

  mobHP = mob['health']
  mobATK = mob['attack']
  mobName = mob['name']

  defense = 0
  attack = 2

  try:
    defense = gameData['items']['armor'][equipped_armor]
  except KeyError:
    defense = 0

  try:
     attack = gameData['items']['attack'][equipped_weapon]
  except KeyError:
    attack = 2


  command = input (f"""
==================================
You got into a battle with a {mobName}
==================================
- Commands -
attack
use [item]
surrender
==================================
- Stats -
{coins} - Coins
{health} - HP 
{equipped_weapon} - Equipped Weapon
{equipped_armor} - Equipped Armor

{attack} - ATK
{defense} - DEF
==================================
- Enemy Stats -
{mobHP} - HP
{mobATK} - ATK
==================================
""")
  if health <= 0:
    newP = f"""
- Death -
The {mob['name']} slowly creeps you to you, as you have been knocked out.
He slowly drags your body over to his den, never to be seen again.
Your family notices and calls out a search to no results.
You have your funeral without your body, slowly disappearing into history.\n
    """
    resetgame()
  elif mob['health'] <= 0:
    mobDrop(mob)
  else:
    if (command.lower() == 'attack'):
      mob['health'] -= attack
      mobHP = mob['health']
      print(f'\n\nYou did {attack} damage to the {mobName}\n\nNow it is at {mobHP} HP\n\n')
      
      if mob['health'] <= 0:
        mobDrop(mob)

      if (mob['attack'] <= defense):
        damageDone = 0
      else:
        damageDone = mob['attack'] - defense

      health -= damageDone

      print(f'\n\nThe {mobName} did {mobATK} damage to you\n\nNow your at {health} HP\n\n')
      input("\nPress enter to continue!")
      newP = f"""
- Death -
The {mob['name']} slowly creeps you to you, as you have been knocked out.
He slowly drags your body over to his den, never to be seen again.
Your family notices and calls out a search to no results.
You have your funeral without your body, slowly disappearing into history.\n
    """
      if health == 0:
        resetgame(newP)

    elif (command.lower() == 'use'):
      replit.clear()
      errMsg = True
      try: 
        item = command.split(' ', 1)[1]
        if item in inventory['items']:
          if health + gameData['items']['healing'][item]['health'] > 100:
            health = 100
            print ("You have been restored to max HP!")
          else:
            health = health + gameData['items']['healing'][item]['health']
            print (f"Restored ${health + gameData['items']['healing'][item]['health']} HP!")
        else:
          print("Please enter a valid item to equip!")
          errMsg = True
          combat(mob)
      except IndexError:
        errMsg = True
        print("Please enter a valid item to equip!")
        combat(mob)
    elif (command.lower() == 'surrender'):
      newP = f"""
- Death -
The {mob['name']} slowly creeps you to you, as you put your arms up in surrender. You hope for mercy, but the {mob['name']} has no intention of showing it. Your cowardice is of no comfort to the frenzied mob. You become nothing more than face on a missing person's poster, and are eventually forgotten by the world.
      """
      resetgame(newP)
    else:
      print('Please enter a valid command!\n')
    combat(mob)

def trigger(trig):
  global location
  global gameData
  global coins
  global health
  global errMsg

  if (errMsg):
    errMsg = False
  else:
    replit.clear()

  if (location == "Hall #2" and "Mysterious Pendant" in inventory['items']):
    replit.clear()
    print("The pendant slowly starts to glow, floating outwards towards the cieling. You wonder what it is doing and it suddenly flashes and a key appears in your hand..\n\nRecieved basement keys!\n\n")
    inventory['items'].append("Basement Key")
    input("Press enter to continue..")
    askDirection()
  elif (location == 'Study Room'):
    if (gameData['rooms']['Study Room']['trigger']['activated'] != "true"):
      userInput = input(gameData['rooms']['Study Room']['trigger']['prompt'])
      if (userInput.lower() == 'yes'):
        piano()
      elif (userInput.lower() == 'no'):
        replit.clear()
        errMsg = True
        print("You step into the study room, looking around wondering what to do..\n")
        askDirection()
      else:
        replit.clear()
        errMsg = True
        print("Please enter a valid response! (Yes or No)\n\n")
        trigger(trig)
  elif (location == 'Basement'):
    if ("Basement Key" in inventory['items']):
      bossBattle()
    else:
      print("You stumble across a basement door but it seems to be locked.\nYou should come back with a key to unlock the door.")
      location = "Living Room"
      askDirection()
  elif (location == 'Outside'):
    finalWarnings = input(trig['prompt'] + "\n\n")
    if (finalWarnings.lower() == 'yes'):
      replit.clear()
      newP = """
- Death -
You walk outside into the cold, as the door seemingly shuts behind you.
A blizzard rages outside, while you try to walk to find any sign of life.
As you walk for miles, your legs get tired and you fall.
Your body slowly gets buried under the intense snow.
Your family eventually calls out a search party and they found your body.
You have your funeral, and you live a violent death.
      """
      resetgame(newP)
    elif (finalWarnings.lower() == 'no'):
      replit.clear()
      print("You slowly step back, walking back to the front door.")
      errMsg = True
      location = 'Front Door'
      askDirection()
    else:
      replit.clear()
      errMsg = True
      print('Please enter a valid resposne! (Yes or No)')
      trig(trig)
  elif(location == 'Dungeon' or location == 'Dungeon #2'):

    if (gameData['rooms'][location]['trigger']['triggeredCount'] <= 5):
        itemsel = input(trig['prompt'] + trig['mob'])

        if (itemsel.lower() == 'no'):
          activated = {'triggeredCount':gameData['rooms'][location]['trigger']['triggeredCount']+ 1}
          gameData['rooms'][location]['trigger'].update(activated)
          replit.clear()
          errMsg = True
          print('You slowly step towards the mob as you prepare to engage for battle.')
          combat(gameData['rooms'][location]['mob'][random.choice(list(gameData['rooms']  [location]['mob']))])
        elif (itemsel.lower() == 'yes'):
          replit.clear()
          print('You successfully run away from the mob, as you exit the dungeon into the    hall.\n\n')
          if location == "Dungeon":
            location = "Hall"
          else:
            location == "Hall #5"
          errMsg = True
          askDirection()
        else:
          replit.clear()
          print('\nPlease enter a valid response! (Yes or No)\n')
          errMsg = True
          trigger(trig)
        askDirection()
  elif('search' in trig):
    if location == 'Library':
      if trig['activated'] == 'false':
        itemsel = input(trig['prompt'])
        try:
          if int(itemsel) > 0 and int(itemsel) < 4:
            activated = {'activated':'true'}
            gameData['rooms']['Library']['trigger'].update(activated)
            replit.clear()
            print(trig['search'][itemsel]['prompt'])
            input("\nPress enter to continue..\n")
            replit.clear()
            errMsg = True

            if trig['search'][itemsel]['item'] != 'nothing':
              if trig['search'][itemsel]['item'] == "Gold":
                goldToGive = int(trig['search'][itemsel]['item'].split()[0])
                coins += goldToGive
                print (f'You have received {goldToGive} gold')
              else:
                if trig['search'][itemsel]['item'] in gameData['items']['healing']:
                  inventory['items'].append(trig['search'][itemsel]['item'])
                  print('You have received a ' + trig['search'][itemsel]['item'])
                elif trig['search'][itemsel]['item'] in gameData['items']['attack']:
                  inventory['weapons'].append(trig['search'][itemsel]['item'])
                  print('You have received the ' + trig['search'][itemsel]['item'])
                else:
                  inventory['armor'].append(trig['search'][itemsel]['item'])
                  print('You have received a ' + trig['search'][itemsel]['item'])
                input("\n\nPress enter to continue..\n")
                replit.clear()
            askDirection()
        except ValueError:
          replit.clear()
          print('Please enter a valid number!')
          errMsg = True
          trigger(trig)
      else:
        askDirection()
  elif('traps' in trig):
    if (location == 'Front Door' or "Hall #4" or "Hall #5"):
      if trig['activated'] == 'false':
        print(trig['prompt'])
        cmdInput = input()

        if (cmdInput.lower() == 'yes'):
          replit.clear()
          errMsg = True
          randomTrap = random.choice(list(gameData['rooms'][location]['trigger']
          ['traps']))
          print(randomTrap)
          damageTaken = gameData['traps'][randomTrap]
          print(f"\n\nYou pressed the button and suddently a {randomTrap} activated!\n\nYou took {damageTaken} damage\n\n")
          health -= damageTaken
          askDirection()
        elif cmdInput.lower() == 'no':
          replit.clear()
          print(f"\n\nYou backed away from it fearing it is a trap\n\n")
          input("\nPress enter to continue..")
          askDirection()
        else:
          replit.clear()
          print('Please enter a valid response! (Yes or No)\n\n')
          errMsg = True
          trigger(trig)
      else:
        askDirection()
  
  elif('items' in trig):
    itemList = []
    finalText = "\n"
    for key in trig['items']:
      #The text at the end that displays the item and what it costs e.g. Excalibur - 5 gold]
      finalText += f"{key} - {trig['items'][key]} Gold\n"
      itemList.append(key)
    print(finalText)
    command = input(f"""
==================================
Shop
==================================
- Stats -
{coins} - Coins
{health} - HP 
{equipped_weapon} - Equipped Weapon
{equipped_armor} - Equipped Armor
==================================
{finalText}
==================================
Commands
==================================
buy (item)
go (north, south, east, west)
inventory
map
==================================
""")
    if "map" in command.lower():
      replit.clear()
      print(displayMap())
      input("\n\nPress enter to continue\n")
      askDirection()
    elif "buy" in command.lower():
      replit.clear()
      errMsg = True
      try: 
        direction = command.split(" ", 1)[1]
        if direction in itemList:
          if coins >= trig['items'][direction]:
            coins -= trig['items'][direction]

            if direction in gameData['items']['healing']:
              inventory['items'].append(direction)
            elif direction in gameData['items']['attack']:
              inventory['weapons'].append(direction)
            else:
              inventory['armor'].append(direction)
            print(f"You have successfully bought the {direction}")
          else:
            print("You do not have enough coins for that item!")
            errMsg = True
            trigger(trig)
        else:
          print("Please enter a VALID item to buy.")
          errMsg = True
          trigger(trig)
      except IndexError:
        print("You didn't enter an item to buy!")
        errMsg = True
        trigger(trig)
    elif "sell" in command.lower():
      try: 
        item = command.split(" ", 1)[1]
        if (item in gameData['rooms']['Shop']['trigger']['items'] and item in inventory['items'] or item in inventory['weapons'] or item in inventory['armor']):
          goldValue = gameData['rooms']['Shop']['trigger']['items'][command.split(" ", 1)[1]]
          goldGiven = math.ceil(goldValue - 20*goldValue / 100.0)
          confirmation = input(f"Please confirm that you would like to sell {item} for {goldGiven} (Yes or No)")

          if confirmation.lower() == 'yes':
            replit.clear()
            errMsg = True
            coins += gameData['rooms']['Shop']['trigger']['items'][command.split(" ", 1)[1]]
            print(f"You have sold a {item} for {goldGiven}")
          elif confirmation.lower() == 'no':
            trigger(trig)
          else:
            replit.clear()
            errMsg = True
            print("Confirmation prompt cancelled, invalid response.\nPlease enter a yes or no next time.")
      except IndexError:
        print('test')
    elif "go" in command.lower():
      replit.clear()
      errMsg = True
      try: 
        direction = command.split(" ", 1)[1]
        if direction.lower() in directions:
          if direction.lower() in gameData['rooms'][location]:
            location = gameData['rooms'][location][direction.lower()]
            replit.clear()
            errMsg = True
            print('You are now in the '+ location + "\n")
            if 'trigger' in gameData['rooms'][location]:
              trigger(gameData['rooms'][location]['trigger'])
              askDirection()
            else:
              askDirection()
          else:
            print('You cannot go in that direction!\n\n')
            errMsg = True
            trigger(trig)
        else:
          print('You cannot go in that direction!\n\n')
          errMsg = True
          trigger(trig)
      except IndexError:
        print("You didn't enter a direction to go towards!")
    elif ("inventory" in command.lower()):
      replit.clear()
      errMsg = True
      print(f"Your Weapons - {','.join(inventory['weapons'])}\nYour Armors - {','.join(inventory['armor'])}\nYour Items - {','.join(inventory['items'])}")
    else:
      replit.clear()
      print("Please enter a valid command!")
      errMsg = True
      trigger(trig)

  elif "item" in trig:
    if (trig['activated'] != "true"):
      mainInput = input(trig['prompt'])
      if mainInput.lower() == "yes":
        replit.clear()
        errMsg = True
        if (isinstance(trig['item'],int)):
          coinsEarned = trig['item']
          coins += coinsEarned
          replit.clear()
          errMsg = True
          print(f"You have recieved {coinsEarned} gold!")
        elif (trig['item'] in gameData['items']['attack']):
         inventory['weapons'].append(trig['item'])
         replit.clear()
         errMsg = True
         print(trig['prompt2'])
         print(f"\n\nYou have recieved {trig['item']}!")
        elif (trig['item'] in gameData['items']['healing']):
         inventory['items'].append(trig['item'])
         replit.clear()
         errMsg = True
         print(trig['prompt2'])
        else:
          inventory['armor'].append(trig['item'])
          print(trig['prompt2'])
          print(f"\n\nYou have recieved {trig['item']}!")
        activated = {'activated':'true'}
        gameData['rooms'][location]['trigger'].update(activated)
      elif mainInput.lower() == "no":
        replit.clear()
        errMsg = True
        print("You look around wondering what to do...")
        askDirection()
      else:
        replit.clear()
        print("Please enter a valid response. (Yes or No)\n")
        errMsg = True
        trigger(trig)
    else:
      askDirection()

  elif("npc" in trig):
    userInput = input(trig['prompt'] + "\n")
    if (trig['activated'] != "true"):
      if (userInput.lower() == 'yes'):
        activated = {'activated':'true'}
        gameData['npc'][trig['npc']].update(activated)
        Startdialogue(gameData['npc'][trig['npc']])
      elif (userInput.lower() == 'no'):
       replit.clear()
       errMsg = True
       print("You stare around blanky, wondering what to do..")
       askDirection()
      else:
        replit.clear()
        print("Please enter a valid response. (Yes or No)\n")
        errMsg = True
        trigger(trig)
    else:
      askDirection()
  
  else:
    replit.clear()
    errMsg = True
    print(trig['prompt'])
    askDirection()
  
  




def askDirection():
  global health
  global equipped_armor
  global equipped_weapon
  global location
  global direction
  global inventory
  global errMsg

  defense = 0
  attack = 2

  if (errMsg):
    errMsg = False
  else:
    replit.clear()


  try:
    defense = gameData['items']['armor'][equipped_armor]
  except KeyError:
    defense = 0

  try:
     attack = gameData['items']['attack'][equipped_weapon]
  except KeyError:
    attack = 2

  direction = input(f"""
==================================
What would you like to do?
==================================
- Commands -
go [north, south, east, west]  
inventory
equip [item]
use [item]
map
==================================
- Stats -
{coins} - Coins
{health} - HP 
{equipped_weapon} - Equipped Weapon
{equipped_armor} - Equipped Armor

{attack} - ATK
{defense} - DEF
==================================
You are currently in the {location}
==================================
""")
  if "map" in direction.lower():
    replit.clear()
    print(displayMap())
    input("\n\nPress enter to continue\n")
    askDirection()
  elif "go" in direction.lower():
    replit.clear()
    errMsg = True
    try: 
      direction = direction.split(" ", 1)[1]
      if direction.lower() in directions:
        if direction.lower() in gameData['rooms'][location]:
          location = gameData['rooms'][location][direction.lower()]
          replit.clear()
          errMsg = True
          print('You are now in the '+ location + "\n")
          errMsg = True
          if 'trigger' in gameData['rooms'][location]:
            trigger(gameData['rooms'][location]['trigger'])
            askDirection()
          else:
            askDirection()
        else:
          replit.clear()
          print('You cannot go in that direction!\n\n')
          errMsg = True
          askDirection()
      else:
        replit.clear()
        print('You cannot go in that direction!\n\n')
        errMsg = True
        askDirection()
    except IndexError:
      replit.clear()
      print("You didn't enter a direction to go towards!")
      errMsg = True
  elif "inventory" in direction.lower():
    replit.clear()
    errMsg = True
    print(f"Your Weapons - {','.join(inventory['weapons'])}\nYour Armors - {','.join(inventory['armor'])}\nYour Items - {','.join(inventory['items'])}")
    askDirection()
  elif "equip" in direction.lower():
    replit.clear()
    errMsg = True
    try: 
      item = direction.split(" ", 1)[1]
      if item in inventory['armor']:
        equipped_armor = item
        print(f"You have equipped the {item}")
        askDirection()
      elif item in inventory['weapons']:
        equipped_weapon = item
        print(f"You have equipped the {item}")
        askDirection()
      else:
        replit.clear()
        print("Please enter a valid item to equip!")
        errMsg = True
        askDirection()
    except IndexError:
      replit.clear()
      print("Please enter a valid item to equip!")
      errMsg = True
      askDirection()
  elif "use" in direction.lower():
    replit.clear()
    errMsg = True
    try: 
      item = direction.split(" ", 1)[1]
      if item in inventory['items']:
        if health + gameData['items']['healing'][item]['health'] > 100:
          health = 100
          print ("You have been restored the max HP!")
        else:
          health = health + gameData['items']['healing'][item]['health']
          print (f"Restored ${health + gameData['items']['healing'][item]['health']} HP!")
      else:
        replit.clear()
        errMsg = True
        print("Please enter a valid item to equip!")
        askDirection()
    except IndexError:
      errMsg = True
      print("Please enter a valid item to equip!")
      askDirection()
  else:
      replit.clear()
      errMsg = True
      print("Type in a valid command!")
      askDirection()

def Startdialogue(character):
  global quest
  dialogueList = list(character['dialogue'].keys())
  try:
    response = input(f"1) {dialogueList[0]}\n2) {dialogueList[1]}\n")
    replit.clear()
    if ("1" in response):
      if ("aggro" in character['dialogue'][dialogueList[0]]):
        print(character['dialogue'][dialogueList[0]]['prompt'])
        input("\n\nPress anything to continue!")
        combat(character)
      elif("item" in character['dialogue'][dialogueList[0]]):
        print(list(character['dialogue'][dialogueList[0]].keys())[1])
        errMsg = True
        item = character['dialogue'][dialogueList[0]]['item']
        print(f"\n\nYou have recieved the {item}")
        inventory['weapons'].append(item)
      else:
        print(character['dialogue'][dialogueList[0]])
        input("\n\nPress anything to continue!")
    elif ("2" in response):
      if ("aggro" in character['dialogue'][dialogueList[1]]):
        print(character['dialogue'][dialogueList[1]]['prompt'])
        input("\n\nPress anything to continue!")
        combat(character)
      elif("item" in character['dialogue'][dialogueList[1]]):
        print(list(character['dialogue'][dialogueList[0]].keys())[1])
        errMsg = True
        print(f"\nYou have recieved the {character['dialogue'][dialogueList[1]]['item']}")
        inventory['weapons'].append(character['dialogue'][dialogueList[1]]['item'])
      else:
        print(character['dialogue'][dialogueList[1]])
        input("\n\nPress anything to continue!")
  except IndexError:
    askDirection()


def bossBattle():
  replit.clear()
  global health
  global equipped_armor
  global equipped_weapon
  global mobsKilled

  if (len(mobsKilled) == 0):
    print("""
Hello fellow being..
I see you have stepped into my mansion.

You have been quite passive throughout the mansion.

I see you are not the monster I am looking for.

You are free to go.
    """)
    input("\nPress enter to continue")
    winGame()
  else:
    finaltext = ""

    for mob in mobsKilled:
     finaltext += mob

    dialogueToDisplay = f"""
==================================
Puppy God
==================================
Hello fellow being..
I see you have stepped into my mansion.

These monsters in the halls you hear of, the evil being is you..

You've been seperating families left right and center..

You have even killed the...
{finaltext}

Now you must pay for your actions..

Tho you are my enemy, I must be fair.
You will have 200hp to fight me.

As a tradeoff however, your armor will be taken away.
Good luck.

(Press enter to continue)
==================================
    """
    print(dialogueToDisplay)
    input("")
    replit.clear()
    equipped_armor = "None"

    health = 200
    finalPreprations()

def finalPreprations():
  global inventory
  global health
  global equipped_weapon

  mobHP = gameData['boss']['hp']
  mobATK = gameData['boss']['attack']

  try:
    defense = gameData['items']['armor'][equipped_armor]
  except KeyError:
    defense = 0

  try:
     attack = gameData['items']['attack'][equipped_weapon]
  except KeyError:
    attack = 2

  print(f"""
==================================
Boss Battle - The Puppy God
==================================
- Stats -
{health} - HP 
{equipped_weapon} - Equipped Weapon

{attack} - ATK
{defense} - DEF
==================================
- Enemy Stats -
{mobHP} - HP
{mobATK} - ATK
==================================
Commands
==================================
equip [attack item]
ready
==================================
Objective
==================================
Soon, you will now enter into a battle with the puppy god.
You have a specified amount of time to type a specfic word.
For every word missed or not answered in time, you will take 10 damage.
Difficulty will increase as time goes on, good luck.
You will not have a chance to heal.
==================================
 """)

  finalCmd = input('\nPlease make final preperations for the upcoming boss battle.\nEquip any weapons that you need.\n\nWhen you are ready, please type "ready".\n\n')

  if (finalCmd.lower() == 'ready'):
    replit.clear()
    battle(gameData['boss']['hp'], 20)
  elif ("equip" in finalCmd.lower()):
    try:
      item = finalCmd.split(' ', 1)[1]
      if (item in gameData['items']['attack'] and item in inventory['weapons']):
        replit.clear()
        print(f"Equipped the {item}!")
        equipped_weapon = item
        finalPreprations()
      else:
        replit.clear()
        print("Please enter a valid weapon to equip!")
        finalPreprations()
    except IndexError:
        replit.clear()
        print("Please enter a weapon to equip!")
        finalPreprations()
  else:
    replit.clear()
    print("Please enter a valid command!")
    finalPreprations()



def battle(hp, times):
  global health
  global equipped_armor
  global equipped_weapon

  try:
     attack = gameData['items']['attack'][equipped_weapon]
  except KeyError:
    attack = 2

  mobHP = hp
  mobATK = gameData['boss']['attack']

  wordToType = random.choice(wordsList)

  if (health < 1):
    print('test')
  elif (hp < 1):
    winGame()
  else:

    print(f"""
==================================
Boss Battle - The Puppy God
==================================
- Stats -
{health} - HP 
{equipped_weapon} - Equipped Weapon
{equipped_armor} - Equipped Armor

{attack} - ATK
==================================
- Enemy Stats -
{mobHP} - HP
{mobATK} - ATK
==================================
 \n\n """)

    print(f"Please type {wordToType} in {times} seconds!")
    i, o, e = select.select( [sys.stdin], [], [], times )

    if (i):
     if (sys.stdin.readline().strip().lower() == wordToType):
       replit.clear()
       print(f"You have dealt {attack} damage to the puppy god!")
       hp -= attack
       times -= 0.2
       battle(hp, times)
     else:
       replit.clear()
       print(f"You have failed to enter the correct word!\nYou have taken {mobATK} damage!")
       health -= mobATK
       times -= 0.5
       battle(hp, times)
    else:
      replit.clear()
      print(f"You have failed to respond in time!\nYou have taken {mobATK} damage!")
      health -= mobATK
      times -= 0.5
      battle(hp, times)




def piano():
  global inventory
  global errMsg

  if (errMsg):
    errMsg = False
  else:
    replit.clear()
  tempResponse = ""
  try: 
    keys = ["C","D","E","F","G"]
    tempResponse = input("Play a piece of music. The piano only seems to have 5 keys: C,D,E,F,and  G.\nSeparate your notes by spaces, and play only three.\n\nType 'exit' to back out.\n\n")
    g,d,f = tempResponse.split()


    if g == "G" and d == "D" and f == "F":
      inventory['items'].append("Mysterious Pendant")
      replit.clear()
      errMsg = True
      activated = {'activated':"true"}
      gameData['rooms']['Study Room']['trigger'].update(activated)
      print('Agh! A mysterious pendant fell out of the piano. You wonder what this does.')
    
    elif g not in keys or d not in keys or f not in keys:
      replit.clear()
      errMsg = True
      print("Please play a key that's on the piano!")
      piano();
    else:
      print("Hmm, those keys didn't seem to do anything..\nMaybe I should try again..")
      piano()
  except ValueError:

    replit.clear()
    errMsg = True

    if (tempResponse.lower() == 'exit'):
      askDirection
    else:
      print("Please enter the keys seperated by a space!\n")
      piano()

def winGame():
  replit.clear()
  words = """
-- Congrats --
You have beat the game!
Thank you for playing 'Dungeon Escape V1.0 Deluxe Edition'
This game was made ontop of hours of work by the Intro to Python track!
I doubt many people will get here but hey for those who do, congrats!
\n
"""
  for char in words:
    sleep(0.05)
    sys.stdout.write(char)
    sys.stdout.flush()
  input("\nPress anything to restart the game!")

def displayMap():
  global location
  newMapGen = replacenth(newMap, gameData['rooms'][location]['uniChar'], "*", gameData['rooms'][location]['mapCount']) + "	"
  return newMapGen


askDirection()
#displayMap()
#Startdialogue(gameData['npc']['Baldwin the Hairless'])
#location = "Outside"
#trigger(gameData['rooms']['Outside']['trigger'])
#winGame()
#bossBattle()
