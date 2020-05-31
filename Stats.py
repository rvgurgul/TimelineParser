

def binned_average(arr, bins=3, rounding=2):
    if len(arr) < bins:
        return [None]*bins
    delta = len(arr)//bins
    ordered = sorted(arr)
    return [round(average(ordered[delta * i:delta * (i + 1)]), rounding) for i in range(bins)]


def median(arr):
    return sorted(arr)[len(arr)//2] if len(arr) > 0 else None


def average(arr, sigfigs=3):
    return None if len(arr) == 0 else round(sum(arr)/len(arr), sigfigs)


DEFAULT_DUMP_STATISTICS = {
    "Size:\t\t\t": len,
    "Average:\t\t": average,
    "Minimum:\t\t": lambda arr: min(arr) if len(arr) > 0 else None,
    "Maximum:\t\t": lambda arr: max(arr) if len(arr) > 0 else None,
    "Median:\t\t\t": median,
    "Low/Med/High:\t": binned_average
}


def statistic_report(arr, funcs=None, rounding=2):
    if funcs is None:
        funcs = DEFAULT_DUMP_STATISTICS
    if type(funcs) is dict:
        for name in funcs:
            value = funcs[name](arr)
            if type(value) is float:
                value = round(value, rounding)
            print(name, value)
    elif type(funcs) is list or type(funcs) is tuple:
        for func in funcs:
            value = func(arr)
            if type(value) is float:
                value = round(value, rounding)
            print(value)


def average_report(arr):
    print(f"Average: {average(arr, )}")


def rate_report(arr):
    avg = 100 * average(arr)
    print("Rate: %02f" % avg, "%", sep="")
