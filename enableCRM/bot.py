import logging

def run(ctx):
    # SRN of the resource in the ticket
    object_srn = ctx.resource_srn

    # Create GraphQL client
    graphql_client = ctx.graphql_client()
    
    #all different action classifications CRM will look for on changes to permissions
    action_class = [dataread, protectionread, create, datacreate, tag]
  
    logging.info('Setting CRM for: {}'.format(object_srn))
    
    for ac in action_class:
      mutationAccess = ( 'mutation CRM {' +
                  'setChangeDetectionProperties('+
                  ' ResourceSrn: "' + object_srn + '" ' +
                  ' keyType: PATH' +
                  ' keyName: "accessedBy" '+
                  ' actionClassification: "' + ac + '" ' +
                  ' alertLevel: 5'
                  )
      results = graphql_client.query(mutationAccess)
    #check to see if everything is good before running
    
    mutation = ( 'mutation CRM_GEO {' +
                'setChangeDetectionProperties('+
                ' ResourceSrn: "' + object_srn + '" ' +
                ' keyType: PATH' +
                ' keyName: "accessedFrom" '+
                ' alertLevel: 5'
                )

    graphql_client.query(mutation)
