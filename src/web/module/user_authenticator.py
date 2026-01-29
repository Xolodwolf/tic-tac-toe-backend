from functools import wraps
from flask import request, jsonify
from domain.service.auth_service import AuthService


class UserAuthenticator:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def require_auth(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return (
                    jsonify(
                        {
                            "error": "Authorization required",
                            "message": "Please provide Authorization header",
                        }
                    ),
                    401,
                )

            if not auth_header.startswith("Bearer "):
                return (
                    jsonify(
                        {
                            "error": "Invalid authorization format",
                            "message": "Authorization header must be in format: Bearer <token>",
                        }
                    ),
                    401,
                )

            token = auth_header[7:]  # После "Bearer "

            if not token:
                return (
                    jsonify(
                        {
                            "error": "Token missing",
                            "message": "Authorization token is missing",
                        }
                    ),
                    401,
                )

            user_id = self.auth_service.authenticate_by_token(token)

            if not user_id:
                return (
                    jsonify(
                        {"error": "Unauthorized", "message": "Invalid or expired token"}
                    ),
                    401,
                )

            request.user_id = user_id
            return f(*args, **kwargs)

        return decorated_function
