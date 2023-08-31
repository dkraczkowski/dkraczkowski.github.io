# Stop wasting time redefining fixtures, and embrace the power of reusing them with Pytest!

In software testing, fixtures play an essential role in setting up necessary preconditions for our tests. They help ensure the environment is consistent, and we have the tools we need to execute the tests. 

Pytest offers a flexible way that enables us to take our fixtures a step further and make them more dynamic using the mark annotation. 
This is particularly useful in scenarios like AWS DynamoDB testing, where different scenarios might require different data setups.

## Scenario: DynamoDB Table Setup

Imagine you're testing a component that interacts with DynamoDB tables. While the structure of the table remains consistent across multiple tests, the seed data could vary based on what functionality you are testing. 

One of the solutions would be to create a fixture that sets up the table with the default data. However, this would mean that you would need to create a separate fixture for every minor variation. Instead, you can use the mark annotation to parametrize your fixtures and make them more dynamic.


The following example shows how you can use the mark annotation to parametrize your fixtures:

`tests/conftest.py`
```python
...
@pytest.fixture
def dynamodb_table(test_dir, request):
    # Default table schema
    table_schema = {
        "table_name": "default",
        "pk": "pk",
        "sk": "sk",
    }
    if request.node.get_closest_marker("dynamodb_table"):
        table_schema = {
            **table_schema, 
            # Override default table schema with custom parameters from the marker
            **request.node.get_closest_marker("dynamodb_table").kwargs
        }

    # Create table and load data
    with moto.mock_dynamodb():
        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
        table = dynamodb.create_table(
            ... # Create table based on the schema
        )
        if "data" in table_schema:
            data = json.load(open(path.join(test_dir, table_schema["data"]), "r"))

            with table.batch_writer() as process:
                for index, record in enumerate(data):
                    process.put_item(Item=record)
        yield table
        
        # Tear down the table
        client = boto3.client("dynamodb", region_name="eu-west-1")
        client.delete_table(TableName=table_schema["name"])
```
> Keep in mind the implementation details from the above code is removed for brevity.
> 
> Fully working is available on my [GitHub](https://github.com/dkraczkowski/dkraczkowski.github.io/articles/parametrize_your_fixtures/tests/conftest.py)

In the provided example, the `request` parameter within the Pytest fixture is an instance of a special object that offers insights into the current test run, specifically accessing markers set on tests. Utilizing this, the fixture is designed to set up a DynamoDB mock table with a schema and, if a `dynamodb_table` marker is associated with the current test, it fetches its custom parameters to potentially adjust the default table configurations or seed different data.

This way, you could use the same `dynamodb_table` fixture across multiple tests but parametrize it differently based on the need of each test. 

> You can read more about the `request` object in the [Pytest documentation](https://docs.pytest.org/en/6.2.x/reference.html#request).

Here's how you can use the fixture in your tests:

`tests/test_fixture.py`
```python
import pytest


@pytest.mark.dynamodb_table(name="test_table", data="fixtures/pets.json")
def test_parametrized_fixture(dynamodb_table) -> None:
    ...
```
> Fully working code is available on my [GitHub](https://github.com/dkraczkowski/dkraczkowski.github.io/articles/parametrize_your_fixtures/tests/test_fixture.py)

## Conclusion

Pytest's flexibility with fixtures and the ability to parametrize them using the mark annotation opens up opportunities for more concise and maintainable tests. This becomes especially invaluable in dynamic scenarios like the AWS DynamoDB example, ensuring your test setup is as efficient as the tests themselves.


That's all Folks!
