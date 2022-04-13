import boto3


def connect_db():
    dynamodb = boto3.resource('dynamodb', aws_access_key_id='AKIA32TG2YFVZ465TSEN',
                              aws_secret_access_key='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', region_name='us-east-1')
    return dynamodb


def get_or_create_table_post(dynamodb):
    for table in dynamodb.tables.all():
        if table.name == 'Statistics':
            print('Table Post already exists')
            return table

    table = dynamodb.create_table(
        TableName='Statistics',
        KeySchema=[
            {
                'AttributeName': 'page_id',
                'KeyType': 'HASH'
            },
            {
                "AttributeName": "user_id",
                "KeyType": "RANGE"
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'page_id',
                'AttributeType': 'S'
            },
            {
                "AttributeName": "user_id",
                "AttributeType": "N"
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print('Table Post has been created')
    return table
