from __future__ import absolute_import
import pytest
import os


@pytest.fixture
def lineup():
    return "Steve Clark, Harrison Afful, Michael Parkhurst, Gaston Sauro, Waylon Francis, Wil Trapp, Tony Tchani (Cedrick Mabwati 67' (Tyson Wahl 115')), Ethan Finlay (sent off 85'), Federico Higuain, Justin Meram (Jack McInerney 74'), Kei Kamara"


@pytest.fixture
def excel():
    return _fixture_path('test.xlsx')


@pytest.fixture
def excel_sheets():
    return _fixture_path('test_sheets.xlsx')


@pytest.fixture
def excel_empty():
    return _fixture_path('test_empty.xlsx')


@pytest.fixture
def excel_games():
    return _fixture_path('test_games.xlsx')


@pytest.fixture
def excel_lineups():
    return _fixture_path('test_lineups.xlsx')


@pytest.fixture
def excel_players():
    return _fixture_path('test_players.xlsx')


@pytest.fixture
def data_teams():
    return _fixture_path('tbl_teams.csv')


def _fixture_path(path):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, 'fixtures', path)
