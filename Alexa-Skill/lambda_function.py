#------------------------------Part1--------------------------------
# In this part we import necessary graph files and initialize our graph
from src.Graph import Graph,initialize_map, get_image_mapping
from googletrans import Translator
import requests

translator = Translator()

nodes,map_node = initialize_map('src/nodes.json')
images = get_image_mapping('src/image_file_mapping.json')
graph = Graph(len(nodes), nodes)
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
        return on_end(event)
        
#------------------------------Part3--------------------------------
# Here we define the Request handler functions
def on_start():
    print("Session Started.")

def on_launch(event):
    onlaunch_MSG = ""
    reprompt_MSG = ""
    if event['request']['locale'] == "hi-IN":
        onlaunch_MSG = "वी जे टी आई में आपका स्वागत है! आप कहाँ जाना चाहते हैं?" 
        reprompt_MSG = "आप कहाँ जाना चाहते हैं?"
    else:
        onlaunch_MSG = "Welcome to VJTI! Where do you want to go?" 
        reprompt_MSG = "Where do you want to go?"
    return output_json_builder_with_reprompt_and_card(onlaunch_MSG, reprompt_MSG, False)

def on_end(event):
    stop_MSG = ""
    if event['request']['locale'] == "hi-IN":
        stop_MSG = "अभी के लिए अलविदा अगर आपको मदद चाहिए तो आप मुझे फिर से जगा सकते हैं"
    else:
        stop_MSG = "Bye For Now! Feel free to call me again if you want help"
    reprompt_MSG = ""
    return output_json_builder_with_reprompt_and_card(stop_MSG,reprompt_MSG, True)
    print("Session Ended.")

#-----------------------------Part3.1-------------------------------
# The intent_scheme(event) function handles the Intent Request
def intent_scheme(event):
    intent_name = ""
    try:
        intent_name = event['request']['intent']['name']
    except:
        return fallback_call(event)
    if intent_name == "DirectionIntent":
        return direction(event)
    elif intent_name == "SourceIntent":
        return set_source(event)
    elif intent_name == "GreetingIntent":
        return greet(event)
    elif intent_name == "WashroomIntent" :
        return washroom(event)
    elif intent_name == "WashroomTypeIntent":
        return washroom_path(event)
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "WhereAmI":
        return where_am_i(event)
    
    return fallback_call(event)
    
#---------------------------Part3-------------------------------
# intent handler functions
def direction(event):
    name = ""
    uttered_name = ""
    try:
        name=event['request']['intent']['slots']['destination']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
        uttered_name = event['request']['intent']['slots']['destination']['value']
    except:
        if event['request']['locale'] == "hi-IN":
            wrongname_MSG = "आपने कोई मान्य स्थान नहीं दिया है। अधिक जानकारी के लिए मदद कहें।"
            reprompt_MSG = "आप कहाँ जाना चाहते हैं  ?"
        else:
            wrongname_MSG = "You haven't given a valid location. Say Help for more details."
            reprompt_MSG = "Where do you want to go"
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, reprompt_MSG, False)
    
    isAPL = supportsAPL(event)
    speech_msg =""
    reprompt_MSG = ""
    wrongname_MSG = ""
    global SOURCE
    if SOURCE:
        if name in map_node.keys():
            directions,src_number,dest_number = getPath(destination=name,source=SOURCE)
            image = str(src_number) + "-" + str(dest_number) + ".jpg"
            if event['request']['locale'] == "hi-IN":
                directions = directions.replace("Take the next Left","take the next left turn")
                directions = directions.replace("Take the next Right","take the next right turn") 
                response = translator.translate(directions,src='en', dest='hi')
                speech_msg = uttered_name  + "  के लिए रास्ता इस तरह है:  " + response.text
                reprompt_MSG =   "क्या आप किसी और जगह की तलाश कर रहे थे?"
            else:
                speech_msg = "Fetching directions for " + uttered_name + ":  " + directions
                reprompt_MSG = "Did you want directions to some other place, please say which one?"
            return output_json_builder_with_reprompt_and_card(speech_msg, reprompt_MSG, False, isAPL, image)
        else:
            if event['request']['locale'] == "hi-IN":
                wrongname_MSG = "आपने कोई मान्य स्थान नहीं दिया है। अधिक जानकारी के लिए मदद कहें।"
                reprompt_MSG = "आप कहाँ जाना चाहते हैं  ?"
            else:
                wrongname_MSG = "You haven't given a valid location. Say Help for more details."
                reprompt_MSG = "Where do you want to go"
            return output_json_builder_with_reprompt_and_card(wrongname_MSG, reprompt_MSG, False)
    else:
        if event['request']['locale'] == "hi-IN":
            speech_msg = "इस वक़्त मैं कहाँ हूँ ?"
            reprompt_MSG = "कुछ ऐसा कहिये : तुम main staircase के पास हो "
        else:
            speech_msg = "Set source location"
            reprompt_MSG = "Say Set source as to give a source location"
        return output_json_builder_with_reprompt_and_card(speech_msg, reprompt_MSG, False)

        
