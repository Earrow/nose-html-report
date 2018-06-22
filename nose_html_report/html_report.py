# coding=utf-8

import os
import json
import traceback
from datetime import datetime

from nose import SkipTest
from nose.plugins import Plugin, skip

from .render import load_template, render_template


class HTMLReport(Plugin):
    name = 'html-report'
    score = skip.Skip.score + 50
    default_template_path = os.path.join(os.path.dirname(__file__), 'templates', 'report.html')

    def __init__(self):
        super().__init__()

        self.test_results = []
        self.results = []
        self.summary_stats = {'总数': 0}
        self.html_file = None
        self.html_report_title = '测试报告'

    def options(self, parser, env=os.environ):
        super().options(parser, env)

        parser.add_option("--html-file", action="store",
                          default=env.get('NOSE_HTML_OUT_FILE', 'results.html'),
                          dest="html_file",
                          metavar="FILE",
                          help="Produce results in the specified HTML file.")
        parser.add_option("--html-title", action="store",
                          default=env.get('NOSE_HTML_TITLE', '测试报告'),
                          dest="html_report_title",
                          metavar="ATTR",
                          help="Title in HTML file.")

    def configure(self, options, conf):
        super().configure(options, conf)

        if options.html_file:
            self.html_file = options.html_file

        if options.html_report_title:
            self.html_report_title = options.html_report_title

    def begin(self):
        self.startTime = datetime.now()

    def addSuccess(self, test):
        output = test.shortDescription() or test.id()

        if '通过' in self.summary_stats:
            self.summary_stats['通过'] += 1
        else:
            self.summary_stats['通过'] = 1
        self.summary_stats['总数'] += 1

        self.test_results.append((0, test, output, ''))

    def addFailure(self, test, err):
        output = test.shortDescription() or test.id()
        err_str = self.formatErr(err)

        if '失败' in self.summary_stats:
            self.summary_stats['失败'] += 1
        else:
            self.summary_stats['失败'] = 1
        self.summary_stats['总数'] += 1

        self.test_results.append((1, test, output, err_str))

    def addError(self, test, err):
        output = test.shortDescription() or test.id()

        if err[0] != SkipTest:
            err_str = self.formatErr(err)

            if '出错' in self.summary_stats:
                self.summary_stats['出错'] += 1
            else:
                self.summary_stats['出错'] = 1

            self.test_results.append((2, test, output, err_str))
        else:
            if '跳过' in self.summary_stats:
                self.summary_stats['跳过'] += 1
            else:
                self.summary_stats['跳过'] = 1

            self.test_results.append((3, test, output, ''))

        self.summary_stats['总数'] += 1

    def formatErr(self, err):
        exception_type, exception_message, exception_traceback = err
        return ''.join(
            traceback.format_exception(exception_type, exception_type(exception_message), exception_traceback))

    def report(self, stream):
        for cid, (cls, cls_results) in enumerate(self._sort_result(self.test_results)):
            for n, t, o, e in cls_results:
                if n == 0:
                    result = 'passed'
                elif n == 1:
                    result = 'failed'
                elif n == 2:
                    result = 'error'
                else:
                    result = 'skipped'

                name = t.id()

                doc = t.shortDescription() or ""
                desc = doc or name

                self.results.append({
                    'name': name,
                    'description': desc,
                    'result': result,
                    'traceback': e
                })

        context = {
            'test_report_title': self.html_report_title,
            'test_summary': self.summary_stats,
            'test_results': self.results,
            'autocomplete_terms': json.dumps(self._generate_search_terms()),
            'timestamp': datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S UTC')
        }
        template = load_template(self.default_template_path)
        rendered_template = render_template(template, context)

        if self.html_file:
            with open(self.html_file, 'w') as fp:
                fp.write(rendered_template)

    def _sort_result(self, result_list):
        rmap = {}
        classes = []
        for n, t, o, e in result_list:
            if hasattr(t, '_tests'):
                for inner_test in t._tests:
                    self._add_cls(rmap, classes, inner_test, (n, inner_test, o, e))
            else:
                self._add_cls(rmap, classes, t, (n, t, o, e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def _add_cls(self, rmap, classes, test, data_tuple):
        if hasattr(test, 'test'):
            cls = test.test.__class__
        else:
            cls = test.__class__
        if cls not in rmap:
            rmap[cls] = []
            classes.append(cls)
        rmap[cls].append(data_tuple)

    def _generate_search_terms(self):
        search_terms = {}

        for test_result in self.results:
            search_terms[test_result['name']] = test_result['name']
            search_terms[test_result['description']] = test_result['name']

        return search_terms
