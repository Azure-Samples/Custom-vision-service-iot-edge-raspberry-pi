import unittest
import json
import sys
sys.path.insert(0, '../')
import app.MessageParser

class UnitTests(unittest.TestCase):
    def test_HighestProbabilityTagMeetingThreshold(self):
        MessageParser = app.MessageParser.MessageParser()
        message1=json.loads("[{\"Tag\": \"banana\",\"Probability\": 0.4}, {\"Tag\": \"apple\",\"Probability\": 0.3}]")
        self.assertEqual(MessageParser.highestProbabilityTagMeetingThreshold(message1, 0.5), 'none')
        message2=json.loads("[{\"Tag\": \"banana\",\"Probability\": 0.4}, {\"Tag\": \"apple\",\"Probability\": 0.5}]")
        self.assertEqual(MessageParser.highestProbabilityTagMeetingThreshold(message2, 0.3), 'apple')
        message3=json.loads("[{\"Probability\": 0.038001421838998795, \"Tag\": \"apple\"}, {\"Probability\": 0.38567957282066345, \"Tag\": \"banana\"}]")
        self.assertEqual(MessageParser.highestProbabilityTagMeetingThreshold(message3, 0.3), 'banana')

if __name__ == '__main__':
    unittest.main()