def set_source(event):
    name=event['request']['intent']['slots']['source']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    uttered_name = event['request']['intent']['slots']['source']['value']
    reprompt_MSG = ""
    if name in map_node.keys():
        global SOURCE
        SOURCE = name
        speech_msg = ""
        if event['request']['locale'] == "hi-IN":
            speech_msg = "स्रोत स्थान के रूप में सफलतापूर्वक  "+ uttered_name  +  "  सेट किया गया है "
            reprompt_MSG = "आप कहाँ जाना चाहते हैं  ?"
        else: 
            speech_msg = "Successfully added " + uttered_name + " as Source location"
            reprompt_MSG = "Where do you want to go?"
        return output_json_builder_with_reprompt_and_card(speech_msg, reprompt_MSG, False)
    else:
        wrongname_MSG = ""
        if event['request']['locale'] == "hi-IN":
            wrongname_MSG = "आपने कोई मान्य स्थान नहीं दिया है। अधिक जानकारी के लिए मदद कहें।" 
            reprompt_MSG = "कुछ ऐसा कहिये : तुम main staircase के पास हो "
        else:
            wrongname_MSG = "You haven't given a valid location. Say Help for more details."
            reprompt_MSG = "Say Set source as to give a source location"
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, reprompt_MSG, False)
        
def greet(event):
    greet_MSG = ""
    reprompt_MSG = ""
    if event['request']['locale'] == "hi-IN": 
        greet_MSG = "नमस्ते, आप कहाँ जाना चाहते हैं  ?"
        reprompt_MSG = "आप कहाँ जाना चाहते हैं  ?"
    else:
        greet_MSG = "Hi, where do you wish to go?"
        reprompt_MSG = "Where do you want to go?"
    return output_json_builder_with_reprompt_and_card(greet_MSG, reprompt_MSG, False)
    
def washroom(event):
    speech_MSG = ""
    reprompt_MSG = ""
    if SOURCE:
        if event['request']['locale'] == "hi-IN":
            speech_MSG = "आप किस वॉशरूम की तलाश में हैं - महिला या पुरुष?"
            reprompt_MSG = "महिला या पुरुष कहें"
        else:
            speech_MSG = "Which washroom are you looking for - Women's or Men's ?"
            reprompt_MSG = "Say Women's or Men's"
        return output_json_builder_with_reprompt_and_card(speech_MSG, reprompt_MSG, False)
    else:
        if event['request']['locale'] == "hi-IN":
            speech_MSG = "इस वक़्त मैं कहाँ हूँ ?"
            reprompt_MSG = "कुछ ऐसा कहिये : तुम main staircase के पास हो "
        else:
            speech_MSG = "Set source location"
            reprompt_MSG = "Say Set source as to give a source location"
        return output_json_builder_with_reprompt_and_card(speech_MSG, reprompt_MSG, False)
    
