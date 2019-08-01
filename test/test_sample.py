# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 08:47:05 2019

"""

import pytest
def test_file1_method1():
	x=5
	y=6
	assert x+1 == y,"test failed"
	assert x == y,"test failed"
def test_file1_method2():
	x=5
	y=6
	assert x+1 == y,"test failed" 