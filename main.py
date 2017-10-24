import json
import numpy as np


def sort_by_company_size(company_units):

    all_sizes = [unit["esize"] for unit in company_units]

    # Quantify strings
    all_sizes_quantified = []
    for size_txt in all_sizes:

        numbers_in_txt = []
        for token in size_txt.strip().split():

            if token.isdigit() is True:
                numbers_in_txt.append(int(token))

        all_sizes_quantified.append(min(numbers_in_txt))

    # Sort by size
    packed = zip(*[company_units, all_sizes_quantified])
    packed_sorted = sorted(packed, key=lambda x: x[1])
    company_units_sorted = zip(*packed_sorted)[0]

    return company_units_sorted


def sort_by_last_active(company_units):

    all_last_actives = [unit["lactive"] for unit in company_units]

    # Quantify strings
    all_last_actives_quantifed = []
    for lactive_txt in all_last_actives:

        numbers_in_txt = []
        for token in lactive_txt.strip().split():

            if token.isdigit() is True:
                numbers_in_txt.append(int(token))
            elif "minute" in token:
                numbers_in_txt.append(1)
            elif "hour" in token:
                numbers_in_txt.append(10)
            elif "day" in token:
                numbers_in_txt.append(100)
            elif "week" in token:
                numbers_in_txt.append(1000)
            elif "month" in token:
                numbers_in_txt.append(10000)
            elif "year" in token:
                numbers_in_txt.append(100000)

        all_last_actives_quantifed.append(reduce(lambda x, y: x * y,
                                                 numbers_in_txt))

    # Sort by size
    packed = zip(*[company_units, all_last_actives_quantifed])
    packed_sorted = sorted(packed, key=lambda x: x[1])
    company_units_sorted = zip(*packed_sorted)[0]

    return company_units_sorted


if __name__ == "__main__":

    with open("all_startups_info.json") as in_:
        all_company_units = json.load(in_)["all_startups_info"]
