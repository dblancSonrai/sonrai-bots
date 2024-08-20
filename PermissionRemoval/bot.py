import logging
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient

#os.environ['AZURE_CLIENT_ID'] = "859e2fc7-9cbe-4d6d-bb6f-7a9e0b3ac68c"
#os.environ['AZURE_TENANT_ID'] = "99396606-ff18-470f-ad3d-e0f25f39a9aa"
#os.environ['AZURE_CLIENT_SECRET'] = "Pb68Q~Ed.jNaPil6FurBXCDdnPmkYm4S6h9Naccm"


def run(ctx):
    #create client whose credentials we will use
    SonraiClient = ctx.get_client()
    logging.info('Client Created')
    logging.info(SonraiClient.credential)
    logging.info(SonraiClient)

    #get ticket date
    ticket = ctx.config
    data = (ticket['data']['ticket'])
    logging.info('ticket data loaded')

    #pull out scope and assignment ID
    assignmentID = data['resourceSRN']
    assignmentID = assignmentID.split('/')
    assignScope = assignmentID[3]+"/"+assignmentID[4]
    assignmentID = assignmentID[8]

    #Authenticate
    client = AuthorizationManagementClient(
        credential = SonraiClient.credential,
        #credential = DefaultAzureCredential(),
        subscription_id = assignmentID[4],
    )
    logging.info('Authentication Done')
    try:
        #remove the role assignment
        response = client.role_assignments.delete(
            scope = assignScope,
            role_assignment_name = assignmentID,
        )
        print(response)
        logging.info('Permission Removal Bot Done')

    except Exception as error:
        logging.info('Permission Removal Bot Failed: '+error)
        gql_loader.add_ticket_comment(ctx, "this is a comment")
