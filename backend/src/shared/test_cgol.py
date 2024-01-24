import pytest
import cgol_lobby
import numpy as np

p1 = cgol_lobby.Player("Player 1", 2)
p2 = cgol_lobby.Player("Player 2", 3)

#testing board initialization
def test_init_1():
    #empty board, no players
    settings = cgol_lobby.CGOLDefaultSettings(0, 0)
    lobby = cgol_lobby.CGOLLobby(settings)
    CGOL_instance = lobby.start_game()

    assert np.array_equal(CGOL_instance.board, np.zeros((0, 0))) == True
    assert CGOL_instance.players == []

def test_init_2():
    #5x5 board, no players
    settings = cgol_lobby.CGOLDefaultSettings(5, 5)
    lobby = cgol_lobby.CGOLLobby(settings)
    CGOL_instance = lobby.start_game()

    assert np.array_equal(CGOL_instance.board, np.zeros((5, 5))) == True
    assert CGOL_instance.players == []

def test_init_3():
    #10x10 board, 2 players
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    assert np.array_equal(CGOL_instance.board, np.zeros((10, 10))) == True
    assert CGOL_instance.players == [p1, p2]

def test_init_4():
    #10x10 board, 2 players with same name and color
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p1)
    CGOL_instance = lobby.start_game()

    assert np.array_equal(CGOL_instance.board, np.zeros((10, 10))) == True
    assert CGOL_instance.players == [p1]

def test_init_5():
    #10x10 board, 2 players with same name
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    temp = cgol_lobby.Player("Player 1", 3)
    lobby.add_player(p1)
    lobby.add_player(temp)
    CGOL_instance = lobby.start_game()

    assert np.array_equal(CGOL_instance.board, np.zeros((10, 10))) == True
    assert CGOL_instance.players == [p1]

def test_init_6():
    #10x10 board, 2 players with same color
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    temp = cgol_lobby.Player("Player 2", 2)
    lobby.add_player(p1)
    lobby.add_player(temp)
    CGOL_instance = lobby.start_game()

    assert np.array_equal(CGOL_instance.board, np.zeros((10, 10))) == True
    assert CGOL_instance.players == [p1]


#testing board update functionality after user input
def test_update_1():
    #10x10 board, 2 players, both try to place on (5, 5) (p1 then p2)
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 5), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(5, 5), 0)]
    results = CGOL_instance.update_board(updates)
    temp = np.zeros((10, 10))
    temp[5][5] = 2

    assert results[0] == True
    assert results[1] == False
    assert np.array_equal(CGOL_instance.board, temp) == True

def test_update_2():
    #10x10 board, 2 players, p1 places on (0, 1) and p2 places on (0, 2)
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(0, 1), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(0, 2), 0)]
    results = CGOL_instance.update_board(updates)
    temp = np.zeros((10, 10))
    temp[0][1] = 2
    temp[0][2] = 3

    assert results[0] == True
    assert results[1] == True
    assert np.array_equal(CGOL_instance.board, temp) == True


#testing food generation
def test_food_1():
    #10x10 board, 2 players, p1 places on (5, 5), p2 places on (2, 2), rest of board is filled with food
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 5), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(2, 2), 0)]
    CGOL_instance.update_board(updates)
    CGOL_instance.spawn_food(1)
    temp = np.ones((10, 10))
    temp[5][5] = 2
    temp[2][2] = 3

    assert np.array_equal(CGOL_instance.board, temp) == True

def test_food_2():
    #10x10 board, 2 players, p1 places on (3, 5), p2 places on (1, 2), rest of board has 50% chance to have food on a given tile
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(3, 5), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(1, 2), 0)]
    CGOL_instance.update_board(updates)
    CGOL_instance.spawn_food(0.5)

    assert 1 in CGOL_instance.board
    assert CGOL_instance.board[3][5] == 2
    assert CGOL_instance.board[1][2] == 3


#testing pixel evolution after a time step
def test_step_1():
    #10x10 board, 2 players, p1 places on (5, 5), p2 places on (2, 2), game moves forward 1 step
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 5), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(2, 2), 0)]
    CGOL_instance.update_board(updates)
    CGOL_instance.step()
    temp = np.zeros((10, 10))

    assert np.array_equal(CGOL_instance.board, temp)

