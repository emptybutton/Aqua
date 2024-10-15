from auth.application.ports.repos import Accounts


async def view_account_with_name_exists(
    name_text: str,
    *,
    accounts: Accounts,
) -> bool:
    return await accounts.contains_account_with_name(name_text=name_text)
