import logging
import json
from sonrai import gql_loader

def run(ctx):
    # Load searches:
    gql = gql_loader.queries()

    # Create GraphQL client
    graphql_client = ctx.graphql_client()

    # Get the ticket data from the context
    #ticket = ctx.config.get('data').get('ticket')
    ticket = ctx.config
    ticketSrn = ticket['data']['ticket']['srn']
    
    get_resources = None
    query_resourcesToExempt = gql['savedQuery.gql']
    mutation_setImportance = gql['setImportance.gql']
    query_ticket = gql['ticket.gql']
    logging.info(ticketSrn)
    ticketSrn = ('{"srn": "' + ticketSrn + '" }')
    
    customField = graphql_client.query(query_ticket,ticketSrn)
    
    logging.info(customField)
    logging.info('Attempting to grab search name')
    search_name = customField['ListFindings']['items'][0]['cfFields'][0]['value']
    logging.info('Formatting query name')
    search_name = ('{"name": "' + search_name + '" }')
    logging.info('Attempting to run query')
    get_resources = graphql_client.query(query_resourcesToExempt,search_name)
    logging.info('Query successfully worked')

    for resource in get_resources['ExecuteSavedQuery']['Query']['Roles']['items']: #change rolls to resources
        srn = resource['srn']
        srn = ('{"srn": "' + srn + '" }')
        set_importance = graphql_client.query(mutation_setImportance,srn)
        endResource = set_importance['setImportance']['srn']
        logging.info('Exempted Resource: '+endResource)

    gql_loader.snooze_ticket(ctx, hours=24)
