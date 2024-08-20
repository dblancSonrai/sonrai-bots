import logging
import os
#from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient

def run(ctx):
    #create client whose credentials we will use
    #SonraiClient = ctx.get_client()
    logging.info('Client Created')
    logging.info(SonraiClient.credential)
    
    #get ticket date
    ticket = ctx.config
    data = (ticket['data']['ticket'])
    logging.info('ticket data loaded')

    #pull out scope and assignment ID
    assignmentID = data['resourceSRN']
    assignmentID = assignmentID.split('/')
    assignScope = assignmentID[3]+"/"+assignmentID[4]
    assignmentID = assignmentID[8]

    #authClient = SonraiClient.get(AuthorizationManagementClient, subscription_id=assignmentID[4])
    
    #Authenticate
    client = ctx.get_client().get(AuthorizationManagementClient, subscription_id=assignmentID[4])
    
    #client = AuthorizationManagementClient(SonraiClient.credential, assignmentID[4])
    
    logging.info('Authentication Done')
    try:
        #remove the role assignment
        response = client.role_assignments.delete(scope = assignScope,role_assignment_name = assignmentID)
        print(response)
        logging.info('Permission Removal Bot Done')

    except Exception as error:
        logging.info('Permission Removal Bot Failed: ')
        logging.info(error)
        #gql_loader.add_ticket_comment(ctx, "this is a comment")
