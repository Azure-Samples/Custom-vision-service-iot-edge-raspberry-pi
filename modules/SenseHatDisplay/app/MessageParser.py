class MessageParser:
    #Returns the highest probablity tag in the json object (takes the output as json.loads as input)
    def highestProbabilityTagMeetingThreshold(self, allTagsAndProbability, threshold):
        highestProbabilityTag = 'none'
        highestProbability = 0
        for item in allTagsAndProbability:
            if item['Probability'] > highestProbability and item['Probability'] > threshold:
                highestProbability = item['Probability']
                highestProbabilityTag = item['Tag']
        return highestProbabilityTag