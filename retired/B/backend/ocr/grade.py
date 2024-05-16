"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai

genai.configure(api_key="AIzaSyCyQnyQE_TFTi7HDIVscRI_o8nFb3Qc_DI")

# Set up the model
generation_config = {
  "temperature": 0.7,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

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
  "My answer: Disaster Risk Reduction:- It includes all activities, techniques involved in the reduction of risk or the chance and probability that a disaster will occur.Early Warning System:- It is a system put in place by the government to warn civilians or those people in immediate danger about a natural disaster (flood, tsunami, cyclones etc.) is about to occur. - Early Warning Systems are very important for disaster risk reduction since:- . They assist in evacuation of people from high risk areas, reducing the chances of loss of life.- Reduces Monetary or financial losses in case of less severe disasters since it gives people time to prepare, e.g., for landslides or cyclones.- Assists in informing the people of the severity of the disaster hazard",
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
  "My answer: ★ Participating disaster risk management in the context of stakeholders, organisations, suffers by the disaster and who are affected by a disaster and action plan in case of risks. * They are classified into three.   * Primary stakeholders - These include people directly affected by a disaster. eg local residents etc  * Secondary stakeholders - These include organisations and institutions that can help and respond to disasters and bring in resources and finance. These include the government, local authorities etc* Key stakeholders - These are other organisations like NGO's that can act during a disaster. * Proper communication with stakeholders are necessary to understand the depth of risk for each stakeholder. Measures are taken for proper participation of stakeholders to build a contingency plan. Some include mandatory participation, sessional meetings with different stakeholders etc",
  "Answer key: explain participatory stakeholder engagement - 2 Mark .\nImportance's and Need Of  participatory stakeholder engagement - 3 Mark.",
  "Maxscore: 5",
  "score: ",
]

response = model.generate_content(prompt_parts)
print(response.text)
