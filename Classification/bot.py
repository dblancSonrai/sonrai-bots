import logging

def run(ctx):
    # SRN of the resource in the ticket
    object_srn = ctx.resource_srn

    # Create GraphQL client
    graphql_client = ctx.graphql_client()

    # options used in creating the data classification jobs
    outputMode = "FINGERPRINT" # FINGERPRINT or OBJECT
    includeSamples = "false" # true or false
    scanMode = "FULL_SCAN" # FULL_SCAN, PARTIAL_SCAN or QUICK_SCAN
    classifiers = " ADDRESS, BANKACCOUNTNUMBER, CREDITCARD, DOB, EMAIL, FULLNAME, PHONENUMBER, SSN, ZIPCODE "
    customClassifier = ' " srn:nafinc::SonraiCustomClassifier/98bd3526-e7c2-455c-9e59-eb4cc6113d1c, srn:nafinc::SonraiCustomClassifier/1506d679-c5e3-4a26-820d-01be122df6b2, srn:nafinc::SonraiCustomClassifier/fd6c9a47-f28c-43b8-b67e-4f5f81fcbe38, srn:nafinc::SonraiCustomClassifier/253d55ab-ff98-4bba-b685-f9029578d1d9, srn:nafinc::SonraiCustomClassifier/c8d599d3-8683-4d9a-ac24-ab0d6728c470, srn:nafinc::SonraiCustomClassifier/3c6a8caf-1f11-4dd2-8860-5b007127e4d2, srn:nafinc::SonraiCustomClassifier/28b654db-bb5c-4b50-a43d-7e7f5ff7800a " '
    encryptionEnabled = "false" # true or false
    # comment out next line if encryptionEnabled is false
    # public key needs to have carriage returns removed and replaced with \\n
    #publicKey ="-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5//KZA2xGUfTV8ohNOAj\\ny6ovDomGqL8Hq5g91vaLs9HfVIR8lrviP9S30y9KWPVWZ/3LWxLzN2uz8OSfK0JS\\nYiCCGdsYa3WppsSlSgMiI9uhDXJpgyBKNoKQcyZR67Bpbtj7/lR4kT6S3kNbIDNf\\nzO/dG4G9MGmdEE0A2wUgCKLHIMH7IoL4dfaSYW4eNcW+uxwX/pnUHWtLAlUFUel1\\np/LDUhjzEuQfw7MfLGHos6h54R+MaY+6OBd+NL6LKswlDwatMK+iu7BLTz3NP6GP\\nZ53n7yKrEs8vHmmTPRTqdEq+EtTtuKmF36j9NJm/t+krhhCqcAuGtyJT2FaBP5kE\\nsQIDAQAB\\n-----END PUBLIC KEY-----"

    # Mutation for schedule Data Classification
    mutation = ( 'mutation dc {' +
                 'CreateDataClassificationConfig (input: {'+
                 ' enabled:true' +
                 ' targetSrn: "' + object_srn + '" ' +
                 ' jobInfo: {' +
                    ' outputMode: ' + outputMode +
                    ' includeSamples: ' + includeSamples +
                    ' scanMode: ' + scanMode +
                    ' classifiers: [ ' + classifiers + ' ]' +
                    ' encryptionEnabled: ' + encryptionEnabled +
                    ' customClassifierSrns: [ ' + customClassifier + ' ]' +
                    ' hashingEnabled:false' +
                    ' hashingType:null' +
                    ' saltKeyvaultName:null' +
                    ' saltKeyvaultPath:null'
                    
              )

    if 'publicKey' in locals():
        mutation += (
                    ' publicKey: "' + publicKey + '"'
        )

    mutation += ( ' }' +
               '}){srn}' +
               '}'
              )

    #variables can be blank because they are put directly into the mutation
    variables = {}

    # Schedule Data Classification job on object_srn
    logging.info('Schedule Data Classification on: {}'.format(object_srn))
    graphql_client.query(mutation, variables)
