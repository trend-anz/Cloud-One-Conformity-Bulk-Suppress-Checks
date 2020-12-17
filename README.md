# Cloud-One-Conformity-Bulk-Suppress-Checks
## Script Overview

This script allows you to suppress findings in bulk based on results returned from the * [Cloud One Conformity Checks API](https://github.com/cloudconformity/documentation-api/blob/master/Checks.md) endpoint.

***IMPORTANT:***
This script will suppress ALL findings returned based on the filters you provide, please ensure you filter your results correctly with filter variables.

### List of variables available within the script:
Conformity Account Info:
- CC_REGION (defaults to us-west-2)
- CC_APIKEY (required)
- CC_ACCOUNTIDS (required)

Suppression Message:
- CC_SUPPRESSION_NOTE (defaults to "Bulk Suppression Script")

Checks API Filters:
CC_FILTER_CATEGORIES
CC_FILTER_COMPLIANCES
CC_FILTER_NEWERTHANDAYS
CC_FILTER_OLDERTHANDAYS
CC_FILTER_REGIONS
CC_FILTER_RISKLEVELS
CC_FILTER_RULEIDS (required to prevent suppression of everything when not supplied)
CC_FILTER_SERVICES
CC_FILTER_STATUSES (defaults to "FAILURE")
CC_FILTER_SUPPRESSED (defaults to "false" to skip already suppressed findings)
CC_FILTER_SUPPRESSEDFILTERMODE (defaults to "v2")
CC_FILTER_TAGS 

## Usage

1. Install the required pip dependencies:
```
pip3 install -r requirements.txt
```
2. Set your environment variables for your desired filters:
Example to suppress all failed checks older than 7 days for the CFM-002 rule.
```
export CC_APIKEY=asdfasdfksjadfkljaDUMMYAPIKEY
export CC_ACCOUNTIDS=i7adfakeID
export CC_RULEIDS=Config-002
export CC_FILTER_OLDERTHANDAYS=7
```

Run the script:
```
python3 suppresschecks.py
```

Example Response:
```
Received API response code of 200 for check ID: ccc:i7adfakeID:CFM-002:CloudFormation:us-east-1:CloudConformity
Received API response code of 200 for check ID: ccc:i7adfakeID:CFM-002:CloudFormation:us-east-1:CloudConformityMonitoring
Received API response code of 200 for check ID: ccc:i7adfakeID:CFM-002:CloudFormation:us-west-1:CloudConformityMonitoring
```


## Authors

* **Tom Ryan** - *Initial work* - [TomRyan-321](https://github.com/TomRyan-321)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## For more information about Trend Micro Cloud One & Cloud One Conformity visit:

* [CloudConformity Official Website](https://www.cloudconformity.com)
* [CloudConformity API Documentation](https://github.com/cloudconformity/documentation-api)
* [Trend Micro Cloud One](https://www.trendmicro.com/en_au/business/products/hybrid-cloud.html)
