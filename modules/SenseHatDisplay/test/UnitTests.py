import unittest
import json
import sys
sys.path.insert(0, '../')
import app.MessageParser

class UnitTests(unittest.TestCase):
    def test_HighestProbabilityTagMeetingThreshold(self):
        MessageParser = app.MessageParser.MessageParser()
        message1 = json.loads(
            "{\"iteration\": \"\",\"id\": \"\",\"predictions\": [{\"probability\": 0.3,\"tagName\": \"Apple\",\"tagId\": \"\",\"boundingBox\": null},{\"probability\": 0.4,\"tagName\": \"Banana\",\"tagId\": \"\",\"boundingBox\": null}],\"project\": \"\",\"created\": \"2019-12-10T04:37:49.657555\"}")
        self.assertEqual(
            MessageParser.highestProbabilityTagMeetingThreshold(message1, 0.5), 'none')
        message2 = json.loads(
            "{\"iteration\": \"\",\"id\": \"\",\"predictions\": [{\"probability\": 0.5,\"tagName\": \"Apple\",\"tagId\": \"\",\"boundingBox\": null},{\"probability\": 0.4,\"tagName\": \"Banana\",\"tagId\": \"\",\"boundingBox\": null}],\"project\": \"\",\"created\": \"2019-12-10T04:37:49.657555\"}")
        self.assertEqual(MessageParser.highestProbabilityTagMeetingThreshold(
            message2, 0.3), 'Apple')
        message3 = json.loads(
            "{\"iteration\": \"\",\"id\": \"\",\"predictions\": [{\"probability\": 0.038001421838998795,\"tagName\": \"Apple\",\"tagId\": \"\",\"boundingBox\": null},{\"probability\": 0.38567957282066345,\"tagName\": \"Banana\",\"tagId\": \"\",\"boundingBox\": null}],\"project\": \"\",\"created\": \"2019-12-10T04:37:49.657555\"}")
        self.assertEqual(MessageParser.highestProbabilityTagMeetingThreshold(
            message3, 0.3), 'Banana')


if __name__ == '__main__':
    unittest.main()
