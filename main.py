import sys
import json
import numpy as np


def get_company_size(company_unit):

    size_txt = company_unit["esize"]

    numbers_in_txt = []
    for token in size_txt.strip().split('-'):

        if token.isdigit() is True:
            numbers_in_txt.append(int(token))
    try:
        return min(numbers_in_txt)
    except:
        return 10**50


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


def sort_logic(company_units):
    """
    Sort companies by esize first and then sort them by their last_active
    """

    final_queue = []
    all_sizes = np.array([get_company_size(unit) for unit in company_units])
    unique_sizes = set(all_sizes)
    for size in sorted(unique_sizes):
        cluster = np.array(company_units)[all_sizes == size]
        cluster_la = sort_by_last_active(company_units=cluster.tolist())
        final_queue += cluster_la

    return final_queue


if __name__ == "__main__":

    with open("all_startups_info.json") as in_:
        all_company_units = json.load(in_)["all_startups_info"]

    with open("state.txt") as in_:
        curr_company = int(in_.readline().strip())

    sorted_companies = sort_logic(company_units=all_company_units)

    for cid, cu in enumerate(sorted_companies[curr_company:]):

        founders_string = ""
        for founder in cu["founders"].values():
            founders_string += "%s\n" % founder.replace("\n", "")

        job_desc_string = ""
        for job in cu["jobs"].values():
            job_desc_string += "%s\n" % job.replace("\n", "")

        company_desc = """
            Company name: %s
            URL : %s
            Last active: %s
            Employee size: %s
            Founders: %s
            Jobs & desc: %s

        """ % (cu["cname"], cu["curl"], cu["lactive"],
               cu["esize"], founders_string, job_desc_string)

        print(company_desc)

        with open("state.txt", "w+") as out_:
            out_.write(str(curr_company + cid))

        read = raw_input("Shall I display next company? (yes/no/exit)")
        while read.lower() != "yes":
            if read.lower() == "exit":
                sys.exit(0)
            read = raw_input("Shall I display next company? (yes/no/exit)")
