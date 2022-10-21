import logging

def run(ctx):
    # SRN of the resource in the ticket
    object_srn = ctx.resource_srn

    # Create GraphQL client
    graphql_client = ctx.graphql_client()
    
    #all different action classifications CRM will look for on changes to permissions
    action_class = ["DataRead", "ProtectionRead", "Create", "DataCreate", "Tag"]
  
    logging.info('Setting CRM for: {}'.format(object_srn))
    
    for ac in action_class:
        mutationAccess = ( 'mutation CRM {' +
                  'setChangeDetectionProperties('+
                  ' resourceSrn: "' + object_srn + '" ' +
                  ' keyType: PATH' +
                  ' keyName: "accessedBy" '+
                  ' actionClassification:' + ac +
                  ' alertLevel: 5){resourceSrn}}'
                  )
        
        logging.info('Mutation: {}'.format(mutationAccess))
        graphql_client.query(mutationAccess)
    
    mutation = ( 'mutation CRM_GEO {' +
                'setChangeDetectionProperties('+
                ' resourceSrn: "' + object_srn + '" ' +
                ' keyType: PATH' +
                ' keyName: "accessedFrom" '+
                ' alertLevel: 5){resourceSrn}}'
                )

    graphql_client.query(mutation)
    
    mutationTag = ( 'mutation addTagsWithNoDuplicates {' +
                    'AddTag(' +
                        'value: {' + 
                            'key: "CRM" '+  
                            'value: "Enabled" '+
                            'tagsEntity: { add: "' + object_srn + '" } }) {' +
                    'srn' +
                    'key' +
                    'value' +
                    '__typename}}'
                  )    
    logging.info('Mutation: {}'.format(mutationTag))               
    graphql_client.query(mutationTag)
