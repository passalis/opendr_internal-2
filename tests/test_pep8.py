#!/usr/bin/env python

# Copyright 2020-2021 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test module of the PEP8 format in the tests."""
import unittest

import fnmatch
import os
import sys
from io import open  # needed for compatibility with Python 2.7 for open(file, encoding='utf-8')

from flake8.api import legacy as flake8

skippedDirectories = [
    '.git',
    'dependencies',
    'lib'
]


class TestCodeFormat(unittest.TestCase):
    """Unit test of the PEP8 format in the tests."""

    def setUp(self):
        """Get all the world file."""
        self.files = []
        for rootPath, dirNames, fileNames in os.walk(os.environ['OPENDR_HOME']):
            for fileName in fnmatch.filter(fileNames, '*.py'):
                shouldContinue = False
                for directory in skippedDirectories:
                    currentDirectories = rootPath.replace(os.environ['OPENDR_HOME'], '').replace(os.sep, '/')
                    if directory in currentDirectories:
                        shouldContinue = True
                        break
                if shouldContinue:
                    continue
                filePath = os.path.join(rootPath, fileName)
                if sys.version_info[0] < 3:
                    with open(filePath) as file:
                        if file.readline().startswith('#!/usr/bin/env python3'):
                            continue
                self.files.append(filePath)

    def test_pep8_conformance(self):
        """Test that the tests are PEP8 compliant."""
        style_guide = flake8.get_style_guide(
            ignore=['E121', 'E126', 'E722', 'E741', 'W504'],
            select=['E', 'W', 'F'],
            max_line_length=128,
            format='pylint',
        )
        reporter = style_guide.check_files(self.files)
        self.assertTrue(
          reporter.total_errors == 0,
          msg='PEP8 errors: %d' % (reporter.total_errors)
        )


if __name__ == '__main__':
    unittest.main()
