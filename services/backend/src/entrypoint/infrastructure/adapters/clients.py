from datetime import datetime, date
from typing import Literal
from uuid import UUID

from aqua.presentation.di import facade as aqua
from auth.presentation.di import facade as auth
from entrypoint.application.ports import clients
from shared.infrastructure.adapters.transactions import DBTransaction


class AquaFacade(clients.aqua.Aqua[DBTransaction]):
    def __init__(self) -> None:
        self.__errors: list[Exception] = list()

    @property
    def errors(self) -> tuple[Exception, ...]:
        return tuple(self.__errors)

    async def register_user(
        self,
        auth_user_id: UUID,
        water_balance_milliliters: int | None,
        glass_milliliters: int | None,
        weight_kilograms: int | None,
        *,
        transaction: DBTransaction,
    ) -> (
        clients.aqua.RegisterUserOutput
        | Literal["aqua_is_not_working"]
        | Literal["incorrect_water_amount"]
        | Literal["incorrect_weight_amount"]
        | Literal["no_weight_for_water_balance"]
        | Literal["extreme_weight_for_water_balance"]
    ):
        try:
            result = await aqua.register_user.perform(
                auth_user_id,
                water_balance_milliliters,
                glass_milliliters,
                weight_kilograms,
                session=transaction.session,
            )
        except aqua.register_user.IncorrectWaterAmountError:
            return "incorrect_water_amount"
        except aqua.register_user.IncorrectWeightAmountError:
            return "incorrect_weight_amount"
        except aqua.register_user.NoWeightForWaterBalanceError:
            return "no_weight_for_water_balance"
        except aqua.register_user.ExtremeWeightForWaterBalanceError:
            return "extreme_weight_for_water_balance"
        except Exception as error:
            self.__errors.append(error)
            return "aqua_is_not_working"

        return clients.aqua.RegisterUserOutput(
            water_balance_milliliters=result.water_balance_milliliters,
            glass_milliliters=result.glass_milliliters,
        )

    async def write_water(
        self,
        auth_user_id: UUID,
        milliliters: int | None,
        *,
        transaction: DBTransaction,
    ) -> (
        clients.aqua.WriteWaterOutput
        | Literal["aqua_is_not_working"]
        | Literal["no_user"]
        | Literal["incorrect_water_amount"]
    ):
        try:
            result = await aqua.write_water.perform(
                auth_user_id,
                milliliters,
                session=transaction.session,
            )
        except aqua.write_water.NoUserError:
            return "no_user"
        except aqua.write_water.IncorrectWaterAmountError:
            return "incorrect_water_amount"
        except Exception as error:
            self.__errors.append(error)
            return "aqua_is_not_working"

        return clients.aqua.WriteWaterOutput(
            record_id=result.record_id,
            drunk_water_milliliters=result.drunk_water_milliliters,
        )

    async def read_day_records(
        self,
        user_id: UUID,
        date_: date,
        *,
        transaction: DBTransaction,
    ) -> (
        clients.aqua.ReadDayRecordsOutput
        | Literal["aqua_is_not_working"]
        | Literal["no_user"]
    ):
        try:
            result = await aqua.read_day_records.perform(
                user_id,
                date_,
                session=transaction.session,
            )
        except aqua.read_day_records.NoUserError:
            return "no_user"
        except Exception as error:
            self.__errors.append(error)
            return "aqua_is_not_working"

        records = tuple(map(self.__record_data_of, result.records))
        return clients.aqua.ReadDayRecordsOutput(records=records)

    async def read_day(
        self,
        user_id: UUID,
        date_: date,
        *,
        transaction: DBTransaction,
    ) -> (
        clients.aqua.ReadDayOutput
        | Literal["aqua_is_not_working"]
        | Literal["no_user"]
    ):
        try:
            result = await aqua.read_day.perform(
                user_id,
                date_,
                session=transaction.session,
            )
        except aqua.read_day.NoUserError:
            return "no_user"
        except Exception as error:
            self.__errors.append(error)
            return "aqua_is_not_working"

        return clients.aqua.ReadDayOutput(
            target_water_balance=result.target_water_balance,
            real_water_balance=result.real_water_balance,
            result_code=result.result_code,
        )

    async def read_user(
        self,
        user_id: UUID,
        *,
        transaction: DBTransaction,
    ) -> clients.aqua.ReadUserOutput | Literal["aqua_is_not_working"] | None:
        try:
            result = await aqua.read_user.perform(
                user_id,
                session=transaction.session,
            )
        except Exception as error:
            self.__errors.append(error)
            return "aqua_is_not_working"

        if result is None:
            return None

        return clients.aqua.ReadUserOutput(
            user_id=result.user_id,
            glass_milliliters=result.glass_milliliters,
            weight_kilograms=result.weight_kilograms,
            target_water_balance_milliliters=(
                result.target_water_balance_milliliters
            ),
        )

    def __record_data_of(
        self,
        facade_data: aqua.read_day_records.RecordData
    ) -> clients.aqua.ReadDayRecordsOutput.RecordData:
        return clients.aqua.ReadDayRecordsOutput.RecordData(
            id=facade_data.id,
            drunk_water=facade_data.drunk_water,
            recording_time=facade_data.recording_time,
        )


