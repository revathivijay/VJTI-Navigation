#------------------------------Part1--------------------------------
# In this part we import necessary graph files and initialize our graph
from src.Graph import Graph,initialize_map

nodes,map_node = initialize_map('src/nodes.json')
graph = Graph(25, nodes)
graph.addAllEdges('src/edges.csv')

SOURCE = None #"Staircase main bldg/statue"

#------------------------------Part2--------------------------------
# Here we define our Lambda function and configure what it does when 
# an event with a Launch, Intent and Session End Requests are sent.

def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()
        
#------------------------------Part3--------------------------------
# Here we define the Request handler functions
def on_start():
    print("Session Started.")

def on_launch(event):
    onlunch_MSG = "Welcome to VJTI! Where do you want to go?"
    reprompt_MSG = "Where do you want to go?"
    card_TEXT = ""
    card_TITLE = ""
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, reprompt_MSG, False)

def on_end():
    print("Session Ended.")

#-----------------------------Part3.1-------------------------------
# The intent_scheme(event) function handles the Intent Request
def intent_scheme(event):
    
    intent_name = event['request']['intent']['name']

    if intent_name == "DirectionIntent":
        return direction(event)
    elif intent_name == "SourceIntent":
        return set_source(event)
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    
    return fallback_call(event)
    
#---------------------------Part3-------------------------------
# intent handler functions
def direction(event):
    name=event['request']['intent']['slots']['destination']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    global SOURCE
    if SOURCE:
        if name in map_node.keys():
            speech_msg = "Fetching directions for " + name + ":  " + getPath(destination=name,source=SOURCE)
            reprompt_MSG = "Did you want directions to some other place, please say which one?"
            return output_json_builder_with_reprompt_and_card(speech_msg, reprompt_MSG, False)
        else:
            wrongname_MSG = "You haven't given a valid location. Say Help for more details."
            reprompt_MSG = "Where do you want to go"
            return output_json_builder_with_reprompt_and_card(wrongname_MSG, reprompt_MSG, False)
    else:
        speech_msg = "Set source location"
        reprompt_MSG = "Say Set source as to give a source location"
        return output_json_builder_with_reprompt_and_card(speech_msg, reprompt_MSG, False)

        
def set_source(event):
    name=event['request']['intent']['slots']['source']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    if name in map_node.keys():
        global SOURCE
        SOURCE = name
        speech_msg = "Successfully added " + name + " as Source location"
        reprompt_MSG = "Where do you want to go?"
        return output_json_builder_with_reprompt_and_card(speech_msg, reprompt_MSG, False)
    else:
        wrongname_MSG = "You haven't given a valid location. Say Help for more details."
        reprompt_MSG = "Say Set source as to give a source location"
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, reprompt_MSG, False)
        
def stop_the_skill(event):
    stop_MSG = "Thank you. Bye!"
    reprompt_MSG = ""
    return output_json_builder_with_reprompt_and_card(stop_MSG,reprompt_MSG, True)
    
def assistance(event):
    selected_nodes = [name for name,num in map_node.items() if name!=""]
    selected_nodes = selected_nodes[:10]
    assistance_MSG = "You can choose any main building location from " + ",".join(selected_nodes)
    reprompt_MSG = "Are you looking for a main building location?"

    return output_json_builder_with_reprompt_and_card(assistance_MSG,  reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Are you looking for a campus location?"
    return output_json_builder_with_reprompt_and_card(fallback_MSG, reprompt_MSG, False)

#------------------------------Part4--------------------------------
# The response of our Lambda function should be in a json format. 

def getPath(destination,source):
    src_number = map_node[source]
    if destination:
        dest_number = map_node[destination]
        floor_navigation = ""
        if dest_number == 23 :
            dest_number = 1
            floor_navigation = " Take the stairs to reach the first floor. Turn left. Walk straight. You have now arrived at Director's Office."
        elif dest_number == 11:
            dest_number = 13
            floor_navigation = " Take the stairs to reach the first floor. Turn left.You have now arrived at Library."
        distance, path, directions, directions_text = graph.dijkstra(src_number, dest_number)
        directions_text = directions_text + floor_navigation
        return directions_text
    return ""

def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict


def response_field_builder_with_reprompt_and_card(outputSpeach_text, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text,reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, reprompt_text, value)
    return response_dict