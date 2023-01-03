from unittest import mock
from unittest.mock import ANY
from titration.utils.ui_state.main_menu import MainMenu
from titration.utils.ui_state.calibration.calibrate_temp import CalibrateTemp
from titration.utils.ui_state.calibration.setup_calibration import SetupCalibration
from titration.utils.titrator import Titrator
from titration.utils import lcd_interface


# Test handleKey
@mock.patch.object(Titrator, "updateState")
def test_handleKey(updateStateMock):
    calibrateTemp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrateTemp.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    assert calibrateTemp.subState == 2

    calibrateTemp.handleKey("1")
    assert calibrateTemp.subState == 3

    calibrateTemp.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "SetupCalibration"


# Test loop
@mock.patch.object(lcd_interface, "lcd_out")
def test_loop(lcdOutMock):
    calibrateTemp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Set Ref solution", line=1),
            mock.call("temp", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibrateTemp.subState += 1
    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Put probe in sol", line=1),
            mock.call("", line=2),
            mock.call("Press 1 to", line=3),
            mock.call("record value", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibrateTemp.subState += 1
    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Recorded temp:", line=1),
            mock.call(
                "{0:0.3f}".format(calibrateTemp.values["actual_temperature"]), line=2
            ),
            mock.call("{}".format(calibrateTemp.values["new_ref_resistance"]), line=3),
            mock.call("", line=4),
        ]
    )


# Test CalibrateTemp
@mock.patch.object(Titrator, "updateState")
@mock.patch.object(lcd_interface, "lcd_out")
def test_CalibrateTemp(lcdOutMock, updateStateMock):
    calibrateTemp = CalibrateTemp(
        Titrator(), SetupCalibration(MainMenu(Titrator()), Titrator())
    )

    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Set Ref solution", line=1),
            mock.call("temp", line=2),
            mock.call("Press any to cont", line=3),
            mock.call("", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibrateTemp.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "UserValue"
    assert calibrateTemp.subState == 2

    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Put probe in sol", line=1),
            mock.call("", line=2),
            mock.call("Press 1 to", line=3),
            mock.call("record value", line=4),
        ]
    )
    lcdOutMock.reset_called()

    calibrateTemp.handleKey("1")
    assert calibrateTemp.subState == 3

    calibrateTemp.loop()
    lcdOutMock.assert_has_calls(
        [
            mock.call("Recorded temp:", line=1),
            mock.call(
                "{0:0.3f}".format(calibrateTemp.values["actual_temperature"]), line=2
            ),
            mock.call("{}".format(calibrateTemp.values["new_ref_resistance"]), line=3),
            mock.call("", line=4),
        ]
    )

    calibrateTemp.handleKey("1")
    updateStateMock.assert_called_with(ANY)
    assert updateStateMock.call_args.args[0].name() == "SetupCalibration"
