from typing import Optional, List
from uuid import UUID, uuid4
from domain.model.current_game import CurrentGame
from domain.model.game_field import GameField
from domain.model.game_state import GameState
from domain.model.game_type import GameType
from domain.model.player_symbol import PlayerSymbol
from domain.model.leader_stats import LeaderStats
from domain.service.game_service_interface import GameServiceInterface
from domain.service.user_service import UserService
from datasource.repository.game_repository import GameRepository
from datasource.mapper.game_mapper import GameMapper


class GameServiceImpl(GameServiceInterface):
    def __init__(self, repository: GameRepository, user_service: UserService = None):
        self._repository = repository
        self._mapper = GameMapper()
        self._user_service = user_service

    def create_game(self, player_id: UUID, game_type: GameType) -> CurrentGame:
        game_id = uuid4()
        empty_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        game_field = GameField(board=empty_board)

        player1_symbol = PlayerSymbol.X
        player2_symbol = PlayerSymbol.O

        if game_type == GameType.PVP:
            game = CurrentGame(
                game_id=game_id,
                game_field=game_field,
                game_type=game_type,
                game_state=GameState.WAITING_FOR_PLAYER,
                player1_id=player_id,
                player2_id=None,
                player1_symbol=player1_symbol,
                player2_symbol=player2_symbol,
                current_player_id=None,
                winner_id=None,
            )
        else:
            game = CurrentGame(
                game_id=game_id,
                game_field=game_field,
                game_type=game_type,
                game_state=GameState.PLAYER_TURN,
                player1_id=player_id,
                player2_id=None,
                player1_symbol=player1_symbol,
                player2_symbol=player2_symbol,
                current_player_id=player_id,
                winner_id=None,
            )

        entity = self._mapper.to_entity(game)
        saved_entity = self._repository.save_game(entity)

        return self._mapper.to_domain(saved_entity)

    def join_game(self, game_id: UUID, player_id: UUID) -> CurrentGame:
        entity = self._repository.get_game(game_id)
        if not entity:
            raise ValueError(f"Game with ID {game_id} not found")

        game = self._mapper.to_domain(entity)

        if game.game_state != GameState.WAITING_FOR_PLAYER:
            raise ValueError("Game is not available for joining")

        if game.game_type != GameType.PVP:
            raise ValueError("Only PvP games can be joined")

        if game.player1_id == player_id:
            raise ValueError("Cannot join your own game")

        game.player2_id = player_id
        game.game_state = GameState.PLAYER_TURN
        game.current_player_id = game.player1_id

        entity = self._mapper.to_entity(game)
        saved_entity = self._repository.save_game(entity)

        return self._mapper.to_domain(saved_entity)

    def make_move(
        self, game_id: UUID, player_id: UUID, board: List[List[int]]
    ) -> CurrentGame:

        entity = self._repository.get_game(game_id)
        if not entity:
            raise ValueError(f"Game with ID {game_id} not found")

        game = self._mapper.to_domain(entity)

        if game.is_game_over():
            raise ValueError("Game is already over")

        if not game.is_player_turn(player_id):
            raise ValueError("Not your turn")

        if not board or len(board) != 3 or any(len(row) != 3 for row in board):
            raise ValueError("Invalid board format")

        game.game_field = GameField(board=board)

        self._update_game_state(game)

        entity = self._mapper.to_entity(game)
        saved_entity = self._repository.save_game(entity)
        game = self._mapper.to_domain(saved_entity)

        if not game.is_game_over() and game.game_type == GameType.PVC:
            game = self._make_computer_move(game)

        if not game.is_game_over() and game.game_type == GameType.PVP:
            game.current_player_id = game.get_opponent_id(player_id)
            entity = self._mapper.to_entity(game)
            saved_entity = self._repository.save_game(entity)
            game = self._mapper.to_domain(saved_entity)

        return game

    def _make_computer_move(self, game: CurrentGame) -> CurrentGame:
        board = game.game_field.board
        best_score = float("-inf")
        best_move = None

        computer_symbol = game.player2_symbol
        player_symbol = game.player1_symbol

        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = computer_symbol.value
                    score = self._minimax(
                        board, 0, False, computer_symbol, player_symbol
                    )
                    board[i][j] = 0

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            new_board = [row[:] for row in board]
            new_board[best_move[0]][best_move[1]] = computer_symbol.value
            game.game_field = GameField(board=new_board)

            self._update_game_state(game)

            if not game.is_game_over():
                game.current_player_id = game.player1_id

            entity = self._mapper.to_entity(game)
            saved_entity = self._repository.save_game(entity)
            return self._mapper.to_domain(saved_entity)

        return game

    def _minimax(
        self,
        board: List[List[int]],
        depth: int,
        is_maximizing: bool,
        computer_symbol: PlayerSymbol,
        player_symbol: PlayerSymbol,
    ) -> int:
        winner_symbol = self._check_winner_symbol(board)

        if winner_symbol == computer_symbol.value:
            return 10 - depth
        elif winner_symbol == player_symbol.value:
            return depth - 10
        elif self._is_board_full(board):
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = computer_symbol.value
                        score = self._minimax(
                            board, depth + 1, False, computer_symbol, player_symbol
                        )
                        board[i][j] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = player_symbol.value
                        score = self._minimax(
                            board, depth + 1, True, computer_symbol, player_symbol
                        )
                        board[i][j] = 0
                        best_score = min(score, best_score)
            return best_score

    def _update_game_state(self, game: CurrentGame) -> None:
        winner_symbol = self._check_winner_symbol(game.game_field.board)

        if winner_symbol is not None:
            if winner_symbol == game.player1_symbol.value:
                game.winner_id = game.player1_id
            elif winner_symbol == game.player2_symbol.value:
                if game.game_type == GameType.PVP:
                    game.winner_id = game.player2_id
                else:
                    game.winner_id = None

            game.game_state = GameState.PLAYER_WON
            game.current_player_id = None
        elif self._is_board_full(game.game_field.board):
            game.game_state = GameState.DRAW
            game.current_player_id = None
            game.winner_id = None

    def _check_winner_symbol(self, board: List[List[int]]) -> Optional[int]:

        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != 0:
                return board[i][0]

        for j in range(3):
            if board[0][j] == board[1][j] == board[2][j] != 0:
                return board[0][j]

        if board[0][0] == board[1][1] == board[2][2] != 0:
            return board[0][0]

        if board[0][2] == board[1][1] == board[2][0] != 0:
            return board[0][2]

        return None

    def _is_board_full(self, board: List[List[int]]) -> bool:

        return all(board[i][j] != 0 for i in range(3) for j in range(3))

    def get_game(self, game_id: UUID) -> Optional[CurrentGame]:

        entity = self._repository.get_game(game_id)
        if entity:
            return self._mapper.to_domain(entity)
        return None

    def get_available_games(self) -> List[CurrentGame]:

        entities = self._repository.get_available_games()
        return [self._mapper.to_domain(entity) for entity in entities]

    def get_completed_games_by_user(self, user_id: UUID) -> List[CurrentGame]:
        entities = self._repository.get_completed_games_by_user(user_id)
        return [self._mapper.to_domain(entity) for entity in entities]

    def get_leaderboard(self, limit: int) -> List[LeaderStats]:
        if limit < 1:
            raise ValueError("Limit must be greater than 0")
        if limit > 100:
            raise ValueError("Limit must not exceed 100")

        leaderboard_data = self._repository.get_leaderboard(limit)

        result = []

        for user_id, win_ratio, wins, total in leaderboard_data:
            user = None
            if self._user_service:
                user = self._user_service.find_by_id(user_id)

            login = user.login if user else str(user_id)

            result.append(
                LeaderStats(user_id=user_id, login=login, win_ratio=win_ratio)
            )

        return result
