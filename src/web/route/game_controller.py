from flask import Blueprint, request, jsonify
from uuid import UUID
from domain.service.game_service_interface import GameServiceInterface
from domain.model.game_type import GameType
from web.mapper.game_dto_mapper import GameDtoMapper
from web.mapper.leaderboard_mapper import LeaderboardMapper
from web.module.user_authenticator import UserAuthenticator


class GameController:
    def __init__(
        self, game_service: GameServiceInterface, authenticator: UserAuthenticator
    ):
        self.game_service = game_service
        self.authenticator = authenticator
        self.mapper = GameDtoMapper()
        self.leaderboard_mapper = LeaderboardMapper()
        self.blueprint = Blueprint("game", __name__, url_prefix="/game")
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule(
            "/create", "create_game", self.create_game, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/available",
            "get_available_games",
            self.get_available_games,
            methods=["GET"],
        )
        self.blueprint.add_url_rule(
            "/<game_id>/join", "join_game", self.join_game, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/<game_id>/move", "make_move", self.make_move, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/<game_id>", "get_game", self.get_game, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/history", "get_game_history", self.get_game_history, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/leaderboard",
            "get_leaderboard",
            self.get_leaderboard,
            methods=["GET"],
        )

    def create_game(self):
        return self.authenticator.require_auth(self._create_game_impl)()

    def _create_game_impl(self):
        try:
            player_id = request.user_id
            data = request.get_json()

            if not data or "game_type" not in data:
                return jsonify({"error": "game_type is required"}), 400

            game_type_str = data["game_type"].lower()
            if game_type_str not in ["pvp", "pvc"]:
                return jsonify({"error": 'game_type must be "pvp" or "pvc"'}), 400

            game_type = GameType.PVP if game_type_str == "pvp" else GameType.PVC

            game = self.game_service.create_game(player_id, game_type)

            game_dto = self.mapper.to_game_info_dto(game)

            return (
                jsonify(
                    {
                        "game_id": game_dto.game_id,
                        "board": game_dto.board,
                        "game_type": game_dto.game_type,
                        "game_state": game_dto.game_state,
                        "player1_id": game_dto.player1_id,
                        "player2_id": game_dto.player2_id,
                        "player1_symbol": game_dto.player1_symbol,
                        "player2_symbol": game_dto.player2_symbol,
                        "current_player_id": game_dto.current_player_id,
                        "winner_id": game_dto.winner_id,
                    }
                ),
                201,
            )

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_available_games(self):
        return self.authenticator.require_auth(self._get_available_games_impl)()

    def _get_available_games_impl(self):
        try:
            games = self.game_service.get_available_games()
            games_list = self.mapper.to_available_games_list(games)

            return jsonify({"games": games_list}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def join_game(self, game_id: str):
        return self.authenticator.require_auth(self._join_game_impl)(game_id)

    def _join_game_impl(self, game_id: str):
        try:
            player_id = request.user_id

            try:
                game_uuid = UUID(game_id)
            except ValueError:
                return jsonify({"error": "Invalid game_id format"}), 400

            game = self.game_service.join_game(game_uuid, player_id)

            game_dto = self.mapper.to_game_info_dto(game)

            return (
                jsonify(
                    {
                        "game_id": game_dto.game_id,
                        "board": game_dto.board,
                        "game_type": game_dto.game_type,
                        "game_state": game_dto.game_state,
                        "player1_id": game_dto.player1_id,
                        "player2_id": game_dto.player2_id,
                        "player1_symbol": game_dto.player1_symbol,
                        "player2_symbol": game_dto.player2_symbol,
                        "current_player_id": game_dto.current_player_id,
                        "winner_id": game_dto.winner_id,
                    }
                ),
                200,
            )

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def make_move(self, game_id: str):
        return self.authenticator.require_auth(self._make_move_impl)(game_id)

    def _make_move_impl(self, game_id: str):
        try:
            player_id = request.user_id
            data = request.get_json()

            if not data or "board" not in data:
                return jsonify({"error": "board is required"}), 400

            board = data["board"]

            if not isinstance(board, list) or len(board) != 3:
                return jsonify({"error": "board must be a 3x3 array"}), 400

            for row in board:
                if not isinstance(row, list) or len(row) != 3:
                    return jsonify({"error": "board must be a 3x3 array"}), 400

            try:
                game_uuid = UUID(game_id)
            except ValueError:
                return jsonify({"error": "Invalid game_id format"}), 400

            game = self.game_service.make_move(game_uuid, player_id, board)

            game_dto = self.mapper.to_game_info_dto(game)

            return (
                jsonify(
                    {
                        "game_id": game_dto.game_id,
                        "board": game_dto.board,
                        "game_type": game_dto.game_type,
                        "game_state": game_dto.game_state,
                        "player1_id": game_dto.player1_id,
                        "player2_id": game_dto.player2_id,
                        "player1_symbol": game_dto.player1_symbol,
                        "player2_symbol": game_dto.player2_symbol,
                        "current_player_id": game_dto.current_player_id,
                        "winner_id": game_dto.winner_id,
                    }
                ),
                200,
            )

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_game(self, game_id: str):
        return self.authenticator.require_auth(self._get_game_impl)(game_id)

    def _get_game_impl(self, game_id: str):
        try:
            try:
                game_uuid = UUID(game_id)
            except ValueError:
                return jsonify({"error": "Invalid game_id format"}), 400

            game = self.game_service.get_game(game_uuid)

            if not game:
                return jsonify({"error": "Game not found"}), 404

            game_dto = self.mapper.to_game_info_dto(game)

            return (
                jsonify(
                    {
                        "game_id": game_dto.game_id,
                        "board": game_dto.board,
                        "game_type": game_dto.game_type,
                        "game_state": game_dto.game_state,
                        "player1_id": game_dto.player1_id,
                        "player2_id": game_dto.player2_id,
                        "player1_symbol": game_dto.player1_symbol,
                        "player2_symbol": game_dto.player2_symbol,
                        "current_player_id": game_dto.current_player_id,
                        "winner_id": game_dto.winner_id,
                    }
                ),
                200,
            )

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_game_history(self):
        return self.authenticator.require_auth(self._get_game_history_impl)()

    def _get_game_history_impl(self):
        try:
            user_id = request.user_id

            games = self.game_service.get_completed_games_by_user(user_id)
            games_list = self.mapper.to_game_history_list(games)

            return jsonify({"games": games_list}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_leaderboard(self):
        return self.authenticator.require_auth(self._get_leaderboard_impl)()

    def _get_leaderboard_impl(self):
        try:
            limit = request.args.get("limit", default=10, type=int)

            if limit < 1:
                return jsonify({"error": "limit must be greater than 0"}), 400
            if limit > 100:
                return jsonify({"error": "limit must not exceed 100"}), 400

            leaders = self.game_service.get_leaderboard(limit)
            leaders_list = self.leaderboard_mapper.to_dto_list(leaders)

            return jsonify({"leaderboard": leaders_list}), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
