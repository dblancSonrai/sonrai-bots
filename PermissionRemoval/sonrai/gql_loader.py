from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join

queriesDirectory = 'graphql'
query_files = [f for f in listdir(queriesDirectory) if isfile(join(queriesDirectory, f))]


# GQL queries loads files
# can also pass name=value pairs to use as $string substitution in file loaded queries
def queries(**kwargs):
    # Create a dictionary to return all queries
    gql = dict()

    # load all query files from the bots graphql folder
    for file in query_files:
        if file.endswith('.gql'):
            file_content = open("{0}/{1}".format(queriesDirectory, file))
            gql_data = file_content.read()

            # Iterating over the keys of the Python kwargs dictionary
            for key, value in kwargs.items():
                gql_data = gql_data.replace('$' + key, value)

            gql[file] = gql_data

    return gql


# loads saved searches by name (bot:[name])
def saved_search(ctx, name):
    if name:
        # search for any saved searched that start with "BOT:" and load in the data as another query
        graphql_client = ctx.graphql_client()
        query = '{ExecuteSavedQuery {Query (name:"' + str(name) + '" )}}'
        query_variables = {}
        results = graphql_client.query(query, query_variables)

        return results['ExecuteSavedQuery']['Query']


# Snoozes Tickets
def snooze_ticket(ctx, hours=None):
    if hours:
        _snooze_interval = hours

        # Get the ticket data from the context
        ticket = ctx.config.get('data').get('ticket')

        if ticket and ticket.get('srn'):
            # un-snooze and re-snooze the ticket for a shorter time period
            mutation_reopen_ticket = ('''
              mutation openTicket($srn:String){
                ReopenTickets(input: {srns: [$srn]}) {
                  successCount
                  failureCount
                }
              }
            ''')

            mutation_snooze_ticket = ('''
                mutation snoozeTicket($srn: String, $snoozedUntil: DateTime) {
                    SnoozeTickets(snoozedUntil: $snoozedUntil, input: {srns: [$srn]}) {
                      successCount
                      failureCount
                      __typename
                    }
                  }
            ''')

            # Create GraphQL client
            graphql_client = ctx.graphql_client()

            # calculate the snoozeUntil time
            snooze_until = datetime.now() + timedelta(hours=_snooze_interval)
            variables = ('{"srn": "' + ticket['srn'] + '", "snoozedUntil": "' + str(snooze_until).replace(" ", "T") + '" }')

            # re-open ticket so it can be snoozed again
            graphql_client.query(mutation_reopen_ticket, variables)

            # snooze ticket
            graphql_client.query(mutation_snooze_ticket, variables)


def add_ticket_comment(ctx, body):
    if body:
        mutation_add_comment = ('''
          mutation addTicketComment($ticketSrn: String!, $body: String!, $createdBy: String!) {
            CreateTicketComment(
               input: {body: $body, ticketSrn: $ticketSrn, createdBy: $createdBy}
             ) {
               resourceId
               srn
               createdBy
               createdDate
               body
             }
         }
        ''')
        # get ticket SRN
        ticket_srn = ctx.config.get('data').get('ticket').get('srn')
        # get current orgName
        org_name = ctx.config.get('data').get('ticket').get('orgName')
        # build the bot_user SRN from the org_name
        user_srn = 'srn:' + org_name + '::SonraiUser/bot_user'
        
        variables = ('{"ticketSrn": "' + ticket_srn + '", "body": "' + body + '", "createdBy": "' + user_srn + '" }')
        graphql_client = ctx.graphql_client()
        graphql_client.query(mutation_add_comment, variables)
