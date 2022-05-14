import boto3

ssm = boto3.client('ssm')

# Creates a Support Ticket in ITSM system about the incident

def lambda_handler(event, context):

    # TODO Implement ITSM Connectivity to log an incident in ITSM system
    # Python Sample to connect to ServiceNow
    #Need to install requests package for python

    # #easy_install requests
    # import requests
    #
    # # Set the request parameters
    # url = 'https://instance.service-now.com/api/now/table/incident'
    #
    # # Eg. User name="admin", Password="admin" for this code sample.
    # user = 'admin'
    # pwd = 'admin'
    #
    # # Set proper headers
    # headers = {"Content-Type":"application/xml","Accept":"application/xml"}
    #
    # # Do the HTTP request
    # response = requests.post(url, auth=(user, pwd), headers=headers ,data="<request><entry><short_description>Unable to connect to office wifi</short_description><assignment_group>287ebd7da9fe198100f92cc8d1d2154e</assignment_group><urgency>2</urgency><impact>2</impact></entry></request>")
    #
    # # Check for HTTP codes other than 200
    # if response.status_code != 200:
    #     print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    #     exit()
    #
    # # Decode the JSON response into a dictionary and use the data
    # data = response.json()
    # print(data)

    return event
