from caseflow.tools import _get_account as get_account, _list_open_cases as list_open_cases, _create_draft_reply as create_draft_reply

def test_get_account():

    valid_id_response = get_account("ACC-1001")
    invalid_id_rsponse = get_account("ACC-1000")
    no_id_repsonse = get_account("")

    assert valid_id_response == {"name": "Jordan Lee", "plan": "Pro", "status": "active", "region": "US"} 
    assert invalid_id_rsponse == {"error": "account_not_found_or_not_permitted"} 
    assert no_id_repsonse == {"error": "account_not_found_or_not_permitted"}

def test_list_open_cases():
    valid_id_response = list_open_cases("ACC-2002")
    invalid_id_rsponse = list_open_cases("AC-5000")
    no_id_repsonse = list_open_cases("")

    assert valid_id_response == [{"case_id": "K-12", "status": "open", "topic": "login", "opened": "2026-08-28"}] 
    assert invalid_id_rsponse == []
    assert no_id_repsonse == []

def test_create_draft_reply():
    valid_id_response = create_draft_reply("ACC-1001", "summary text", "proposed text")
    invalid_id_rsponse = create_draft_reply("ACC-9999", "summary text", "proposed text")
    no_id_repsonse = create_draft_reply("", "summary text", "proposed text")

    expected_fields = {"draft_id", "status"}

    assert expected_fields.issubset(valid_id_response.keys())
    assert expected_fields.issubset(invalid_id_rsponse.keys())
    assert expected_fields.issubset(no_id_repsonse.keys())