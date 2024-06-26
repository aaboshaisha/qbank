from myapp import create_app

def test_config():
    assert not create_app().testing # if app created with no test config passed, should see defaults
    # The assert not statement checks that the testing attribute is False by default.
    assert create_app({'Testing': True}).testing # app created with testing configs
    # The assert statement checks that the testing attribute is True when this configuration is applied.
    