def test_step_2():
    #10x10 board, 2 players, p1 places on (5, 5), (5, 4), and (4, 5); p2 places on (2, 2), (1, 2), and (2, 1), game moves forward 1 step
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 5), 0), cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 4), 0), cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(4, 5), 0),
               cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(2, 2), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(2, 1), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(1, 2), 0)]
    CGOL_instance.update_board(updates)
    CGOL_instance.step()
    temp = np.zeros((10, 10))
    temp[5][5], temp[5][4], temp[4][5], temp[4][4] = [2, 2, 2, 2]
    temp[2][2], temp[2][1], temp[1][2], temp[1][1] = [3, 3, 3, 3]

    assert np.array_equal(CGOL_instance.board, temp)

def test_step_3():
    #10x10 board, 2 players, p1 places on (5, 5) and (5, 4), p2 places on (3, 3), (4, 4), and (3, 4), game moves forward 1 step
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 5), 0), cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 4), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(3, 3), 0),
               cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(4, 4), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(3, 4), 0)]
    CGOL_instance.update_board(updates)
    CGOL_instance.step()
    temp = np.zeros((10, 10))
    temp[3][3], temp[3, 4] = [3, 3]

    assert np.array_equal(CGOL_instance.board, temp)

    #game moves forward another step
    CGOL_instance.step()

    assert np.array_equal(CGOL_instance.board, np.zeros((10, 10)))

def test_step_4():
    #10x10 board, 2 players, p1 places on (5, 5) and (5, 4), p2 places on (2, 2) and (2, 1), game moves forward 1 step
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 5), 0), cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 4), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(2, 2), 0),
               cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(2, 1), 0)]
    CGOL_instance.update_board(updates)
    CGOL_instance.step()
    temp = np.zeros((10, 10))

    assert np.array_equal(CGOL_instance.board, temp)


#testing player stats after they perform actions and time steps pass
def test_stats_1():
    #10x10 board, 2 players, p1 places on (5, 5), (5, 4), and (4, 5); p2 places on (2, 2), (1, 2), and (2, 1), game moves forward 1 step
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 5), 0), cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 4), 0), cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(4, 5), 0),
               cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(2, 2), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(2, 1), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(1, 2), 0)]
    CGOL_instance.update_board(updates)
    CGOL_instance.step()
    p1_stats = cgol_lobby.PlayerStats(p1)
    p1_stats.cells_created = 1
    p1_stats.contested_areas = 0
    p1_stats.total_food_captured = 0
    p2_stats = cgol_lobby.PlayerStats(p2)
    p2_stats.cells_created = 1
    p2_stats.contested_areas = 0
    p2_stats.total_food_captured = 0
    player_stats = CGOL_instance.get_stats()

    assert (p1_stats.player.username == player_stats[0].player.username and p1_stats.player.color_no == player_stats[0].player.color_no and p1_stats.cells_created == player_stats[0].cells_created 
            and p1_stats.contested_areas == player_stats[0].contested_areas and p1_stats.total_food_captured == player_stats[0].total_food_captured)
    assert (p2_stats.player.username == player_stats[1].player.username and p2_stats.player.color_no == player_stats[1].player.color_no and p2_stats.cells_created == player_stats[1].cells_created 
            and p2_stats.contested_areas == player_stats[1].contested_areas and p2_stats.total_food_captured == player_stats[1].total_food_captured)
    
