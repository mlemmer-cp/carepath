class Symptoms:

    def __init__(self):
        self.possibleAreaIndex = 0
        self.mainSymptomIndex = 0
        self.followSymptomIndex = 0
        self.areas = ["Head and/or Neck", "Arms", "Digestive System", "Respiratory System", "Half of Body", "Skin"]
        #if list is of len = 0, yes results in ER response.
        self.symptomsDict = {"a fever": ["a stiff neck and headache with", "medication not working on"],
                    "headache": ["an unusual", "an abnormally bad"], \
                    "trouble breathing": ["moderate or severe"], 
                    "dizziness or weakness": ["persistent", "sudden, on one side,"], 
                    "confusion": ["sudden"], 
                    "faintness": ["any fainting episodes after feeling"], 
                    "speech or voice issues": ["slurred or disoriented speech as part of your", "sudden voice loss, not related to known sickness or overuse, as part of your"], 
                    "vision loss": [], 
                    "mobility loss": [], 
                    "drooping of muscles": ["sudden, on one side,"], 
                    "bleeding": ["any coughing with", "any vomiting with", "heavy"], 
                    "broken or visible bones": [], 
                    "wounds or burns": ["deep", "severe"], 
                    "pain": ["arm or jaw", "severe"], 
                    "hives or swelling": ["moderate or severe"], 
                    "a potential overdose": [], 
                    "any seizures": [], 
                    "vomiting or loose stools": ["persistent"],
                    "any symptoms after exposure to smoke, toxins, or poision": []}
        # always questions always get asked.
        self.always = ["mobility loss", "bleeding", "broken or visible bones", "wounds or burns", "pain", "hives or swelling", "a potential overdose", "any seizures", "any symptoms after exposure to smoke, toxins, or poision"]
        # questions related to head/neck area or should be moved up in the always list of questions
        self.headNeck = ["a fever", "headache", "trouble breathing", "dizziness or weakness", "confusion", "faintness", "speech or voice issues", "vision loss", "vomiting or loose stools"]
        # questions related to digestion or should be moved up in the always list of questions
        self.digest = ["bleeding", "vomiting or loose stools"]
        # questions related to respitory or should be moved up in the always list of questions
        self.respit = ["trouble breathing", "bleeding"]
        # questions related to symptoms on one half of the body only or should be moved up in the always list of questions
        self.sideOnly = ["any seizures", "drooping of muscles", "mobility loss", "vision loss", "speech or voice issues", "dizziness or weakness", "confusion"]
        self.chooseAreas = {"head and/or neck": self.headNeck, "digestive system": self.digest, "respitory system": self.respit, "one half of your body": self.sideOnly}
        self.areas = []

    def numAreas(self):
        return len(self.chooseAreas)

    def getNextArea(self):
        if (self.possibleAreaIndex >= self.numAreas()):
            return None
        possibleAreas = [*self.chooseAreas]
        next = possibleAreas[self.possibleAreaIndex]
        self.possibleAreaIndex += 1
        return next

    def addAreaToInterest(self):
        possibleAreas = [*self.chooseAreas]
        areaList = self.chooseAreas.get(possibleAreas[self.possibleAreaIndex - 1])
        if len(self.areas) == 0:
            self.areas.extend(areaList)
        else:
            for symptom in areaList:
                # Prioritize asking questions that relate to multiple chosen areas first
                if symptom in self.areas:
                    self.areas.remove(symptom)
                    self.areas.insert(0, symptom)
                else:
                    self.areas.append(symptom)

    def addAlwaysAndCondense(self):
        # Add questions that should always be asked as they can relate to the whole body
        self.areas.extend(self.always)
        # Remove duplicates but keep order
        self.areas = sorted(set(self.areas), key=self.areas.index)

    def numSymptomsToCheck(self):
        return len(self.areas)
    
    def getCurrentSymptom(self):
        return self.areas[self.mainSymptomIndex - 1]

    def getNextSymptom(self):
        if self.mainSymptomIndex >= len(self.areas):
            return None
        symptom = self.areas[self.mainSymptomIndex]
        self.mainSymptomIndex += 1
        return symptom
    
    def getFollowUpSymptom(self):
        currentSymptom = self.areas[self.mainSymptomIndex - 1]
        if len(self.symptomsDict[currentSymptom]) == 0:
            return True
        if self.followSymptomIndex >= len(self.symptomsDict[currentSymptom]):
            self.followSymptomIndex = 0
            return None
        symptom = self.symptomsDict[currentSymptom][self.followSymptomIndex]
        self.followSymptomIndex += 1
        return symptom