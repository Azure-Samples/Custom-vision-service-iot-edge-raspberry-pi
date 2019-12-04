import app.AnnotationParser
import unittest
import json
import sys
sys.path.insert(0, '../')
# pylint: disable=E0401


class UnitTests(unittest.TestCase):
    def test_getCV2RectanglesFromProcessingService1(self):
        AnnotationParser = app.AnnotationParser.AnnotationParser()
        response = json.loads(
            "{\"language\":\"en\",\"textAngle\":0,\"orientation\":\"Up\",\"regions\":[{\"boundingBox\":\"400,560,3272,288\",\"lines\":[{\"boundingBox\":\"400,560,3272,288\",\"words\":[{\"boundingBox\":\"400,560,672,280\",\"text\":\"word1\"},{\"boundingBox\":\"1200,568,216,272\",\"text\":\"word2\"}]}]}]}")
        self.assertEqual(AnnotationParser.getCV2RectanglesFromProcessingService1(
            response), [[560, 400, 3832, 688]])

    def test_getCV2RectanglesFromProcessingService2(self):
        AnnotationParser = app.AnnotationParser.AnnotationParser()
        response = json.loads(
            "[{\"Id\": \"c5c24a82-6845-4031-9d5d-978df9175426\",\"rectangle\": {\"top\": 54, \"left\": 394,\"width\": 78,\"height\": 78}}]")
        self.assertEqual(AnnotationParser.getCV2RectanglesFromProcessingService2(
            response), [[394, 54, 472, 132]])


if __name__ == '__main__':
    unittest.main()
