
import google.generativeai as genai
import csv

genai.configure(api_key="AIzaSyCyQnyQE_TFTi7HDIVscRI_o8nFb3Qc_DI")

# Set up the model
generation_config = {
  "temperature": 0.5,
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

response = model.generate_content(dataset[0]+l4)
print(response.text)
mark.append(response.text)

print(mark)