def washroom_path(event):
    global SOURCE
    isAPL = supportsAPL(event)
    gender = event['request']['intent']['slots']['type']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    washroom_number = findDestinationForWashroom("washroom",SOURCE,gender)
    src_number = map_node[SOURCE]
    image = str(map_node[SOURCE])+"-"+str(washroom_number) + ".jpg"
    distance, path, _, directions = graph.dijkstra(src_number, washroom_number)
    speech_MSG = ""
    reprompt_MSG = ""
    if event['request']['locale'] == "hi-IN":
        directions = directions.replace("Take the next Left","take the next left turn")
        directions = directions.replace("Take the next Right","take the next right turn") 
        response = translator.translate(directions,src='en', dest='hi')
        speech_MSG = "Washroom"  + "  के लिए रास्ता इस तरह है:  " + response.text
        reprompt_MSG =   "क्या आप किसी और जगह की तलाश कर रहे थे?"
    else:
        speech_MSG = "Fetching directions for nearest washroom : "  + directions
        reprompt_MSG = "Did you want directions to some other place, please say which one?"

    return output_json_builder_with_reprompt_and_card(speech_MSG, reprompt_MSG, False, isAPL, image)
    
def where_am_i(event):
    global SOURCE
    speech_msg = ""
    reprompt_MSG = ""
    if SOURCE:
        if event['request']['locale'] == "hi-IN":
            speech_msg = "आप यहां हैं" + SOURCE
            reprompt_MSG = "क्या आप जानना चाहते हैं कि आप कहां हैं?"
        else:
            speech_msg = "You are at " + SOURCE
            reprompt_MSG = "Do you want to know where you are?"
        return output_json_builder_with_reprompt_and_card(speech_msg, reprompt_MSG, False)
    else:
        if event['request']['locale'] == "hi-IN":
            speech_msg = "स्रोत सेट नहीं किया गया है। स्रोत को स्रोत स्थान देने के लिए सेट करें के रूप में कहें"
            reprompt_MSG = "कुछ ऐसा कहिये : तुम main staircase के पास हो "
        else:
            speech_msg = "Source has not been set. Say Set source as to give a source location"
            reprompt_MSG = "Would you like to set source location? Say Set source as to give a source location"
        return output_json_builder_with_reprompt_and_card(speech_msg, reprompt_MSG, False)
    
def stop_the_skill(event):
    stop_MSG = ""
    if event['request']['locale'] == "hi-IN":
        stop_MSG = "अभी के लिए अलविदा अगर आपको मदद चाहिए तो आप मुझे फिर से जगा सकते हैं"
    else:
        stop_MSG = "Bye For Now! Feel free to call me again if you want help"
    reprompt_MSG = ""
    return output_json_builder_with_reprompt_and_card(stop_MSG,reprompt_MSG, True)
    print("Session Ended.")

    
