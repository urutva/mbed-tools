#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Tests for sync_board_database.py."""
from unittest import TestCase

from ci_scripts import sync_board_database

from mbed_tools.targets.boards import Boards
from mbed_tools.targets import Board


BOARD_1 = {
    "type": "target",
    "id": "1",
    "attributes": {
        "features": {
            "mbed_enabled": ["Advanced"],
            "mbed_os_support": [
                "Mbed OS 5.10",
                "Mbed OS 5.11",
                "Mbed OS 5.12",
                "Mbed OS 5.13",
                "Mbed OS 5.14",
                "Mbed OS 5.15",
                "Mbed OS 5.8",
                "Mbed OS 5.9",
            ],
            "antenna": ["Connector", "Onboard"],
            "certification": [
                "Anatel (Brazil)",
                "AS/NZS (Australia and New Zealand)",
                "CE (Europe)",
                "FCC/CFR (USA)",
                "IC RSS (Canada)",
                "ICASA (South Africa)",
                "KCC (South Korea)",
                "MIC (Japan)",
                "NCC (Taiwan)",
                "RoHS (Europe)",
            ],
            "communication": ["Bluetooth & BLE"],
            "interface_firmware": ["DAPLink", "J-Link"],
            "target_core": ["Cortex-M4"],
            "mbed_studio_support": ["Build and run"],
        },
        "board_type": "MTB_UBLOX_NINA_B1",
        "flash_size": 512,
        "name": "u-blox NINA-B1",
        "product_code": "0455",
        "ram_size": 64,
        "target_type": "module",
        "hidden": False,
        "device_name": "nRF52832_xxAA",
    },
}

BOARD_2 = {
    "type": "target",
    "id": "2",
    "attributes": {
        "features": {
            "mbed_enabled": ["Advanced"],
            "mbed_os_support": [
                "Mbed OS 5.10",
                "Mbed OS 5.11",
                "Mbed OS 5.12",
                "Mbed OS 5.13",
                "Mbed OS 5.14",
                "Mbed OS 5.15",
                "Mbed OS 5.8",
                "Mbed OS 5.9",
            ],
            "antenna": ["Connector"],
            "certification": ["AS/NZS (Australia and New Zealand)", "CE (Europe)", "FCC/CFR (USA)", "IC RSS (Canada)"],
            "communication": ["LoRa"],
            "interface_firmware": ["DAPLink"],
            "target_core": ["Cortex-M3"],
            "mbed_studio_support": ["Build and run"],
        },
        "board_type": "MTB_MTS_XDOT",
        "flash_size": 256,
        "name": "Multitech xDOT",
        "product_code": "0453",
        "ram_size": 64,
        "target_type": "module",
        "hidden": False,
        "device_name": "STM32L151CC",
    },
}


def _make_mbed_boards_for_diff(boards_a, boards_b):
    return (
        Boards(Board.from_online_board_entry(b) for b in boards_a),
        Boards(Board.from_online_board_entry(b) for b in boards_b),
    )


class TestBoardDatabasePath(TestCase):
    def test_board_database_path_exists(self):
        self.assertTrue(sync_board_database.BOARD_DATABASE_PATH.exists())


class TestDetermineBoardDatabaseUpdateResult(TestCase):
    def test_detects_added(self):
        mock_online_boards, mock_offline_boards = _make_mbed_boards_for_diff([BOARD_1, BOARD_2], [BOARD_1])
        result = sync_board_database.determine_board_database_update_result(mock_offline_boards, mock_online_boards)
        self.assertEqual(len(result.boards_added), 1, "Expect one new board to be added to offline db.")
        self.assertEqual(len(result.boards_removed), 0, "Expect no boards to be removed from offline db.")

    def test_detects_removed(self):
        mock_offline_boards, mock_online_boards = _make_mbed_boards_for_diff([BOARD_1, BOARD_2], [BOARD_1])
        result = sync_board_database.determine_board_database_update_result(mock_offline_boards, mock_online_boards)
        self.assertEqual(len(result.boards_added), 0, "Expect no boards to be added to offline db.")
        self.assertEqual(len(result.boards_removed), 1, "Expect one board to be removed from offline db.")

    def test_returns_empty_when_no_change(self):
        mock_offline_boards, mock_online_boards = _make_mbed_boards_for_diff([BOARD_1], [BOARD_1])
        result = sync_board_database.determine_board_database_update_result(mock_offline_boards, mock_online_boards)
        self.assertEqual(len(result.boards_added), 0, "Returns an empty targets container when no targets added")
        self.assertEqual(len(result.boards_removed), 0, "Returns an empty targets container when no targets removed.")


class TestCreateNewsFileTextFromResult(TestCase):
    def test_text_formatting_for_boards_added(self):
        mock_online_boards, mock_offline_boards = _make_mbed_boards_for_diff([BOARD_1, BOARD_2], [])
        result = sync_board_database.determine_board_database_update_result(
            online_boards=mock_online_boards, offline_boards=mock_offline_boards
        )
        text = sync_board_database.create_news_file_text_from_result(result)
        self.assertEqual(
            text,
            f"Targets added: {BOARD_1['attributes']['name']}, {BOARD_2['attributes']['name']}.\n",
            "Text is formatted correctly.",
        )

    def test_text_formatting_for_boards_removed(self):
        mock_online_boards, mock_offline_boards = _make_mbed_boards_for_diff([], [BOARD_1, BOARD_2])
        result = sync_board_database.determine_board_database_update_result(
            online_boards=mock_online_boards, offline_boards=mock_offline_boards
        )
        text = sync_board_database.create_news_file_text_from_result(result)
        self.assertEqual(
            text,
            f"Targets removed: {BOARD_1['attributes']['name']}, {BOARD_2['attributes']['name']}.\n",
            "Text is formatted correctly.",
        )

    def test_text_formatting_for_boards_added_and_removed(self):
        mock_online_boards, mock_offline_boards = _make_mbed_boards_for_diff([BOARD_1], [BOARD_2])
        result = sync_board_database.determine_board_database_update_result(
            online_boards=mock_online_boards, offline_boards=mock_offline_boards
        )
        text = sync_board_database.create_news_file_text_from_result(result)
        self.assertEqual(
            text,
            f"Targets added: {BOARD_1['attributes']['name']}.\nTargets removed: {BOARD_2['attributes']['name']}.\n",
            "Text is formatted correctly.",
        )
