
from Stats import statistic_dump, DEFAULT_DUMP_STATISTICS


def unpack(box):
    arr = []
    for x in box:
        for y in x:
            arr.append(y)
    return arr


def occurrences(arr, ascending=False):
    counts = {}
    for x in arr:
        if x not in counts:
            counts[x] = 1
        else:
            counts[x] += 1
    result = [(counts[x], x) for x in counts]
    result.sort(reverse=not ascending)
    return result


def occurrence_report(arr, ascending=False, threshold_count=0, threshold_percent=0, only_top=False):
    res = occurrences(arr, ascending=ascending)
    total = sum([x[0] for x in res])
    if only_top < 1:
        only_top = len(res)
    for i, x in enumerate(res):
        percent = round(100 * x[0] / total, 2)
        if x[0] < threshold_count or percent < threshold_percent or i >= only_top:
            print("...")
            break
        print(x[0], "x\t", sep="", end="")
        if x[0] < 100:
            print("\t", end="")
        if percent < 10:
            print(end=" ")
        print("(", percent, "%)", sep="", end="\t")
        print(x[1])


def analysis_report(result, numeric=False):
    if type(result) is dict:
        for x in result:
            print("Results of", x)
            if numeric:
                statistic_dump(result[x])
            else:
                occurrence_report(result[x])
    elif type(result) is list:
        if numeric:
            statistic_dump(result, DEFAULT_DUMP_STATISTICS)
        else:
            occurrence_report(result)
    else:
        print(result)
