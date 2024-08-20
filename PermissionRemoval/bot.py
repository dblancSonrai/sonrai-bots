import logging
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient

def run(ctx):
    #create client whose credentials we will use
    client = ctx.get_client()
    logging.info('Client Created')
    #logging.info(SonraiClient.credential)
    
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
    #client = ctx.get_client().get(AuthorizationManagementClient, subscription_id=assignmentID[4])
    #logging.info(client.credentials)

    auth_client = AuthorizationManagementClient(credential = DefaultAzureCredential(),subscription_id = assignmentID[4])
    
    #auth_client = AuthorizationManagementClient(client.credential, assignmentID[4])
    
    
    logging.info('Auth Client Created')
    
    try:
        #remove the role assignment
        response = auth_client.role_assignments.delete(scope = assignScope,role_assignment_name = assignmentID)
        print(response)
        logging.info('Permission Removal Bot Done')

    except Exception as error:
        logging.info('Permission Removal Bot Failed: ')
        logging.info(error)
        #gql_loader.add_ticket_comment(ctx, "this is a comment")
