import lxml.html
import StringIO
import json


def extract_content(outer_html):
    companies_divs = outer_html.findall('.//div[@data-id]')

    with open("target_fields_xpaths.json") as in_:
        xpaths = json.load(in_)

    all_data = []
    for cdiv in companies_divs:
        cdata = dict()
        cdata.update({"cname": cdiv.find(xpaths["company_name"]).text_content().strip()})
        cdata.update({"lactive": cdiv.find(xpaths["last_active"]).text_content().strip()})
        cdata.update({"esize": cdiv.find(xpaths["employee_size"]).text_content().strip()})
        try:
            cdata.update({"curl": cdiv.findall(xpaths["urls"])[-1].text_content().strip()})
        except IndexError:
            cdata.update({"curl": 'can not find'})
        jobs = dict()
        for j_id, jdiv in enumerate(cdiv.findall(xpaths["jobs"])):
            jobs.update({j_id: jdiv.text_content()})
        cdata.update({"jobs": jobs})
        founders = dict()
        for f_id, fdiv in enumerate(cdiv.findall(xpaths["founders"])):
            founders.update({f_id: fdiv.text_content().strip()})
        cdata.update({"founders": founders})
        all_data.append(cdata)

    return all_data


if __name__ == "__main__":

    # Parse HTML
    with open("sw-blr-startups.html") as in_:
        outer_html = lxml.html.parse(StringIO.StringIO(in_.read()))

    # extract_content
    all_data = extract_content(outer_html=outer_html)

    with open("all_startups_info.json", "wb+") as out:
        json.dump(fp=out, obj={"all_strartups_info": all_data})
