from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.titration.automatic_titration import AutomaticTitration
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface


# Test handleKey
@mock.patch.object(Titrator, "updateState")
def test_handleKey(updateStateMock):
    automaticTitration = AutomaticTitration(Titrator())

    automaticTitration.handleKey("1")
    assert automaticTitration.subState == 2

    automaticTitration.handleKey("1")
    assert automaticTitration.subState == 3

    automaticTitration.handleKey("1")
    assert automaticTitration.subState == 4

    automaticTitration.handleKey("0")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "MainMenu"


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    automaticTitration = AutomaticTitration(Titrator())

    automaticTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call(
                "Titrating to {} pH".format(
                    str(automaticTitration.values["pH_target"])
                ),
                line=1,
            ),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    automaticTitration.subState += 1
    automaticTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Mixing...", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    automaticTitration.subState += 1
    automaticTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call(
                "pH value {} reached".format(automaticTitration.values["current_pH"]),
                line=1,
            ),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    automaticTitration.subState += 1
    automaticTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Return to", line=1),
            mock.call("main menu", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )


@mock.patch.object(Titrator, "updateState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_AutomaticTitration(lcdOutMock, updateStateMock):
    automaticTitration = AutomaticTitration(Titrator())

    automaticTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call(
                "Titrating to {} pH".format(
                    str(automaticTitration.values["pH_target"])
                ),
                line=1,
            ),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    automaticTitration.handleKey("1")
    assert automaticTitration.subState == 2

    automaticTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Mixing...", line=1),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    automaticTitration.handleKey("1")
    assert automaticTitration.subState == 3

    automaticTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call(
                "pH value {} reached".format(automaticTitration.values["current_pH"]),
                line=1,
            ),
            mock.call("", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    automaticTitration.handleKey("1")
    assert automaticTitration.subState == 4

    automaticTitration.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Return to", line=1),
            mock.call("main menu", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )

    automaticTitration.handleKey("0")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "MainMenu"
