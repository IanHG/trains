#!/usr/bin/python

import random

game_state = {
   # Rules map, defines basic rules of the game.
   "rules_map" : {
      # Range for number of trips per round
      "trips" : (7, 12),
      "random_factor" : (1.00, 0.07),
      },
   # Goods map, defines; goods_name : statistical_weight, base_unit_price, min_unit, max_unit
   "goods_map": {
      "wood"   : (4, 100, 5, 15),
      "stone"  : (3, 200, 3, 10),
      "coal"   : (2, 300, 2, 7),
      "silver" : (1, 400, 1, 5),
      "gold"   : (1, 500, 1, 4),
      },
   # Goods roll, get a goods from a random roll (created at game start).
   "goods_roll" : [],
   # City map (will get populated with the cities of the current game)
   "city_map" : {},
}

def random_factor(state):
   rule_random = state["rules_map"]["random_factor"]
   return random.normalvariate(rule_random[0], rule_random[1])

def quit(state):
   return True

#
def input_add_city(state):
   print("Enter city name, then distance to center and lastly compas direction (degrees).")
   city_name           = raw_input()
   distance_to_center  = raw_input()
   degrees             = raw_input()
   state["city_map"][city_name] = (int(distance_to_center), int(degrees))
   return False

def input_print_city_map(state):
   for key, value in state["city_map"].iteritems():
      print(key + " - " + str(value[0]) + "m from center at " + str(value[1]) + "degrees.")

def create_trips(state):
   number_of_trips = random.randint(state["rules_map"]["trips"][0], state["rules_map"]["trips"][1])
   goods_map = state["goods_map"]
   city_map  = state["city_map"]

   """ Loop over number of trips for round and generate random trips """
   for n in range(0, number_of_trips):
      """ Generate city pair and multiplication factor.
          Multiplication faction depends on distance from center of both cities 
          and distance between the cities.
      """
      city1 = random.randint(0, len(city_map) - 1)
      city2 = random.randint(0, len(city_map) - 1)
      while city2 == city1:
         city2 = random.randint(0, len(city_map) - 1)
      randfac = random_factor(state)
      print(city1)
      print(city2)
      print(randfac)


      """ Generate goods and price """
      goods = state["goods_roll"][random.randint(0, len(state["goods_roll"]) - 1)]
      load  = random.randint(goods_map[goods][2], goods_map[goods][3])
      print(goods + " : " + str(load))


def game_turn(state):
   trips = create_trips(state)
   return False


game_driver_map = {
   "1" : ("Take turn.", game_turn),
   "2" : ("Quit :C", quit),
}

def initialize_game(state):
   print("initializing")
   
   print("Checking city map")
   if len(state["city_map"]) < 2:
      print("City map must be a least size 2.")
      return False

   print("Setting up goods roll map")
   for key, value in state["goods_map"].iteritems():
      for i in range(0, value[0]):
         state["goods_roll"].append(key)
   
   print(state["goods_roll"])
   return True

def game_driver(state):
   print("game startet")
   
   """ Initialize game """
   init = initialize_game(state)
   if not init:
      return False
   
   """ Start game loop """
   while True:
      for key, value in game_driver_map.iteritems():
         print(key + ": " + value[0])
      userinp = raw_input()
      stop = game_driver_map[userinp][1](game_state)
      if stop:
         print("Quitting game")
         break

   return False


setup_game_map = {
   "1" : ("Add city.", input_add_city),
   "2" : ("Print city map.", input_print_city_map),
   "3" : ("Start game!", game_driver),
   "4" : ("Quit :C", quit),
}

# Print game header.
def print_game_header():
   """ Print games header """
   print("")
   print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
   print("")
   print("              /$$$$$$$$                 /$$                                  ")
   print("             |__  $$__/                |__/                                  ")
   print("                | $$  /$$$$$$  /$$$$$$  /$$ /$$$$$$$   /$$$$$$$              ")
   print("                | $$ /$$__  $$|____  $$| $$| $$__  $$ /$$_____/              ")
   print("                | $$| $$  \__/ /$$$$$$$| $$| $$  \ $$|  $$$$$$               ")
   print("                | $$| $$      /$$__  $$| $$| $$  | $$ \____  $$              ")
   print("                | $$| $$     |  $$$$$$$| $$| $$  | $$ /$$$$$$$/              ")
   print("                |__/|__/      \_______/|__/|__/  |__/|_______/               ")
   print("")
   print("")
   print("         o o o o ~~  ~~ ~                                      _____         ")
   print("      o     _____         ________________ ________________ ___|_=_|_()__    ")
   print("    .][_mm__|[]| ,===___ ||              | |              | |          |     ")
   print("   >(_______|__|_|_GBRR_]_|              |_|              |_|          |_|   ")
   print("   _/oo-OOOO-oo' !oo!!oo!=`!o!o!----!o!o!'=`!o!o!----!o!o!'=`!o!o--o!o!'     ")
   print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
   print("")


# Define main
def main():
   """ Print game header/intro. """
   print_game_header()
   
   """ Setup loop. """
   while True:
      print("What?")
      for key, value in setup_game_map.iteritems():
         print(key + ": " + value[0])
      userinp = raw_input()
      stop = setup_game_map[userinp][1](game_state)
      if stop:
         print("Quitting game")
         break

# Run main
if __name__ == "__main__":
   main()
