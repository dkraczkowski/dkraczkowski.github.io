import json
from os import path

import boto3
import moto
import pytest


@pytest.fixture
def test_dir():
    return path.join(path.dirname(__file__))


@pytest.fixture
def dynamodb_table(test_dir, request):
    # Default table schema
    table_schema = {
        "table_name": "default",
        "pk": "pk",
        "sk": "sk",
    }
    if request.node.get_closest_marker("dynamodb_table"):
        table_schema = {**table_schema, **request.node.get_closest_marker("dynamodb_table").kwargs}

    # Create table and load data
    with moto.mock_dynamodb():
        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
        table = dynamodb.create_table(
            TableName=table_schema["name"],
            KeySchema=[
                {"AttributeName": table_schema["pk"], "KeyType": "HASH"},
                {"AttributeName": table_schema["sk"], "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": table_schema["pk"], "AttributeType": "S"},
                {"AttributeName": table_schema["sk"], "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        if "data" in table_schema:
            data = json.load(open(path.join(test_dir, table_schema["data"]), "r"))

            with table.batch_writer() as process:
                for index, record in enumerate(data):
                    process.put_item(Item=record)
        yield table
        client = boto3.client("dynamodb", region_name="eu-west-1")
        client.delete_table(TableName=table_schema["name"])
