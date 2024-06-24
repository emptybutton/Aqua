from datetime import date
from typing import Optional
from uuid import UUID

from src.aqua.presentation.facade import controllers as aqua
from src.auth.presentation.facade import controllers as auth
from src.entrypoint.application.ports import gateways
from src.shared.infrastructure.adapters.uows import DBUoW


class AquaGateway(gateways.aqua.Gateway[DBUoW[object]]):
    async def register_user(  # noqa: PLR0913
        self,
        auth_user_id: UUID,
        water_balance_milliliters: Optional[int],
        glass_milliliters: Optional[int],
        weight_kilograms: Optional[int],
        *,
        uow: DBUoW[object],
    ) -> gateways.aqua.RegistrationDTO:
        result = await aqua.registration.register_user(
            auth_user_id,
            water_balance_milliliters,
            glass_milliliters,
            weight_kilograms,
            session=uow.session,
        )

        return gateways.aqua.RegistrationDTO(
            water_balance_milliliters=result.water_balance_milliliters,
            glass_milliliters=result.glass_milliliters,
        )

    async def write_water(
        self,
        auth_user_id: UUID,
        milliliters: Optional[int],
        *,
        uow: DBUoW[object],
    ) -> gateways.aqua.WaterWritingDTO:
        result = await aqua.writing.write_water(
            auth_user_id,
            milliliters,
            session=uow.session,
        )

        return gateways.aqua.WaterWritingDTO(
            record_id=result.record_id,
            drunk_water_milliliters=result.drunk_water_milliliters,
        )

    async def read_day_records(
        self,
        user_id: UUID,
        date_: date,
        *,
        uow: DBUoW[object],
    ) -> gateways.aqua.DayRecordReadingDTO:
        result = await aqua.day_record_reading.read_day_records(
            user_id,
            date_,
            session=uow.session,
        )

        records = tuple(map(self.__record_dto_of, result.records))
        return gateways.aqua.DayRecordReadingDTO(records=records)

    async def read_day(
        self,
        user_id: UUID,
        date_: date,
        *,
        uow: DBUoW[object],
    ) -> gateways.aqua.DayReadingDTO:
        result = await aqua.day_reading.read_day(
            user_id,
            date_,
            session=uow.session,
        )

        return gateways.aqua.DayReadingDTO(
            target_water_balance=result.target_water_balance,
            real_water_balance=result.real_water_balance,
            result_code=result.result_code,
        )

    async def read_user_data(
        self,
        user_id: UUID,
        *,
        uow: DBUoW[object],
    ) -> Optional[gateways.aqua.UserDataReadingDTO]:
        result = await aqua.user_data_reading.read_user_data(
            user_id,
            session=uow.session,
        )

        if result is None:
            return None

        return gateways.aqua.UserDataReadingDTO(
            user_id=result.user_id,
            glass_milliliters=result.glass_milliliters,
            weight_kilograms=result.weight_kilograms,
            target_water_balance_milliliters=(
                result.target_water_balance_milliliters
            ),
        )

    def __record_dto_of(
        self,
        dto: aqua.day_record_reading.RecordDTO
    ) -> gateways.aqua.RecordDTO:
        return gateways.aqua.RecordDTO(
            id=dto.id,
            drunk_water=dto.drunk_water,
            recording_time=dto.recording_time,
        )


class AuthGateway(gateways.auth.Gateway[DBUoW[object]]):
    async def register_user(
        self,
        name: str,
        password: str,
        *,
        uow: DBUoW[object],
    ) -> gateways.auth.UserRegistrationDTO:
        result = await auth.registration.register_user(
            name,
            password,
            session=uow.session,
        )

        return gateways.auth.UserRegistrationDTO(
            user_id=result.user_id,
            username=result.username,
            access_token=result.serialized_access_token,
            refresh_token_expiration_date=result.refresh_token_expiration_date,
            refresh_token=result.refresh_token_text,
        )

    def authenticate_user(
        self,
        jwt: str,
    ) -> gateways.auth.UserAuthenticationDTO:
        result = auth.authentication.authenticate_user(jwt)

        return gateways.auth.UserAuthenticationDTO(auth_user_id=result.user_id)

    async def read_user_data(
        self,
        user_id: UUID,
        *,
        uow: DBUoW[object],
    ) -> Optional[gateways.auth.UserDataReadingDTO]:
        result = await auth.user_data_reading.read_user_data(
            user_id,
            session=uow.session,
        )

        if result is None:
            return None

        return gateways.auth.UserDataReadingDTO(username=result.username)
