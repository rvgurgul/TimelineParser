from collections import Counter
from Stats import statistic_report, DEFAULT_DUMP_STATISTICS


def unpack(box):
    arr = []
    for x in box:
        for y in x:
            arr.append(y)
    return arr


def occurrences(arr, ascending=False):
    cts = Counter(arr)
    return sorted([(cts[x], x) for x in cts], reverse=not ascending)


def occurrence_report(arr, ascending=False, threshold_count=2, threshold_percent=0, only_top=False):
    res = occurrences(arr, ascending=ascending)
    total = sum([x[0] for x in res])
    if only_top < 1:
        only_top = len(res)
    buffer = len(str(res[0][0])) + 4
    for i, x in enumerate(res):
        percent = round(100 * x[0] / total, 2)
        if x[0] < threshold_count or percent < threshold_percent or i >= only_top:
            print(f"and {len(res)-i} more...")
            break
        print(f"{x[0]}x".ljust(buffer), end="")
        if percent < 10:
            print(end=" ")
        print("(%.2f" % percent + "%)", sep="", end="\t")
        print(x[1])


def analysis_report(result, numeric=False):
    if type(result) is dict:
        for x in result:
            print("Results of", x)
            if numeric:
                statistic_report(result[x])
            else:
                occurrence_report(result[x])
    elif type(result) is list:
        if numeric:
            statistic_report(result, DEFAULT_DUMP_STATISTICS)
        else:
            occurrence_report(result)
    else:
        print(result)
