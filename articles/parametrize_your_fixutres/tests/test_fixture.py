import pytest


@pytest.mark.dynamodb_table(name="test_table", data="fixtures/pets.json")
def test_parametrized_fixture(dynamodb_table) -> None:
    # given
    pk_value = "Pet"

    # when
    response = dynamodb_table.query(
        KeyConditionExpression="pk = :pk",
        ExpressionAttributeValues={":pk": pk_value}
    )

    # then
    assert len(response["Items"]) == 3
