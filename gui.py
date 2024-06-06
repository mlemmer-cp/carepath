import streamlit as st
import time
import symptoms as sy
import random

if "sym" not in st.session_state:
    st.session_state.sym = sy.Symptoms()

sym = st.session_state.sym

if "mainSym" not in st.session_state:
    st.session_state.mainSym = True

if "botQues" not in st.session_state:
    st.session_state.botQues = []

if "disabled" not in st.session_state:
    st.session_state.disabled = False

if "messages" not in st.session_state:
    st.session_state.messages = []

def disable():
    st.session_state.disabled = True

def reset_chat():
    st.session_state['messages'] = []
    st.session_state['botQues'] = []
    st.session_state['disabled'] = False
    st.session_state['sym'] = sy.Symptoms()
    st.session_state['mainSym'] = True

intro = "Hello! I'm Pathways, a chatbot to help guide you through questions about the symptoms that led you here and point you towards where to go next.\n\n I'll ask if you've experienced any symptoms in certain locations then ask some questions about those symptoms. I just need a yes or no for an answer.\n\n Accepted responses must include \"Yes\", \"No\", \"N\", or \"Y\" and may be uppercase or lowercase."

def sendMessage(message):
    for word in message.split(" "):
        yield word + " "
        time.sleep(0.08)

def addBotResponse(message):
    st.session_state.messages.append({"role": "Pathways", "avatar": "🩺", "content": message})
    with chatResponseCont.chat_message("Pathways", avatar="🩺"):
                st.write_stream(sendMessage(message))

def addUserResponse(message):
    st.session_state.messages.append({"role": "Pathways", "avatar": "user", "content": message})
    with chatResponseCont.chat_message("user"):
                st.write_stream(sendMessage(message))

def sendER():
    addBotResponse("Based on my notes and your last question, you would be best served at an Emergency Room. Please proceed there now or call 911 for assistance.")
    disable()

def sendUrgent():
    addBotResponse("Based on my notes, you would be best served at an Urgent Care. Please proceed there now or call 911 for assistance.")
    disable()

ready = False

def askAboutMainSymptom():
    symptom = sym.getNextSymptom()
    if symptom is not None:
        message = "Are you experiencing " + symptom + "?"
        addBotResponse(message)
        st.session_state.botQues.append(message)
        st.session_state.mainSym = True
        return True
    else:
        sendUrgent()
    
def askFollowUp():
    followUp = sym.getFollowUpSymptom()
    main = sym.getCurrentSymptom()
    if followUp is True:
        sendER()
        return False
    elif followUp is not None:
        message = "Are you experiencing " + followUp + " " + main + "?: "
        addBotResponse(message)
        st.session_state.botQues.append(message)
        st.session_state.mainSym = False
        return True
    else:
        return None

def nextBotQuestion(answer):
    if answer == "invalid":
        addBotResponse(st.session_state.botQues[-1])
    else:
        if len(st.session_state.botQues) < sym.numAreas() + 1:
            if len(st.session_state.botQues) != 1 and answer:
                sym.addAreaToInterest()
            areaToCheck = sym.getNextArea()
            message = "Are you having issues with your " + areaToCheck + "? "
            addBotResponse(message)
            st.session_state.botQues.append(message)
            return True
        elif len(st.session_state.botQues) == sym.numAreas() + 1:
            if answer:
                sym.addAreaToInterest()

            if sym.numSymptomsToCheck() == 0:
                addBotResponse("Based on my notes, you have indicated you are not having trouble with any areas we specifically evaluate. You will be asked more general questions that could pertain to anywhere on your body.")
                sym.addAlwaysAndCondense()
                askAboutMainSymptom()
                return True
            else:
                sym.addAlwaysAndCondense()
                addBotResponse("Thanks for answering the questions about where you have symptoms. The next questions will ask about your specific symptoms.")
                askAboutMainSymptom()
                return True
        elif len(st.session_state.botQues) > sym.numAreas() + 1:
            if st.session_state.mainSym and answer:
                return askFollowUp()
            elif st.session_state.mainSym and not answer:
                return askAboutMainSymptom()
            elif not st.session_state.mainSym and answer:
                return sendER()
            elif askFollowUp() is None:
                return askAboutMainSymptom()

def handleSubmit():
    input = st.session_state['userInput']
    if input is not None and input != "":
        addUserResponse(input)
        input = input.lower()
        if any(word in ["yes", "y"] for word in input.split(" ")):
            answer = True
            if st.session_state.botQues[-1] == "Ready to begin?":
                response = "Great! Let's begin."
                ready = True
            else:
                response = "I will add this to my notes."
        elif any(word in ["no", "n"] for word in input.split(" ")):
            answer = False
            if st.session_state.botQues[-1] == "Ready to begin?":
                answer = "end"
                response = "Stay safe! Press the reset button in the sidebar to start over."
            else:
                response = random.choice(
                            [
                                "I will add this to my notes.",
                                "Understood. I've got that down.",
                                "Duly noted.",
                            ])
        else:
            answer = "invalid"
            response = "I didn't see a clear yes or no within your response. Can you send it again?"
        addBotResponse(response)
        if answer != "end":
            nextBotQuestion(answer)
        else:
            disable()
        
with st.sidebar:                                    
    st.title("CarePath")
    st.subheader("Solving Where To Go After Hours", divider="rainbow")
    st.write("If at any time your condition becomes life-threatening, stop and call 911.", )
    if st.button("Reset Chat"):
        reset_chat()
        st.rerun()

    with st.expander("Credit"):
         st.write("Developed by Mary Lemmer for Cal Poly's CSC 480 in June of 2024.")
    with st.expander("Bugs"):
        st.write("Notice: There is a known bug if you submit input when the bot is writing the \"Are you having issues with\" questions that it indexes out. \n\nIf any bugs are encountered, click the Reset Chat button above.")

chatResponseCont = st.container(border=True)

for message in st.session_state.messages:
    with chatResponseCont.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    addBotResponse(intro)
    addBotResponse("Ready to begin?")
    st.session_state.botQues.append("Ready to begin?")

if not st.session_state['disabled']:
    st.chat_input("Type 'Yes', 'No', 'N', or 'Y'", key="userInput", on_submit=handleSubmit)
else:
    st.chat_input("Type 'Yes', 'No', 'N', or 'Y'", disabled=True)
        