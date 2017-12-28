from collections import OrderedDict
import sys

def report(line, reports):
    filename, line_num = line.split()
    filename = filename.split('\\')[-1]
    key = (filename, line_num)
    reports[key] = reports.get(key, 0) + 1


def print_reports(reports):
    m = 0 if len(reports) < 8 else len(reports) - 8
    for k, v in reports.items()[m:]:
        filename, line_num = k
        filename = filename if len(filename) <= 16 else filename[-16:]
        print '{} {} {}'.format(filename, line_num, v)


reports = OrderedDict()
for line in sys.stdin.readlines():
    report(line, reports)
    print reports
print_reports(reports)
