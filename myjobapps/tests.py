__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."

import unittest
from models import *

class ModelEmailMessage(unittest.TestCase):

    def testGetSubjectFreeOfPrefixes(self):
        self.assertEquals(EmailMessage(Subject='Re: job offer').getSubjectFreeOfPrefixes(), 'job offer')
        self.assertEquals(EmailMessage(Subject='[Fwd: Next World Cafe: Friday 28th August + live music]').getSubjectFreeOfPrefixes(), 'Next World Cafe: Friday 28th August + live music')
        self.assertEquals(EmailMessage(Subject='FW: How\'s life stranger?').getSubjectFreeOfPrefixes(), 'How\'s life stranger?')
