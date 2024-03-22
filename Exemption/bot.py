import logging
from sonrai import gql_loader

def run(ctx):
    # Load searches:
    gql = gql_loader.queries()

    # Create GraphQL client
    graphql_client = ctx.graphql_client()

    search_name = ""

    for customField in ticket.get('customFields'):
        search_name = customField['name']

    query_resourcesToExempt = gql['savedQuery.gql']
    get_resources = graphql_client.query(query_resourcesToExempt,search_name)

    for resource in get_resources['ExecuteSavedQuery']['Query']['Resources']['items']:
        srn = resource['srn']
        mutation_setImportance = gql['setImportance.gql']
        set_importance = graphql_client.query(mutation_setImportance,srn)
        endResource = set_importance['setImportance']['srn']
        logging.info('Exempted Resource: '+endResource)

gql_loader.snooze_ticket(ctx, hours=24)
