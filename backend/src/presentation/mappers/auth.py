from dataclasses import dataclass
from typing import final

from backend.src.presentation.schemas.responses import (
    TokenResponseSchema
)


@final
@dataclass(frozen=True, slots=True)
class AuthPresentationMapper:
    @classmethod
    def tokens_to_response(cls, tokens: dict[str, bool|str]) -> TokenResponseSchema:
        """Преобразуйте Application DTO в API Response model."""
        return TokenResponseSchema(
            ok=tokens["ok"],
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
        )