def test_stats_2():
    #10x10 board, 2 players, p1 places on (5, 5); p2 places on (2, 2), game moves forward 1 step
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 5), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(2, 2), 0)]
    CGOL_instance.update_board(updates)
    CGOL_instance.step()
    p1_stats = cgol_lobby.PlayerStats(p1)
    p1_stats.cells_created = 0
    p1_stats.contested_areas = 0
    p1_stats.total_food_captured = 0
    p2_stats = cgol_lobby.PlayerStats(p2)
    p2_stats.cells_created = 0
    p2_stats.contested_areas = 0
    p2_stats.total_food_captured = 0
    player_stats = CGOL_instance.get_stats()

    assert (p1_stats.player.username == player_stats[0].player.username and p1_stats.player.color_no == player_stats[0].player.color_no and p1_stats.cells_created == player_stats[0].cells_created 
            and p1_stats.contested_areas == player_stats[0].contested_areas and p1_stats.total_food_captured == player_stats[0].total_food_captured)
    assert (p2_stats.player.username == player_stats[1].player.username and p2_stats.player.color_no == player_stats[1].player.color_no and p2_stats.cells_created == player_stats[1].cells_created 
            and p2_stats.contested_areas == player_stats[1].contested_areas and p2_stats.total_food_captured == player_stats[1].total_food_captured)
    
def test_stats_3():
    #10x10 board, 1.0 food spawn rate, 2 players, p1 places on (5, 5), (5, 4), and (4, 5); p2 places on (2, 2), (1, 2), and (2, 1), game moves forward 1 step
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    settings.spawn_rate = 1
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 5), 0), cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 4), 0), cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(4, 5), 0),
               cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(2, 2), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(2, 1), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(1, 2), 0)]
    CGOL_instance.update_board(updates)
    CGOL_instance.spawn_food()
    CGOL_instance.step()
    p1_stats = cgol_lobby.PlayerStats(p1)
    p1_stats.cells_created = 1
    p1_stats.contested_areas = 0
    p1_stats.total_food_captured = 1
    p2_stats = cgol_lobby.PlayerStats(p2)
    p2_stats.cells_created = 1
    p2_stats.contested_areas = 0
    p2_stats.total_food_captured = 1
    player_stats = CGOL_instance.get_stats()

    assert (p1_stats.player.username == player_stats[0].player.username and p1_stats.player.color_no == player_stats[0].player.color_no and p1_stats.cells_created == player_stats[0].cells_created 
            and p1_stats.contested_areas == player_stats[0].contested_areas and p1_stats.total_food_captured == player_stats[0].total_food_captured)
    assert (p2_stats.player.username == player_stats[1].player.username and p2_stats.player.color_no == player_stats[1].player.color_no and p2_stats.cells_created == player_stats[1].cells_created 
            and p2_stats.contested_areas == player_stats[1].contested_areas and p2_stats.total_food_captured == player_stats[1].total_food_captured)
    
def test_stats_4():
    #10x10 board, 2 players, p1 places on (5, 5) and (5, 4), p2 places on (3, 3), (4, 4), and (3, 4), game moves forward 1 step
    settings = cgol_lobby.CGOLDefaultSettings(10, 10)
    lobby = cgol_lobby.CGOLLobby(settings)
    lobby.add_player(p1)
    lobby.add_player(p2)
    CGOL_instance = lobby.start_game()

    updates = [cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 5), 0), cgol_lobby.SquareUpdate(p1, cgol_lobby.Coordinate(5, 4), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(3, 3), 0),
               cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(4, 4), 0), cgol_lobby.SquareUpdate(p2, cgol_lobby.Coordinate(3, 4), 0)]
    CGOL_instance.update_board(updates)
    CGOL_instance.step()
    p1_stats = cgol_lobby.PlayerStats(p1)
    p1_stats.cells_created = 0
    p1_stats.contested_areas = 6
    p1_stats.total_food_captured = 0
    p2_stats = cgol_lobby.PlayerStats(p2)
    p2_stats.cells_created = 0
    p2_stats.contested_areas = 6
    p2_stats.total_food_captured = 0
    player_stats = CGOL_instance.get_stats()

    assert (p1_stats.player.username == player_stats[0].player.username and p1_stats.player.color_no == player_stats[0].player.color_no and p1_stats.cells_created == player_stats[0].cells_created 
            and p1_stats.contested_areas == player_stats[0].contested_areas and p1_stats.total_food_captured == player_stats[0].total_food_captured)
    assert (p2_stats.player.username == player_stats[1].player.username and p2_stats.player.color_no == player_stats[1].player.color_no and p2_stats.cells_created == player_stats[1].cells_created 
            and p2_stats.contested_areas == player_stats[1].contested_areas and p2_stats.total_food_captured == player_stats[1].total_food_captured)