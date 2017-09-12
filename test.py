import unittest
from scripts.gamecomponents.tests.test_TestPhysicsObject import TestPhysicsObject
from scripts.gamecomponents.tests.test_TestVector import TestVector
from scripts.gamecomponents.tests.TestDisc import TestDisc

runner = unittest.TextTestRunner()
runner.run(unittest.makeSuite(TestVector))
runner.run(unittest.makeSuite(TestPhysicsObject))
runner.run(unittest.makeSuite(TestDisc))