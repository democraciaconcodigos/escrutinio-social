import cStringIO
import os
import pep8
import sys

from collections import defaultdict

from django.test import TestCase
from pyflakes.scripts.pyflakes import checkPath

import escrutiniosocial
import core


PACKAGES = [escrutiniosocial, core]


class Pep8ConformanceTestCase(TestCase):

    exclude = ['migrations']

    def setUp(self):
        super(Pep8ConformanceTestCase, self).setUp()
        self.errors = {}
        self.pep8style = pep8.StyleGuide(
            counters=defaultdict(int),
            doctest='',
            exclude=self.exclude,
            filename=['*.py'],
            ignore=[],
            messages=self.errors,
            repeat=True,
            select=[],
            show_pep8=False,
            show_source=False,
            max_line_length=79,
            quiet=0,
            statistics=False,
            testsuite='',
            verbose=0
        )

    def test_pep8_conformance(self):
        for package in PACKAGES:
            self.pep8style.input_dir(os.path.dirname(package.__file__))
        self.assertEqual(self.pep8style.options.report.total_errors, 0)


class PyflakesAnalysisTestCase(TestCase):

    def test_pyflakes_analysis(self):
        old_stdout = sys.stdout
        sys.stdout = cStringIO.StringIO()
        self.addCleanup(setattr, sys, 'stdout', old_stdout)

        for package in PACKAGES:
            self._run_pyflakes_analysis(package)

        errors = sys.stdout.getvalue().splitlines()
        self.assertEqual(errors, [], '\n'.join(errors))

    def _run_pyflakes_analysis(self, package):
        package_path = os.path.dirname(package.__file__)
        for dir_path, dir_names, file_names in os.walk(package_path):
            for file_name in file_names:
                if file_name.endswith('.py'):
                    file_path = os.path.join(dir_path, file_name)
                    checkPath(file_path)
