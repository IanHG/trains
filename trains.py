#!/usr/bin/python

import random
import math

game_state = {
   # Rules map, defines basic rules of the game.
   "rules_map" : {
      # Range for number of trips per round
      "trips" : (6, 6),
      "random_factor" : (1.00, 0.07),
      "trip_turn_random_term" : (-1, 6),
      "trip_die"      : (1, 6),
      "trip_mean_die" : None,
      "trip_space"    : 10,
      },
   # Goods map, defines; goods_name : statistical_weight, base_unit_price, min_unit, max_unit, liability in %
   "goods_map": {
      "Wood"   : (6, 100, 3, 10, 30),
      "Stone"  : (4, 200, 3, 8 , 50),
      "Coal"   : (3, 300, 2, 6 , 70),
      "Silver" : (1, 400, 1, 3 , 95),
      "Gold"   : (1, 500, 1, 2 , 110),
      },
   # Goods roll, get a goods from a random roll (created at game start).
   "goods_roll" : [],
   # City map (will get populated with the cities of the current game)
   "city_map" : [],
   # Mean distance to center
   "city_mean_dist" : None,
}

def random_factor(state):
   rule_random = state["rules_map"]["random_factor"]
   return random.normalvariate(rule_random[0], rule_random[1])

def roundup(x):
   return int(math.ceil(x / 10.0)) * 10

def quit(state):
   return True

def print_train():
   print("")
   print("         o o o o ~~  ~~ ~                                      _____         ")
   print("      o     _____         ________________ ________________ ___|_=_|_()__    ")
   print("    .][_mm__|[]| ,===___ ||              | |              | |          |     ")
   print("   >(_______|__|_|_GBRR_]_|              |_|              |_|          |_|   ")
   print("   _/oo-OOOO-oo' !oo!!oo!=`!o!o!----!o!o!'=`!o!o!----!o!o!'=`!o!o--o!o!'     ")
   print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
   print("")

#
def input_add_city(state):
   print("Enter city name, then distance to center and lastly compas direction (degrees).")
   city_name           = raw_input()
   distance_to_center  = raw_input()
   degrees             = raw_input()
   state["city_map"].append((int(distance_to_center), int(degrees), city_name))
   return False

def input_load_cities_file(state):
   filename = raw_input()
   with open(filename) as f:
      for line in f:
         line_split = line.split(",")
         city_name          = line_split[0]
         distance_to_center = line_split[1]
         degrees            = line_split[2]
         state["city_map"].append((int(distance_to_center), int(degrees), city_name))

def input_print_city_map(state):
   for value in state["city_map"]:
      print(value[2] + " - " + str(value[0]) + "m from center at " + str(value[1]) + "degrees.")

def city_scale_factor(dist, city_mean_dist):
   return (math.tanh(dist / city_mean_dist) + 1.0) / 2.0
   #return dist / city_mean_dist

def create_trips(state):
   number_of_trips = random.randint(state["rules_map"]["trips"][0], state["rules_map"]["trips"][1])
   goods_map = state["goods_map"]
   city_map  = state["city_map"]
   city_mean_dist  = state["city_mean_dist"]

   print_train()

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
      city1 = city_map[city1]
      city2 = city_map[city2]

      city1_fac = city_scale_factor(city1[0], city_mean_dist)
      city2_fac = city_scale_factor(city2[0], city_mean_dist)
      city_dist = math.sqrt(city1[0]*city1[0] + city2[0]*city2[0] - 2*city1[0]*city2[0]*math.cos(math.radians(city1[1]-city2[1])))
      city_dist_fac = city_scale_factor(city_dist, city_mean_dist)
      #print("City dist  = " + str(city_dist))
      #print("City 1 fac = " + str(city1_fac))
      #print("City 1 fac = " + str(city2_fac))
      #print("City   fac = " + str(city_dist_fac))
      #print("Rand   fac = " + str(randfac))

      total_fac = city1_fac * city2_fac * city_dist_fac * randfac

      #print("Total fac = " + str(total_fac))


      """ Generate goods and price """
      goods = state["goods_roll"][random.randint(0, len(state["goods_roll"]) - 1)]
      load  = random.randint(goods_map[goods][2], goods_map[goods][3])
      price = roundup(goods_map[goods][1] * total_fac)
      liability = roundup(goods_map[goods][4] * price / 100) 

      """ Generate number of turns """
      trip_turns = (city_dist / state["rules_map"]["trip_space"] / state["rules_map"]["trip_mean_die"]) + random.randint(state["rules_map"]["trip_turn_random_term"][0], state["rules_map"]["trip_turn_random_term"][1])
      trip_turns = math.ceil(trip_turns * random_factor(state))
      
      #print(goods + " : " + str(load) + " at " 
      print(repr(str(load)).ljust(5) + repr(goods).ljust(10) + " from " + repr(city1[2]).ljust(20) + " to " + repr(city2[2]).ljust(20) + " at " + repr(str(price)).ljust(6) + " in " + repr(str(int(trip_turns))).ljust(4) + "  liability : " + repr(str(liability).ljust(5)))
      print("")

   print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")


def game_turn(state):
   trips = create_trips(state)
   return False


game_driver_map = {
   "1" : ("Take turn.", game_turn),
   "2" : ("Quit :C", quit),
}

def initialize_game(state):
   print("initializing")
   
   city_map = state["city_map"]

   print("Checking city map")
   if len(city_map) < 2:
      print("City map must be a least size 2.")
      return False
   
   print("Calculating mean distance to center.")
   mean_dist = 0.0
   for value in city_map:
      mean_dist = mean_dist + value[0]
   mean_dist = mean_dist / len(city_map)
   print(mean_dist)
   state["city_mean_dist"] = mean_dist

   state["rules_map"]["trip_mean_die"] = 3.5

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
   "2" : ("Load cities from file.", input_load_cities_file),
   "3" : ("Print city map.", input_print_city_map),
   "4" : ("Start game!", game_driver),
   "5" : ("Quit :C", quit),
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

   print_train()


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
