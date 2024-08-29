from datetime import date
from typing import Literal
from uuid import UUID

from aqua.presentation.di import facade as aqua
from entrypoint.application.ports import clients
from shared.infrastructure.adapters.transactions import DBTransaction


class AquaFacade(clients.aqua.Aqua[DBTransaction]):
    def __init__(self) -> None:
        self.__errors: list[Exception] = list()

    @property
    def errors(self) -> tuple[Exception, ...]:
        return tuple(self.__errors)

    async def close(self) -> None:
        await aqua.close.perform()

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

        target = result.target_water_balance_milliliters

        return clients.aqua.RegisterUserOutput(
            user_id=result.user_id,
            target_water_balance_milliliters=target,
            glass_milliliters=result.glass_milliliters,
            weight_kilograms=result.weight_kilograms,
        )

    async def write_water(
        self,
        user_id: UUID,
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
                user_id, milliliters, session=transaction.session
            )
        except aqua.write_water.NoUserError:
            return "no_user"
        except aqua.write_water.IncorrectWaterAmountError:
            return "incorrect_water_amount"
        except Exception as error:
            self.__errors.append(error)
            return "aqua_is_not_working"

        target = result.target_water_balance_milliliters
        previous_records = tuple(
            map(self.__write_water_record_data_of, result.previous_records)
        )

        return clients.aqua.WriteWaterOutput(
            user_id=result.user_id,
            target_water_balance_milliliters=target,
            water_balance_milliliters=result.water_balance_milliliters,
            result_code=result.result_code,
            real_result_code=result.real_result_code,
            is_result_pinned=result.is_result_pinned,
            date_=result.date_,
            previous_records=previous_records,
            new_record=self.__write_water_record_data_of(result.new_record),
        )

    def __write_water_record_data_of(
        self, data: aqua.write_water.RecordData
    ) -> clients.aqua.WriteWaterOutput.RecordData:
        return clients.aqua.WriteWaterOutput.RecordData(
            record_id=data.record_id,
            drunk_water_milliliters=data.drunk_water_milliliters,
            recording_time=data.recording_time,
        )

    async def read_day(
        self, user_id: UUID, date_: date, *, transaction: DBTransaction
    ) -> (
        clients.aqua.ReadDayOutput
        | Literal["aqua_is_not_working"]
        | Literal["no_user"]
    ):
        try:
            result = await aqua.read_day.perform(
                user_id, date_, session=transaction.session
            )
        except aqua.read_day.NoUserError:
            return "no_user"
        except Exception as error:
            self.__errors.append(error)
            return "aqua_is_not_working"

        target = result.target_water_balance_milliliters
        records = tuple(
            clients.aqua.ReadDayOutput.RecordData(
                record_id=record.record_id,
                drunk_water_milliliters=record.drunk_water_milliliters,
                recording_time=record.recording_time,
            )
            for record in result.records
        )
        return clients.aqua.ReadDayOutput(
            user_id=result.user_id,
            date_=result.date_,
            target_water_balance_milliliters=target,
            water_balance_milliliters=result.water_balance_milliliters,
            result_code=result.result_code,
            real_result_code=result.real_result_code,
            is_result_pinned=result.is_result_pinned,
            records=records,
        )

    async def read_user(
        self, user_id: UUID, *, transaction: DBTransaction
    ) -> (
        clients.aqua.ReadUserOutput
        | Literal["aqua_is_not_working"]
        | Literal["no_user"]
    ):
        try:
            result = await aqua.read_user.perform(
                user_id, session=transaction.session
            )
        except Exception as error:
            self.__errors.append(error)
            return "aqua_is_not_working"

        if result is None:
            return "no_user"

        target = result.target_water_balance_milliliters
        records = tuple(
            clients.aqua.ReadUserOutput.RecordData(
                record_id=record.record_id,
                drunk_water_milliliters=record.drunk_water_milliliters,
                recording_time=record.recording_time,
            )
            for record in result.records
        )
        return clients.aqua.ReadUserOutput(
            user_id=result.user_id,
            glass_milliliters=result.glass_milliliters,
            weight_kilograms=result.weight_kilograms,
            date_=result.date_,
            target_water_balance_milliliters=target,
            water_balance_milliliters=result.water_balance_milliliters,
            result_code=result.result_code,
            real_result_code=result.real_result_code,
            is_result_pinned=result.is_result_pinned,
            records=records,
        )
