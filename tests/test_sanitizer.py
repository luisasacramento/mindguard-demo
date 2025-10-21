from app.utils.sanitizer import sanitize_username

def test_good_username():
    assert sanitize_username("luisa_99") == "luisa_99"

def test_bad_username():
    assert sanitize_username("bad user!") is None
