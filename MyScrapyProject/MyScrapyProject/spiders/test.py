import sys
import os
from sys import path
path.append(os.path.abspath(os.path.dirname(__file__)).split('MyScrapyProject')[0])
import sys

from MyScrapyProject.MyScrapyProject.spiders.StarSpider import ScrapyForUserStarClass

Spider=ScrapyForUserStarClass()
Spider.GetUserStarPics(2,56346048)