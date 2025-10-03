# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Soft Assertion class

This module is an assertion helper for doing multiple assertions at once and failing the script only
when assertion has finished.

The module contains the following public classes:
    Soft_Assert
"""
import logging
import inspect
import os.path


class SoftAssert:
    log = logging.getLogger()

    def __init__(self):
        self._failed_expectations = []
        self._cnt = 1
        self._fail_messages = []

    def expect(self, expr, msg):
        if not expr:
            self._log_failure(msg)

    def assert_all(self):
        if self._failed_expectations:
            all_msgs = "Assertion failed for below conditions:\n"
            for i, x in enumerate(self._fail_messages, 1):
                all_msgs += str(i) + x + "\n"
            self._report_failures()
            self.log.info(all_msgs)
            assert False, all_msgs

    def _log_failure(self, msg=None):
        (filename, line, func, contextlist) = inspect.stack()[2][1:5]
        filename = os.path.basename(filename)
        context = contextlist[0]
        expect_template = """{0}: Assertion occured in {1}\n at line no {2} - test method{3}\n {4}\n {5} """
        tmp = expect_template.format(
            self._cnt, filename, line, func, context, msg if msg else ""
        )
        self._cnt += 1
        self._failed_expectations.append(tmp)
        msg = " Assertion failed {0}: {1} at line no.{2} due to '{3}'".format(
            filename, func, str(line), str(msg)
        )
        self._fail_messages.append(msg)

    def _report_failures(self):
        if self._failed_expectations:
            _, line, func = inspect.stack()[2][1:4]
            assert_tmpl = (
                "Asserting all expectations: In test {} at line no {}".format(
                    func, line
                )
            )
            assert_count = "Failed expectations:%s" % len(
                self._failed_expectations
            )
            report = [assert_tmpl, assert_count]
            report.extend(self._failed_expectations)
            self._failed_expectations = []
