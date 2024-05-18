import google.generativeai as genai
import csv

import os
from dotenv import load_dotenv
load_dotenv() # Load from .env file

genai.configure(api_key=os.getenv('GEMINI_API'))

# Set up the model
generation_config = {"temperature": 0.5,"top_p": 1,"top_k": 1,"max_output_tokens": 2048,}

safety_settings = [
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",generation_config=generation_config,safety_settings=safety_settings)

'''
#question and answer 1
l1=["My answer: Participating disaster risk management in the context of stakeholders, organisations, suffers by the disaster and who are affected by a disaster and action plan in case of risks. ",
  "Answer key: explain participatory stakeholder engagement - 2 Mark .\nImportance's and Need Of  participatory stakeholder engagement - 3 Mark.",
  "Maxscore: 5",
  "score: ",]

#question and answer 2
l2=["My answer: Stakeholders are normally the people that are vulnerable to disasters. * Participatory stakeholder engagement refers to the active participation of stakeholders which helps to plan projects that help manage the disasters. * It is important that even the minority group is also involved in the meeting as these groups may be the ones who suffer the most ones disaster occurs.* So it is important that the project should consider all the stakeholders involved its possible or atleast the ones who are most vulnerable must be considered.* If the stakeholders do not actively engage in disaster reduction the project ideas may not be good as not implemented at all and the risk of disaster could be reduced. * Stakeholder participation is important because it allows for management to be achievable ", 
  "Answer key: explain participatory stakeholder engagement - 2 Mark .\nImportance's and Need Of  participatory stakeholder engagement - 3 Mark.",
  "Maxscore: 5",
  "score: ",]

#question and answer 3
l3=["My answer: * Effective communication plays a key role in disaster management and disaster risk reduction.* Some of the main information needs of communication are: * To provide early warning to people - providing early warnings can help people prepare for the upcoming disaster and plan evacuation if needed without putting ones life in danger. * To provide information as a disaster occurred to nearby areas - proper information to nearby areas help them evacuate or take necessary steps to reduce risk of the disaster . * Provide assistance to people who are trapped or isolated.   - proper communication through devices help people rescue teams with correct details on locations provides. * Communication - Be though social media, by word etc. helps to deliver problems to key personnel of the world easily. This can help bring attention to the overlooked by the corrupt such fund raising etc, can be done easily.* Effective communication helps both verbal and non-verbal communication should be there so as to present the issues in details & discreetly to the debate to a particular property or community. As it is most done to market/sell, the details involved and its seriousness.* Some of the ways to communication are - * Social apps, calls, CB radios, police sirens. The discreet communication however to portray clandestine messages.* If communications are done right, it can save a lot of people and also reduce the casualties both before and after a disaster has occured.* Response and relief plans are implemented often on the basis of planning and information of the disaster at hand. This information is mostly obtained through proper communication.* The needs of people after a disaster can only be properly obtained using proper communication else there is a lack of communication the needs may not be satisfied and excess or unwanted items may be brought up.* All these statements show how important is communication in disaster risk management and risk reduction.",
  "Answer key: Explain what is effective communication in disaster management - 3 Mark .\nExplain The need of effective communication - 5 Mark.\nExplain The ways to Improve communication - 5 Mark.\nConclusion - 2 Mark.",
  "Maxscore: 15",
  "score: "]

#question and answer 4
l4=["My answer: Participating disaster risk management in the context of stakeholders, organisations, suffers by the disaster and who are affected by a disaster and action plan in case of risks. * They are classified into three.   * Primary stakeholders - These include people directly affected by a disaster. eg local residents etc  * Secondary stakeholders - These include organisations and institutions that can help and respond to disasters and bring in resources and finance.",
    "Answer key: Explain Disaster response - 1 Mark. Any 5 Methods to improve  disaster response effectiveness - 4 Mark.",
    "Maxscore: 5",
    "score: "]



dataset=[]
with open("data.csv", 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            dataset.append(row)          
mark=[]
response = model.generate_content(dataset[0]+l1)
print(response.text)
mark.append(response.text)

response = model.generate_content(dataset[0]+l2)
print(response.text)
mark.append(response.text)

response = model.generate_content(dataset[0]+l3)
print(response.text)
mark.append(response.text)
'''

def getMark(a, k, m) -> int:
  prompt_parts = [
  "My answer: Early warning systems are an important part of disaster prevention/ mitigation measures. * It is pivotal to help state prepare for disasters to take precautions and prepare for a possible disaster. * Early warning systems are necessary to start preparing relief camps etc. for evacuation during disasters. * This saves lives and reduces loss of property.* In some disasters, time is a major constraint and hence early warning system helps in disaster risk reduction.* Eg:- Tsunami early warning system helps fishermen, to get out of sea, people of low lying areas and coastal areas to move to higher ground. This makes evacuation faster, less lives are affected and people can take their loved ones and important goods along.",
  "Answer key: Explain early warning system   - 1 Mark.\nwhy is early warning system important - 2 Mark .\nexplain how early warning system lead to disaster prevention and mitigation - 2 Mark.",
  "Maxscore: 5",
  "score: 3",
  "My answer: The main objective of disaster response is to save lives. Thus disaster response efforts include preparation of evacuation plans, setting up of relief camps etc.* Disaster response also need to set up proper communication to reduce impact of disaster. * Other objectives include setting up of proper relief camps, distribution of resources, ensuring food, water, shelter to people affected by the disaster. * Psychosocial efforts are also a major part of the relief efforts as it helps people overcome the loss and recover and include setting up emergency meet up places in case of disasters to make evacuation easier.* Search and rescue is a major part of disaster response services. SAR is the method used to search and find the missing people and to bring them to safety.* Medical attention, first aid - setting up of temporary medical units are also part of disaster response efforts.",
  "Answer key: Explain Disaster response  - 1 Mark .\nAny 5 Methods to improve  disaster response effectiveness - 4 Mark .",
  "Maxscore: 5",
  "score: 4",
  "My answer: * Capacity building in context of disaster Risk reduction refers to how effectively people or communities affected by disasters can prepare for and respond to each type of disaster. * It analyses the capacity to deal with each type of possible disaster.",
  "Answer key: Explain Capacity Building. - 2 Mark .\nExplain 2 types of Capacity Building - 3 Mark.",
  "Maxscore: 5",
  "score: 1",
  "My answer: ",
  "Answer key: Explain early warning system - 1 Mark .\nwhy is early warning system important.(2 Mark)\nexplain how early warning system lead to disaster prevention and mitigation - 4 Mark.",
  "Maxscore: 5",
  "score: 0",
  "My answer: Communication * Communication is a vital part of disaster risk reduction.* Communication is involved from early warning system to even counselling of disaster affected people.* Every stage of disaster management cycle involves effective communication.* Communication involves spreading awareness among people to react to any impending kind of disaster * Proper communication channels need to be set up to help in evacuation. Rescue teams need proper communication to carry out evacuation. Search and rescue can be jeopardised if communication lines break down. * Communication methods which are very effective include social media platforms like Facebook, twitter, etc as information can be shared to a large audience at once. * Other channels of communication during rescue efforts include two-way radio, CB radios, walkie-talkies etc.* Police scanners are important in spreading awareness. * Usage of apps like Life360 helps people to coordinate during disasters. * Lan Lines are an underestimated form of communication as many wireless facilities can breakdown. * Satellite phones are another mode of communication.* People to People Communication is very important, especially counselling. This is needed for motivation and to keep the morale high to bring people out of depression and overcome losses of disasters. * Even before disasters, prevention measures involve proper communication between stakeholders to create contingency plans, evacuation measures, priority lists. * Proper use of technology is needed to prevent breaking down of communication channels during disasters.",
  "Answer key: Explain what is effective communication in disaster management - 3 Mark .\nExplain The need of effective communication - 5 Mark.\nExplain The ways to Improve communication - 5 Mark.\nConclusion - 2 Mark.",
  "Maxscore: 15",
  "score: 11",
  "My answer: Disaster Risk Reduction:- It includes all activities, techniques involved in the reduction of risk or the chance and probability that a disaster will occur.Early Warning System:- It is a system put in place by the government to warn civilians or those people in immediate danger about a natural disaster is about to occur. - Early Warning Systems are very important for disaster risk reduction since:- . They assist in evacuation of people from high risk areas, reducing the chances of loss of life.- Reduces Monetary or financial losses in case of less severe disasters since it gives people time to prepare, e.g., for landslides or cyclones.- Assists in informing the people of the severity of the disaster hazard",
  "Answer key: Explain early warning system - 1 Mark.\nwhy is early warning system important - 2 Mark.\nexplain how early warning system lead to disaster prevention and mitigation -2 Mark.",
  "Maxscore: 5",
  "score: 1.5",
  "My answer: Disaster Response :- It comprises of actions taken after disaster has occured to assist or rescue victims and ensure that no further loss of life occurs. types include :- search & rescue, first aid, etc..**Primary objectives :-***   **Risk Reduction:-** Reduce the risk of occurrence or less to risk of any further damage or loss*   **Damage Prevention:-**These objectives are present to completely reach to the goal of Disaster Response:*   Prevent loss of life",
  "Answer key: Explain Disaster response - 1 Mark.\nAny 5 Methods to improve  disaster response effectiveness - 4 Mark.",
  "Maxscore: 5",
  "score: 3",
  "My answer: ★ Participating disaster risk management in the context of stakeholders, organisations, suffers by the disaster and who are affected by a disaster and action plan in case of risks. * They are classified into three.   * Primary stakeholders - These include people directly affected by a disaster. eg local residents etc  * Secondary stakeholders - These include organisations and institutions that can help and respond to disasters and bring in resources and finance. These include the government, local authorities etc* Key stakeholders - These are other organisations like NGO's that can act during a disaster. * Proper communication with stakeholders are necessary to understand the depth of risk for each stakeholder. Measures are taken for proper participation of stakeholders to build a contingency plan. Some include mandatory participation, sessional meetings with different stakeholders etc",
  "Answer key: explain participatory stakeholder engagement - 2 Mark.\nImportance's and Need Of  participatory stakeholder engagement - 3 Mark.",
  "Maxscore: 5",
  "score: 4",
  "My answer: Early warning systems are systems which warn people of a community just before the occurrence of a disaster. * These systems helps the people to take measures to reduce the impact of disaster before it has occured.* These system helps to start evacuation plans, start strategies to minimize the effect of the disaster. * All organizations and government officials are alerted as they can start their initial responses with the help of these warning systems before a disaster occurs.* Doing all these after the occurs of a disaster makes the tasks less effective and harder to implement.* Eg: - before a flood , if the early warning system detects it then evacuation of people,  moving material bodies can be done but after the flood occurs, the evacuation plan and other rescue plans are much harder to implement",
  "Answer key: Explain early warning system   - 1 Mark.\nwhy is early warning system important - 2 Mark .\nexplain how early warning system lead to disaster prevention and mitigation - 2 Mark.",
  "Maxscore: 5",
  "score: 5",
  "My answer: * The primary objectives of disaster response teams are -    * Rescue maximum amount of people from the area of disaster.   * Provide basic needs for the survival of people affected in the disaster, like food, first aid and shelter.    * Start procedures like search and rescue, providing initial first aid, SOPs, psychological support to people who need it.    * Communicate to nearby areas so that they know that a disaster has come so as they start to take measures.   * Communicate to civil society organisations and Non government organisations about the disaster occurence and ask support to those groups.     * The evacuation was not done well. And this is one of the main steps to be done that is to sent as many people out of the area of disaster as soon as possible.",
  "Answer key: Explain Disaster response - 1 Mark.\nAny 5 Methods to improve  disaster response effectiveness - 4 Mark.",
  "Maxscore: 5",
  "score: 5",
  "My answer: *Capacity building refers to the term to take apt measures and store more resources and knowledge to face a disaster. *There are 2 types of capacity building - *physical capacity building refers to use of physical constructs to reduce the risk of disasters.*Building houses using particular materials to protect it from disaster, building retaining walls to protect from landslides are some examples of physical capacity to reduce risk of disasters.*Non structural capacity building refers to the collective knowledge to be given to the affected at hand. Conducting mock drills, demo evacuation plans etc are some examples.*These capacity building focuses on involving as much people, teaching them how to act at the time of a disaster etc.",
  "Answer key: Explain Capacity Building. - 2 Mark .\nExplain 2 types of Capacity Building - 3 Mark.",
  "Maxscore: 5",
  "score: 4",
  "My answer: * Effective communication plays a key role in disaster management and disaster risk reduction.* Some of the main information needs of communication are: * To provide early warning to people - providing early warnings can help people prepare for the upcoming disaster and plan evacuation if needed without putting ones life in danger. * To provide information as a disaster occurred to nearby areas - proper information to nearby areas help them evacuate or take necessary steps to reduce risk of the disaster . * Provide assistance to people who are trapped or isolated.   - proper communication through devices help people rescue teams with correct details on locations provides. * Communication - Be though social media, by word etc. helps to deliver problems to key personnel of the world easily. This can help bring attention to the overlooked by the corrupt such fund raising etc, can be done easily.* Effective communication helps both verbal and non-verbal communication should be there so as to present the issues in details & discreetly to the debate to a particular property or community. As it is most done to market/sell, the details involved and its seriousness.* Some of the ways to communication are - * Social apps, calls, CB radios, police sirens. The discreet communication however to portray clandestine messages.* If communications are done right, it can save a lot of people and also reduce the casualties both before and after a disaster has occured.* Response and relief plans are implemented often on the basis of planning and information of the disaster at hand. This information is mostly obtained through proper communication.* The needs of people after a disaster can only be properly obtained using proper communication else there is a lack of communication the needs may not be satisfied and excess or unwanted items may be brought up.* All these statements show how important is communication in disaster risk management and risk reduction.",
  "Answer key: Explain what is effective communication in disaster management - 3 Mark .\nExplain The need of effective communication - 5 Mark.\nExplain The ways to Improve communication - 5 Mark.\nConclusion - 2 Mark.",
  "Maxscore: 15",
  "score: 15",
  ]

  prompt_parts.extend([
    "My answer: " + a,
    "Answer key: " + k,
    "Maxscore: " + str(m),
    "score: ",
  ])

  mark = int(str(model.generate_content(prompt_parts).text))

  return mark 


if __name__ == "__main__":
  print(getMark("hello", "hello world", 5))
