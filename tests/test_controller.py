from src.controller import Controller


def test_set_url_file():
    controller = Controller()

    TEST_NAME = "test"
    controller.set_url_file(TEST_NAME)

    assert controller.url_file_name == TEST_NAME


def test_set_report_file():
    controller = Controller()

    TEST_NAME = "test"
    controller.set_report_file(TEST_NAME)

    assert controller.report_file_name == TEST_NAME


def test_set_destination():
    controller = Controller()

    TEST_NAME = "test"
    controller.set_destination(TEST_NAME)

    assert controller.destination == TEST_NAME
