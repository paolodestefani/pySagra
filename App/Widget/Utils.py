from contextlib import contextmanager
from typing import Generator, Any

# Adjust imports according to your internal architecture
# from App.Core.exceptions import PyAppDBError
# from App.Database.connection import appconn
# from App.Core.translation import _tr
# from App.Ui.widgets import MessageBoxCritical

@contextmanager
def gui_exception_context(parent_widget: Any, operation_title: str) -> Generator[None, None, None]:
    """
    Catches PyAppDBError exceptions, translates PostgreSQL SQLSTATE codes 
    into user-friendly localized messages, and displays a critical dialog.
    """
    try:
        yield
    except PyAppDBError as er:
        # Map standard PostgreSQL SQLSTATE error codes to clear messages
        match er.code:
            case 'CCER':
                msg = _tr("Form", "Row modified before update/delete: "
                                  "unable to commit the transaction because "
                                  "the row was modified before update or delete "
                                  "from another client")
            case '23000':
                msg = _tr("Form", "Integrity constraint violation: "
                                  "unable to commit the transaction because "
                                  "a generic integrity violation occurred")
            case '23502':
                msg = _tr("Form", "Integrity constraint violation: "
                                  "unable to commit the transaction because "
                                  "a not null error occurred")
            case '23503':
                msg = _tr("Form", "Foreign key violation: "
                                  "unable to delete the current record because "
                                  "it is still referenced from another database object")
            case '23505':
                msg = _tr("Form", "Duplicate key value violates unique constraint: "
                                  "Cannot insert the current record because a key value "
                                  "is already present in the database table")
            case _:
                msg = (f"Unrecognized database error code: {er.code}\n"
                       f"For more information click on 'Show Details...'")
        
        # Display the custom PySide6 critical dialog box
        MessageBoxCritical(parent_widget, operation_title, msg, er.message)
        
        # Safe fallback: rollback the shared connection to reset the transaction state
        appconn.rollback()
