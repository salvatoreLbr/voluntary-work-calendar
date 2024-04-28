from voluntary_work_calendar.db.gateway import CSVGateway, DBGateway


def test_csv_gateway():
    gateway = CSVGateway(test=True)

    #: Test insert_new_volunteer
    gateway.insert_new_volunteer(name="Salvatore")

    #: Test insert_presence
    gateway.insert_presence(data="2023-12-31", orario_from="10:00", orario_to="18:00", name="Salvatore")

    #: Test get_calendar
    _ = gateway.get_calendar()

    #: Test get_volunteers_name
    _ = gateway.get_volunteers_name()

    #: Test delete_presence
    gateway.delete_presence(data="2023-12-31", name="Salvatore")

    #: Test delete_volunteer
    gateway.delete_volunteer(name="Salvatore")

    #: Test insert_new_volunteer
    gateway.insert_new_volunteer(name="Salvatore")
    gateway.insert_new_volunteer(name="Paolo")
    gateway.insert_new_volunteer(name="Marco")

    #: Test delete_volunteer
    gateway.delete_volunteer(name="Paolo")

    #: Remove test file
    test_path = gateway.input_path
    for file in test_path.glob("*"):
        file.unlink()
    gateway.input_path.rmdir()