def assistance(event):
    #selected_nodes = [name for name,num in map_node.items() if name!=""]
    #selected_nodes = selected_nodes[:10]
    selected_nodes = ["Comps Department", "CCF1" , "Library", "DEP 1", "Canteen", "Auditorium", "Quad", "Lab 3"]
    assistance_MSG = ""
    reprompt_MSG = ""
    if event['request']['locale'] == "hi-IN":
        assistance_MSG = "आप कोई भी main बिल्डिंग की जगह कह सकते हैं जैसे की  " + ",".join(selected_nodes)
        reprompt_MSG = "क्या आप main  बिल्डिंग की कोई जगह ढूंढ रहे हैं ?"
    else :
        assistance_MSG = "You can choose any campus location from " + ",".join(selected_nodes)
        reprompt_MSG = "Are you looking for a location in V J T I?"

    return output_json_builder_with_reprompt_and_card(assistance_MSG,  reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = ""
    reprompt_MSG = ""
    if event['request']['locale'] == "hi-IN":
        fallback_MSG = "सॉरी , मैं आपकी मदद नहीं कर सकती , प्रश्न बदलने की कोशिश करें या मदद कहें "
        reprompt_MSG = "क्या आप main  बिल्डिंग की कोई जगह ढूंढ रहे है"
    else:
        fallback_MSG = "Sorry, I can't help you with that, try rephrasing the question or ask for help by saying HELP."
        reprompt_MSG = "Are you looking for a campus location?"
    return output_json_builder_with_reprompt_and_card(fallback_MSG, reprompt_MSG, False)

#------------------------------Part4--------------------------------
# The response of our Lambda function should be in a json format. 

def supportsAPL(event):
    if event['context'] and event['context']['System'] and event['context']['System']['device'] :
        supportedInterfaces = event['context']['System']['device']['supportedInterfaces']
        if supportedInterfaces and ( 'Alexa.Presentation.APL' in supportedInterfaces.keys() ):
            aplInterface = supportedInterfaces['Alexa.Presentation.APL']
            if aplInterface != {} and aplInterface != None:
                    return True
    return False
    
def findDestinationForWashroom(dest,src=SOURCE, gender="girls"):
    all_dests = []
    dist = []
    if(dest=="washroom"):
        for i in range(len(nodes)):
            if "washroom" in nodes[i].name and gender in nodes[i].name:
                all_dests.append(nodes[i])
                dist.append(graph.calculateDistance(map_node[src], nodes[i].number))
    else:
        for i in range(len(nodes)):
            if dest in nodes[i].name :
                all_dests.append(nodes[i])
                dist.append(graph.calculateDistance(map_node[src], nodes[i].number))

    dest = all_dests[dist.index(min(dist))]
    return dest.number
    


def getPath(destination,source=SOURCE):
    src_number = map_node[source]
    if destination:
        dest_number = map_node[destination]
        floor_navigation = ""
        if dest_number == 23 :
            dest_number = 1
            floor_navigation = " Take the stairs to reach the first floor. Turn left. Walk straight. You have now arrived at Director's Office."
        elif dest_number == 11:
            dest_number = 10
            floor_navigation = " Take the stairs to reach the first floor. Turn left.You have now arrived at Library."
        distance, path, directions, directions_text = graph.dijkstra(src_number, dest_number)
        directions_text = directions_text + floor_navigation
        return directions_text,src_number,dest_number
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


def response_field_builder_with_reprompt_and_card(outputSpeach_text, reprompt_text, value, image_url = None):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    if image_url:
        speech_dict['directives'] = [{
        "type": "Alexa.Presentation.APL.RenderDocument",
        "token": "mapToken",
        "document": {
            "type": "APL",
            "version": "1.4",
            "settings": {},
            "theme": "light",
            "import": [],
            "resources": [],
            "styles": {},
            "onMount": [],
            "graphics": {},
            "commands": {},
            "layouts": {},
            "mainTemplate": {
                "parameters": [
                    "payload"
                ],
                "items": [
                    {
                        "type": "Container",
                        "items": [
                            {
                                "type": "Image",
                                "height": "100%",
                                "width": "100%",
                                "source": image_url
                            }
                        ],
                        "height": "100%",
                        "width": "100%"
                    }
                ]
            }
        },
        "datasources": {}
        }
        ]
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text,reprompt_text, value, isAPL=False, image=None):
    response_dict = {}
    response_dict['version'] = '1.0'
    if isAPL and image:
        if image in images.keys():
            image_url = "https://drive.google.com/uc?export=view&id=" + images[image]
            status_code  = requests.head(image_url).status_code
            if status_code != 404 or status_code != 403 :
                response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, reprompt_text, value, image_url)
                return response_dict
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, reprompt_text, value)
    return response_dict