class AuthFacade(clients.auth.Auth[DBTransaction]):
    def __init__(self) -> None:
        self.__errors: list[Exception] = list()

    @property
    def errors(self) -> tuple[Exception, ...]:
        return tuple(self.__errors)

    async def register_user(
        self,
        name: str,
        password: str,
        *,
        transaction: DBTransaction,
    ) -> (
        clients.auth.RegisterUserOutput
        | Literal["auth_is_not_working"]
        | Literal["user_is_already_registered"]
        | Literal["empty_username"]
        | Literal["week_password"]
    ):
        try:
            result = await auth.register_user.perform(
                name,
                password,
                session=transaction.session,
            )
        except auth.register_user.UserIsAlreadyRegisteredError:
            return "user_is_already_registered"
        except auth.register_user.EmptyUsernameError:
            return "empty_username"
        except auth.register_user.WeekPasswordError:
            return "week_password"

        return clients.auth.RegisterUserOutput(
            user_id=result.user_id,
            username=result.username,
            access_token=result.serialized_access_token,
            refresh_token_expiration_date=result.refresh_token_expiration_date,
            refresh_token=result.refresh_token_text,
        )

    async def authenticate_user(
        self,
        jwt: str,
    ) -> (
        clients.auth.AuthenticateUserOutput
        | Literal["auth_is_not_working"]
        | Literal["invalid_jwt"]
        | Literal["expired_access_token"]
    ):
        try:
            result = await auth.authenticate_user.perform(jwt)
        except auth.authenticate_user.InvalidJWTError:
            return "invalid_jwt"
        except auth.authenticate_user.ExpiredAccessTokenError:
            return "expired_access_token"
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        return clients.auth.AuthenticateUserOutput(user_id=result.user_id)

    async def authorize_user(
        self,
        name: str,
        password: str,
        *,
        transaction: DBTransaction,
    ) -> (
        clients.auth.AuthorizeUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["incorrect_password"]
    ):
        try:
            result = await auth.authorize_user.perform(
                name,
                password,
                session=transaction.session,
            )
        except auth.authorize_user.NoUserError:
            return "no_user"
        except auth.authorize_user.IncorrectPasswordError:
            return "incorrect_password"
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        return clients.auth.AuthorizeUserOutput(
            user_id=result.user_id,
            username=result.username,
            refresh_token=result.refresh_token,
            refresh_token_expiration_date=result.refresh_token_expiration_date,
            jwt=result.jwt,
        )

    async def read_user(
        self,
        user_id: UUID,
        *,
        transaction: DBTransaction,
    ) -> clients.auth.ReadUserOutput | Literal["auth_is_not_working"] | None:
        try:
            session = transaction.session
            result = await auth.read_user.perform(user_id, session=session)
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        if result is None:
            return None

        return clients.auth.ReadUserOutput(username=result.username)

    async def refresh_token(
        self,
        jwt: str,
        refresh_token: str,
        refresh_token_expiration_date: datetime,
        *,
        transaction: DBTransaction,  # noqa: ARG002
    ) -> (
        clients.auth.RefreshTokenOutput
        | Literal["auth_is_not_working"]
        | Literal["invalid_jwt"]
        | Literal["not_utc_refresh_token_expiration_date"]
        | Literal["expired_refresh_token"]
    ):
        try:
            result = await auth.refresh_token.perform(
                jwt,
                refresh_token,
                refresh_token_expiration_date,
            )
        except auth.refresh_token.InvalidJWTError:
            return "invalid_jwt"
        except auth.refresh_token.NotUTCRefreshTokenExpirationDateError:
            return "not_utc_refresh_token_expiration_date"
        except auth.refresh_token.ExpiredRefreshTokenError:
            return "expired_refresh_token"
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        return clients.auth.RefreshTokenOutput(jwt=result.jwt)