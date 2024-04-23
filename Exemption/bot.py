import logging
import json
from sonrai import gql_loader

def run(ctx):
    # Load searches:
    gql = gql_loader.queries()

    # Create GraphQL client
    graphql_client = ctx.graphql_client()

    # Get the ticket data from the context
    ticket = ctx.config.get('data').get('ticket')
    logging.info('Got ticket data')

    get_resources = None
    query_resourcesToExempt = gql['savedQuery.gql']
    mutation_setImportance = gql['setImportance.gql']
    
    logging.info('print ticket info')
    
    logging.info(ticket.get('cfFields'))
    
    logging.info('Attempting to get custom field')
    
    for customField in ticket.get('cfFields'):
        logging.info('Attempting to grab search name')
        search_name = customField['value']
        logging.info('Formatting query name')
        search_name = ('{"name": "' + search_name + '" }')
        logging.info('Attempting to run query')
        get_resources = graphql_client.query(query_resourcesToExempt,search_name)
        logging.info('Query successfully worked')

    for resource in get_resources['ExecuteSavedQuery']['Query']['Resources']['items']:
        srn = resource['srn']
        srn = ('{"srn": "' + srn + '" }')
        print(srn)
        set_importance = graphql_client.query(mutation_setImportance,srn)
        endResource = set_importance['setImportance']['srn']
        logging.info('Exempted Resource: '+endResource)

    gql_loader.snooze_ticket(ctx, hours=24)
