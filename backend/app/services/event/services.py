from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from models.crud import get_public_valentines, create_valentine
from backend.app.notification.mail import send_valentine
from schemas import (
    AllElementsResponseDTO,
    CreateEventResponseDTO,
    IntEventCreatorId,
    StrEventAddress,
    StrEventDescription,
    StrEventTitle,
)
from backend.app.notification.mail import send_valentine

if TYPE_CHECKING:
    from schemas import CreateEventDTO


class ManagementEvents:
    """
    Модуль (класс) для управления валентинками.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_events(
        self,
        data: "CreateEventDTO",
    ) -> CreateEventResponseDTO:
        """
        Метод для создания.
        """
        event = await create_valentine(
            self.db, data.text, 
            data.recipient_email, 
            data.author_email, 
            data.is_public, 
            data.dispatch_date
        )

        await send_valentine(data.recipient_email, data.text)

        return CreateEventResponseDTO.model_validate(event)

    async def all_events(self) -> list[AllElementsResponseDTO]:
        """
        Метод для вывода всех мероприятий (не оптимизирован для больших данных).

        Args:
            jwt_token (str): Токен пользователя.

        Returns:
           AllElementsResponseDTO (list[BaseModel]): Все мероприятия.

        Raises:
            NoTokenError (HTTPException): Токен отсутствует.
        """
        events = await get_public_valentines(self.db)
        return [AllElementsResponseDTO.model_validate(event) for event in events]
