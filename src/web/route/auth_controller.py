from flask import Blueprint, request, jsonify
from domain.service.auth_service import AuthService
from domain.service.user_service import UserService
from web.mapper.auth_mapper import AuthMapper
from web.mapper.jwt_mapper import JwtMapper
from web.model.sign_up_request_dto import SignUpRequestDto
from web.model.sign_up_response_dto import SignUpResponseDto
from web.model.jwt_request_dto import JwtRequestDto
from web.model.refresh_jwt_request_dto import RefreshJwtRequestDto
from web.module.user_authenticator import UserAuthenticator


class AuthController:
    def __init__(
        self,
        auth_service: AuthService,
        user_service: UserService,
        authenticator: UserAuthenticator,
    ):
        self.auth_service = auth_service
        self.user_service = user_service
        self.authenticator = authenticator
        self.auth_mapper = AuthMapper()
        self.jwt_mapper = JwtMapper()
        self.bp = Blueprint("auth", __name__, url_prefix="/auth")
        self._register_routes()

    def _register_routes(self):
        self.bp.add_url_rule("/register", "register", self.register, methods=["POST"])
        self.bp.add_url_rule("/login", "login", self.login, methods=["POST"])
        self.bp.add_url_rule(
            "/refresh-access", "refresh_access", self.refresh_access, methods=["POST"]
        )
        self.bp.add_url_rule("/refresh", "refresh", self.refresh, methods=["POST"])
        self.bp.add_url_rule("/me", "me", self.get_me, methods=["GET"])

    def register(self):
        try:
            data = request.get_json()

            if not data or "login" not in data or "password" not in data:
                return (
                    jsonify(
                        {"success": False, "message": "Login or password are required"}
                    ),
                    400,
                )

            dto = SignUpRequestDto(login=data["login"], password=data["password"])

            sign_up_request = self.auth_mapper.to_sign_up_request(dto)
            success = self.auth_service.register(sign_up_request)

            if success:
                response = SignUpResponseDto(
                    success=True, message="User registered successfully"
                )
                return (
                    jsonify({"success": response.success, "message": response.message}),
                    200,
                )
            else:
                response = SignUpResponseDto(
                    success=False, message="Login already exists"
                )
                return (
                    jsonify({"success": response.success, "message": response.message}),
                    400,
                )

        except Exception as e:
            return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

    def login(self):
        try:
            data = request.get_json()

            if not data or "login" not in data or "password" not in data:
                return jsonify({"error": "Login and password are required"}), 400

            dto = JwtRequestDto(login=data["login"], password=data["password"])

            result = self.auth_service.authenticate(dto)

            if result:
                return jsonify(self.jwt_mapper.jwt_response_to_dict(result)), 200
            else:
                return jsonify({"error": "Invalid credentials"}), 401

        except Exception as e:
            return jsonify({"error": f"Error: {str(e)}"}), 500

    def refresh_access(self):
        try:
            data = request.get_json()

            if not data or "refresh_token" not in data:
                return jsonify({"error": "Refresh token is required"}), 400

            dto = RefreshJwtRequestDto(refresh_token=data["refresh_token"])
            refresh_token = self.jwt_mapper.to_refresh_jwt_request(dto)

            result = self.auth_service.refresh_access_token(refresh_token)

            if result:
                return jsonify(self.jwt_mapper.jwt_response_to_dict(result)), 200
            else:
                return jsonify({"error": "Invalid or expired refresh token"}), 401

        except Exception as e:
            return jsonify({"error": f"Error: {str(e)}"}), 500

    def refresh(self):
        try:
            data = request.get_json()

            if not data or "refresh_token" not in data:
                return jsonify({"error": "Refresh token is required"}), 400

            dto = RefreshJwtRequestDto(refresh_token=data["refresh_token"])
            refresh_token = self.jwt_mapper.to_refresh_jwt_request(dto)

            result = self.auth_service.refresh_refresh_token(refresh_token)

            if result:
                return jsonify(self.jwt_mapper.jwt_response_to_dict(result)), 200
            else:
                return jsonify({"error": "Invalid or expired refresh token"}), 401

        except Exception as e:
            return jsonify({"error": f"Error: {str(e)}"}), 500

    def get_me(self):
        return self.authenticator.require_auth(self._get_me_impl)()

    def _get_me_impl(self):
        try:
            user_id = request.user_id
            user = self.user_service.find_by_id(user_id)

            if user:
                return jsonify({"user_id": str(user.user_id), "login": user.login}), 200
            else:
                return jsonify({"error": "User not found"}), 404

        except Exception as e:
            return jsonify({"error": f"Error: {str(e)}"}), 500
