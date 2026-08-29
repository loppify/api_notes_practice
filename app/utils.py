import re

import asyncpg
from sqlalchemy.exc import IntegrityError


def parse_integrity_error(exc: IntegrityError) -> tuple[str, str]:
    """
    :returns: Tuple[Field or Restriction name, Detailed error message]
    """
    # Отримуємо оригінальну помилку asyncpg
    orig_error = getattr(exc, "orig", None)
    asyncpg_error = getattr(orig_error, "__cause__", orig_error)

    if isinstance(asyncpg_error, asyncpg.exceptions.UniqueViolationError):
        # asyncpg надає detail у форматі: Key (column_name)=(value) already exists.
        detail = asyncpg_error.detail or ""
        match = re.search(r"Key \((.*?)\)=\((.*?)\) already exists", detail)
        if match:
            field_name, value = match.groups()
            return (
                field_name,
                f"Record with '{value}' for field '{field_name}' already existі.",
            )

        # Фолбек на назву обмеження
        constraint = asyncpg_error.constraint_name or "unknown"
        return constraint, f"Constraint's uniqueness violated for '{constraint}'."

    elif isinstance(asyncpg_error, asyncpg.exceptions.ForeignKeyViolationError):
        detail = asyncpg_error.detail or ""
        match = re.search(r"Key \((.*?)\)=\((.*?)\) is not present in table", detail)
        if match:
            field_name, value = match.groups()
            return (
                field_name,
                f"Related record '{field_name}' with value '{value}' is not  present.",
            )

        constraint = asyncpg_error.constraint_name or "unknown"
        return constraint, f"Violated foreign key '{constraint}'."

    elif isinstance(asyncpg_error, asyncpg.exceptions.NotNullViolationError):
        column = asyncpg_error.column_name or "unknown"
        return column, f"Field '{column}' is necessary and can't be empty."

    return "database", "Violated data integrity."
