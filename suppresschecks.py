import os
import json
import requests

# Conformity Region, API Key & Target Account(s) variables (when inputting multiple accounts comma delimit)
CC_REGION = os.environ.get("CC_REGION", "us-west-2")
CC_APIKEY = os.environ["CC_APIKEY"]
CC_ACCOUNTIDS = os.environ["CC_ACCOUNTIDS"]

# Pagination variables
CC_PAGESIZE = int(os.environ.get("CC_PAGESIZE", 1000))
CC_PAGENUMBER = int(os.environ.get("CC_PAGENUMBER", 0))

# Suppression note to add
CC_SUPPRESSION_NOTE = os.environ.get("CC_SUPPRESSION_NOTE", "Bulk Suppression Script")

# Checks API Filters
CC_FILTER_CATEGORIES = os.environ.get("CC_FILTER_CATEGORIES", "")
CC_FILTER_COMPLIANCES = os.environ.get("CC_FILTER_COMPLIANCES", "")
CC_FILTER_CREATEDLESSTHAN = os.environ.get("CC_FILTER_CREATEDLESSTHAN", "")
CC_FILTER_CREATEDMORETHAN = os.environ.get("CC_FILTER_CREATEDMORETHAN", "")
CC_FILTER_REGIONS = os.environ.get("CC_FILTER_REGIONS", "")
CC_FILTER_RISKLEVELS = os.environ.get("CC_FILTER_RISKLEVELS", "")
CC_FILTER_RULEIDS = os.environ["CC_FILTER_RULEIDS"]
CC_FILTER_SERVICES = os.environ.get("CC_FILTER_SERVICES", "")
CC_FILTER_STATUSES = os.environ.get("CC_FILTER_STATUSES", "FAILURE")
CC_FILTER_SUPPRESSED = os.environ.get("CC_FILTER_SUPPRESSED", "false")
CC_FILTER_SUPPRESSEDFILTERMODE = os.environ.get("CC_FILTER_SUPPRESSEDFILTERMODE", "v2")
CC_FILTER_TAGS = os.environ.get("CC_FILTER_TAGS", "")

url = "https://" + CC_REGION + "-api.cloudconformity.com/v1/checks"
params = {
    "accountIds": CC_ACCOUNTIDS,
    "filter[categories]": CC_FILTER_CATEGORIES,
    "filter[compliances]": CC_FILTER_COMPLIANCES,
    "filter[createdLessThanDays]": CC_FILTER_CREATEDLESSTHAN,
    "filter[createdMoreThanDays]": CC_FILTER_CREATEDMORETHAN,
    "filter[regions]": CC_FILTER_REGIONS,
    "filter[riskLevels]": CC_FILTER_RISKLEVELS,
    "filter[ruleIds]": CC_FILTER_RULEIDS,
    "filter[services]": CC_FILTER_SERVICES,
    "filter[tags]": CC_FILTER_TAGS,
    "filter[statuses]": CC_FILTER_STATUSES,
    "filter[suppressed]": CC_FILTER_SUPPRESSED,
    "filter[suppressedFilterMode]": CC_FILTER_SUPPRESSEDFILTERMODE,
    "page[size]": CC_PAGESIZE,
    "page[number]": CC_PAGENUMBER,
}
# def get_account_checks():
payload = {}
headers = {
    "Content-Type": "application/vnd.api+json",
    "Authorization": "ApiKey " + CC_APIKEY,
}

session = requests.session()


def get_account_checks():
    combined = []
    counter = 0
    max_results = 1
    while counter <= max_results:
        page = session.get(url, params=params, headers=headers, data=payload).json()
        max_results = page["meta"]["total"]
        counter += CC_PAGESIZE
        params["page[number]"] += 1
        data = page["data"]
        combined += data
    return {"data": combined, "meta": page["meta"]}


pages_combined = get_account_checks()
checkstosuppress = pages_combined["data"]
for check in checkstosuppress:
    id = check["id"]
    checkurl = url + "/" + id
    suppressbody = {
        "data": {
            "type": "checks",
            "attributes": {"suppressed": True, "suppressed-until": None},
        },
        "meta": {"note": CC_SUPPRESSION_NOTE},
    }
    jsonbody = json.dumps(suppressbody)
    suppress = session.patch(checkurl, headers=headers, data=jsonbody)
    print("Received API response code of " + str(suppress.status_code) + " for suppress of check ID: " + id)
