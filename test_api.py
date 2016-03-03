"""
Test module
"""

import pytest
import diff_api
import json


@pytest.fixture
def client():
    """Fixture form Flask"""
    return diff_api.app.test_client()


def post_data(client, side, data):
    """
    Helper to post data

    :param client: Flask client
    :param side: 'left' or 'right'
    :param data: payload
    :return: <class 'flask.wrappers.Response'>
    """
    return client.post('/v1/diff/%s' % side, data=data,
                follow_redirects=True)


payload = """eyJtZW51Ijogew0KICAiaWQiOiAiZmlsZSIsDQogICJ2YWx1ZSI6ICJGaWxlIiwNCiAgInBvcHVwIjogew0KICAgICJtZW51aXRlbSI6IFsNCiAgICAgIHsidmFsdWUiOiAiTmV3IiwgIm9uY2xpY2siOiAiQ3JlYXRlTmV3RG9jKCkifSwNCiAgICAgIHsidmFsdWUiOiAiT3BlbiIsICJvbmNsaWNrIjogIk9wZW5Eb2MoKSJ9LA0KICAgICAgeyJ2YWx1ZSI6ICJDbG9zZSIsICJvbmNsaWNrIjogIkNsb3NlRG9jKCkifQ0KICAgIF0NCiAgfQ0KfX0="""
payload2 = """eyJtZW51Ijogew0KICAiaWQiOiAiZmlsZSIsDQogICJ2YWx1ZSI6ICJGaWxlIiwNCiAgInBvcHVwIjogew0KICAgICJtZW51aXRlbSI6IFsNCiAgICAgIHsidmFsdWUiOiAiT2xkIiwgIm9uY2xpY2siOiAiQ3JlYXRlTmV3RG9jKCkifSwNCiAgICAgIHsidmFsdWUiOiAiT3BlbiIsICJvbmNsaWNrIjogIk9wZW5Eb2MoKSJ9LA0KICAgICAgeyJ2YWx1ZSI6ICJDbG9zZSIsICJvbmNsaWNrIjogIkNsb3NlRG9jKCkifQ0KICAgIF0NCiAgfQ0KfX0="""
payload_wrong_json ="""eyJtZW51Ijogew0KICAiaWQiOiAiZmlsZSIsDQogICJ2YWx1ZSI6ICJGaWxlIiwNCiAgInBvcHVwIjogew0KICAgICJtZW51aXRlbSI6IFsNCiAgICAgIHsidmFsdWUiOiAiTmV3IiwgIm9uY2xpY2siOiAiQ3JlYXRlTmV3RG9jKCkifSwNCiAgICAgIHsidmFsdWUiOiAiT3BlbiIsICJvbmNsaWNrIjogIk9wZW5Eb2MoKSJ9LA0KICAgICAgeyJ2YWx1ZSI6ICJDbG9zZSIsICJvbmNsaWNrIjogIkNsb3NlRG9jKCkifQ0KICAgIF1dDQogIH0NCn19"""
payload_wrong_base64 ="""eyJtZW51Ijogew0KICAiaWQiOiAiZmlsZSIsDQogICJ2YWx1ZSI6ICJGaWxlIiwNCiAgInBvcHVwIjogew0KICAgICJtZW51aXRlbSI6IFsNCiAgICAgIHsidmFsdWUiOiAiTmV3IiwgIm9uY2xpY2siOiAiQ3JV3RG9jKCkifSwNCiAgICAgIHsidmFsdWUiOiAiT3BlbiIsICJvbmNsaWNrIjogIk9wZW5Eb2MoKSJ9LA0KICAgICAgeyJ2YWx1ZSI6ICJDbG9zZSIsICJvbmNsaWNrIjogIkNsb3NlRG9jKCkifQ0KICAgIF0NCiAgfQ0KfX0="""
jsn = {"menu": {
    "id": "file",
    "value": "File",
    "popup": {
        "menuitem": [
            {"value": "New", "onclick": "CreateNewDoc()"},
            {"value": "Open", "onclick": "OpenDoc()"},
            {"value": "Close", "onclick": "CloseDoc()"}
        ]
    }
    }}


def side_t(client, side):
    """
    Helper to to test one of side.

    :param client: Flask client
    :param side: 'left' or 'right'
    :return:
    """
    global payload, payload_wrong_json, payload_wrong_base64, jsn
    r = client.get('/v1/diff/%s' % side)
    assert r.status_code == 200
    assert '' == json.loads(r.data.decode('utf-8'))

    # test post request with correct payload
    r = post_data(client, side, payload)
    assert r.status_code == 202
    assert jsn == json.loads(r.data.decode('utf-8'))

    # test post request with wrong payload
    r = post_data(client, side, payload_wrong_json)
    assert r.status_code == 406

    # test post request with wrong payload
    r = post_data(client, side, payload_wrong_base64)
    assert r.status_code == 406


def test_byte_to_json():
    """ Test byte_to_json method"""
    global payload, json
    r = diff_api.byte64_to_json(payload)
    assert r == jsn


def test_diff_left(client):
    """ Test /v1/diff/left"""
    side_t(client, 'left')


def test_diff_right(client):
    """ Test /v1/diff/right"""
    side_t(client, 'right')


def test_diff(client):
    """Test /v1/diff"""
    # delete all data
    client.delete('/v1/diff/left')
    client.delete('/v1/diff/right')
    r = client.get('/v1/diff')
    assert r.status_code == 412

    # test same payload
    global payload
    post_data(client, 'right', payload)
    post_data(client, 'left', payload)
    r = client.get('/v1/diff')
    assert r.status_code == 200
    assert {'diff': True} == json.loads(r.data.decode('utf-8'))

    # test different payload
    r = post_data(client, 'left', payload2)
    assert r.status_code == 202
    r = client.get('/v1/diff')
    assert {'diff': False} == json.loads(r.data.decode('utf-8'))
