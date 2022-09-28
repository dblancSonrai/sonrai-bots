import logging

def run(ctx):
    # SRN of the resource in the ticket
    object_srn = ctx.resource_srn

    # Create GraphQL client
    graphql_client = ctx.graphql_client()
    
    #all different action classifications CRM will look for on changes to permissions
    action_class = ["DataCreate, DataDelete, DataUpdate, DataRead, ProtectionCreate, ProtectionDelete, ProtectionUpdate, ProtectionRead, Configure, Delete, Update"]
    
    #different CRM types. the who or what can access and who or what did access options
    key_name = ["actionableBy, accessedBy"]
    
    logging.info('Setting CRM for: {}'.format(object_srn))
    
    for ac in action_class:
      mutationAction = ( 'mutation CRM {' +
                  'setChangeDetectionProperties('+
                  ' ResourceSrn: "' + object_srn + '" ' +
                  ' keyType: PATH' +
                  ' keyName: "actionableBy" +
                  ' actionClassification: "' + ac + '" ' +
                  ' alertLevel: 5
                  )
      mutationAccess = ( 'mutation CRM {' +
                  'setChangeDetectionProperties('+
                  ' ResourceSrn: "' + object_srn + '" ' +
                  ' keyType: PATH' +
                  ' keyName: "accessedBy" +
                  ' actionClassification: "' + ac + '" ' +
                  ' alertLevel: 5
                  )
      graphql_client.query(mutationAction)
      graphql_client.query(mutationAccess)
    
    mutation = ( 'mutation CRM_GEO {' +
                'setChangeDetectionProperties('+
                ' ResourceSrn: "' + object_srn + '" ' +
                ' keyType: PATH' +
                ' keyName: "accessedFrom" +
                ' alertLevel: 5
                )

    graphql_client.query(mutation)

    
    
