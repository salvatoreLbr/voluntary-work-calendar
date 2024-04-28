from pytest import raises

from voluntary_work_calendar.auth.authorization import create_new_user
from voluntary_work_calendar.db.crud import get_table, delete_record
from voluntary_work_calendar.db.main import get_db
from voluntary_work_calendar.db.models import Users


def test_create_new_user():
    #: Create new user
    create_new_user(
        db=get_db(),
        username="lala",
        password="Hello123?",
    )
    users_df = get_table(
        db_session=get_db(),
        model=Users
    )
    assert "lala" in users_df.username.unique(), "!!! Error in creating new users !!!"

    #: Delete test user
    delete_record(
        db_session=get_db(),
        model=Users,
        filter={"username": "=='lala'"}
    )

    #: Raise exception
    with raises(Exception):
        create_new_user(
            db=get_db(),
            username="lala",
            password="Hello",
        )
