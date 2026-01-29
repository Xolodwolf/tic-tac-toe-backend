from flask import Blueprint, request, jsonify
from domain.service.user_service import UserService
from web.mapper.auth_mapper import AuthMapper
from web.module.user_authenticator import UserAuthenticator


class UserController:
    def __init__(self, user_service: UserService, authenticator: UserAuthenticator):
        self.user_service = user_service
        self.authenticator = authenticator
        self.auth_mapper = AuthMapper()
        self.blueprint = Blueprint("user", __name__, url_prefix="/user")
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule(
            "/<user_id>", "get_user_info", self.get_user_info, methods=["GET"]
        )

    @property
    def _require_auth(self):
        return self.authenticator.require_auth

    def get_user_info(self, user_id: str):
        return self._require_auth(self._get_user_info_impl)(user_id)

    def _get_user_info_impl(self, user_id: str):
        try:
            from uuid import UUID

            try:
                uuid_obj = UUID(user_id)
            except ValueError:
                return jsonify({"error": "Invalid user_id format"}), 400

            user = self.user_service.find_by_id(uuid_obj)

            if not user:
                return jsonify({"error": "User not found"}), 404

            user_info_dto = self.auth_mapper.to_user_info_dto(user)

            return (
                jsonify(
                    {"user_id": user_info_dto.user_id, "login": user_info_dto.login}
                ),
                200,
            )

        except Exception as e:
            return jsonify({"error": f"Error: {str(e)}"}), 500
