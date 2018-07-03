#!/usr/bin/python3
import os
import json
import sys

homedir = os.path.expanduser('~')
this = { "datadir": homedir+"/.config/dissolve", "update": False }

# example of data structure
#{
#  'instance': "data.dat",
#  'nest':
#    [
#      { 'instance': "words", 'nest':[] },
#      { 'instance': "overword", 'nest':
#        [
#          { 'instance': "wolo", 'nest':
#             [
#               {'instance': "curve", 'nest': []} 
#             ] 
#           },
#          { 'instance': "sparrow", 'nest':[] },
#          { 'instance': "love", 'nest':[] }
#        ]
#      },
#      { 'instance': "long", 'nest':[] }
#    ]
#}
#
# command structure
# [ command [ action ] [ value ] [ input ] ]
# ex: ( problem ( long ) ( time ago ) )
# creates new subproblem under 'long'

### init file

def init(inp):
  setup()   # start all of it
  route(inp)   # route input 
  update()  # update if changes to datafile

### Comunication with data structure

def showInstance(data, spa = 0): #since they are recursive(sorry) they'll have to be applied func(self.data)
  for x in data['nest']:
    print(' '*spa + x['instance'])
    if len(x['nest']) > 0:
      showInstance(x, spa+2)

def newInstance(data, atTask, sentence): #add a problem or subproblem
  for x in data['nest']:
    if x['instance'] == atTask:
      x['nest'].append( {'instance': sentence, 'nest': []} )
      break
    if len(x['nest']) > 0:
      newInstance(x, atTask, sentence)

def delInstance(data, whichDel, prev): #  when problem is done delete it
  for y, x in enumerate(data['nest']):
    if whichDel == x['instance']:
      del prev['nest'][y]
      break
    if len(x['nest']) > 0:
      prev = x
      delInstance(x, whichDel, prev)

### Communication with user

def workInGoalM(inp): # functions: change current goal, list goals, print current goal, del goal
  if inp[0] == "list": 
    entries = [ x for x in os.listdir(this['datadir']) if ".dat" in x]
    print('\n'.join(entries))
  elif inp[0] == "new": 
    initGoal( inp[1] )
    initGoalfile( inp[1] )
  elif inp[0] == "del": 
    os.remove( this['datadir']+"/"+inp[1]+".dat" )
    initGoalfile("default")
  elif inp[0] == "curr":
    print("current goal you are working on is "+fetchCurrentProblem())
  elif len(inp) == 1: 
    initGoalfile( inp[0] )
  else:
    print("bad input, use dissolve help to check args")

def workInProblemM(inp): # functions: add a problem and remove a problem ( <= change this['update'] to True ), list problems
  if len(inp) == 2: 
    this['update'] = True
    newInstance( this['data'], inp[0], inp[1])
  elif inp[0] == "list": 
    showInstance( this['data'] )
  elif len(inp) == 1: 
    this['update'] = True
    delInstance( this['data'], inp[0], this['data'] )
  else:
    print("bad input, use 'dissolve help' to check args")

def help(parameterThatDoesNothing): # functions: print instructions
  with open("./readme.md", 'r') as f:
    print( f.read() )

def route(inp):
  choice = { "goal": workInGoalM, "problem": workInProblemM, "help": help } 
  try:
    choice[ inp[0] ]( inp[1:] )
  except KeyError:
    print("Invalid instruction, try help")

### creating data structure

# final structure of this
# this = { 'datadir': '~/.config/dissolve', 'update': False, 'goalname': nameOfProblem, 'data': dataFromFile }

def setup():
  if not(os.path.exists( this['datadir'] )):
    os.makedirs( this['datadir'] )
    initGoalfile("default")
    initGoal("default")
    this['goalname'] = this['datadir']+"/default"
  else:
    this['goalname'] = this['datadir']+"/"+fetchCurrentProblem()
  this['data'] = getData( this['goalname'] )

def fetchCurrentProblem():
  with open( this['datadir']+"/goal", 'r' ) as f:
    return f.read()

def getData(data):
  with open(data+".dat", "r") as f:
    return json.loads( f.read() )

### writing to data structure

def update():
  if this['update']:
    with open( this['goalname']+".dat", "w" ) as f:
      f.write( json.dumps( this['data'] ) )

def initGoalfile(name):
  with open( this['datadir']+"/goal", "w+" ) as f:
    f.write(name)

def initGoal(name):
  with open( this['datadir']+"/"+name+".dat", "w+" ) as f:
      f.write( json.dumps( { 'nest': [ {'instance': name+".dat", "nest": []}]}) )

cmd = sys.argv[1:] 
init(cmd)
