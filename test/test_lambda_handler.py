from json import dumps

from mock import Mock, MagicMock, patch
import pytest

from src.lambda_function import lambda_handler, get_random_text, LambdaException

line_1 = 'Having money ain\'t everything'
line_2 = 'Not having it is'

@patch('src.lambda_function.boto3.resource')
@patch('src.lambda_function.get_random_text')
def test_lambda_handler_happy_path(
    mock_get_random_text, mock_get_table_resource
):
    mock_get_random_text.return_value = {
        'firstLine': line_1, 'secondLine': line_2
    }

    assert lambda_handler(None, None) == {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'body': dumps({
            'firstLine': line_1, 'secondLine': line_2
        })
    }

@patch('src.lambda_function.boto3.resource')
@patch('src.lambda_function.get_random_text')
def test_lambda_handler_handles_lambda_exception(
    mock_get_random_text, mock_get_table_resource
    ):
    mock_get_random_text.side_effect = LambdaException('asdf', 404)
    
    assert lambda_handler(None, None) == {
        'functionError': 'asdf',
        'statusCode': 404
    }

@patch('src.lambda_function.boto3.resource')
@patch('src.lambda_function.get_random_text')
def test_lambda_handler_handles_general_exceptions(
    mock_get_random_text, mock_get_table_resource
):
    mock_get_random_text.side_effect = AttributeError
    assert lambda_handler(None, None) == {
        'functionError': 'Service failed unexpectedly',
        'statusCode': 500
}

def test_get_random_text_gets_good_result_first_try():
    table = Mock()
    table.query.return_value = {
        'Items': [{
            'firstLine': line_1,
            'secondLine': line_2
        }]
    }
    
    response = get_random_text(table)

    assert response == {'firstLine': line_1, 'secondLine': line_2}
    assert table.query.call_count == 1

def test_get_random_text_gets_good_result_second_try():
    table = Mock()
    table.query.side_effect = [
        {
            'Items': []
        },
        {   
            'Items': [{
                'firstLine': line_1,
                'secondLine': line_2
            }]    
        }
    ]

    response = get_random_text(table)
    assert response == {'firstLine': line_1, 'secondLine': line_2}
    assert table.query.call_count == 2

def test_get_random_text_fails_after_first_retry():
    table = Mock()
    table.query.return_value = {'Items': []}
    with pytest.raises(LambdaException) as context:
        get_random_text(table)
    
    assert context.value.status_code == 404

