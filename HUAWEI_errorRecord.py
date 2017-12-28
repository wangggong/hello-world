import sys

def report(line, filenames, line_nums, counts, rep_num):
    filename, line_num = line.split()
    filename = filename[-16:].split('\\')[-1]
    
    for i, f in enumerate(filenames):
        if filename == f and line_num == line_nums[i]:
            counts[i] += 1
            rep_num += [i]
            return
    
    filenames += [filename]
    line_nums += [line_num]
    counts += [1]
    rep_num += [len(filenames) - 1]


def print_reports(filenames, line_nums, counts, rep_num):
    m = 0 if len(rep_num) < 8 else len(rep_num) - 8
    while m < len(rep_num):
        print '{} {} {}'.format(filenames[rep_num[m]], line_nums[rep_num[m]], counts[rep_num[m]])
        m += 1


filenames, line_nums, counts, rep_nums = [], [], [], []
for line in sys.stdin.readlines():
    report(line, filenames, line_nums, counts, rep_nums)
    print filenames, line_nums, counts, rep_nums
print_reports(filenames, line_nums, counts, rep_nums)
