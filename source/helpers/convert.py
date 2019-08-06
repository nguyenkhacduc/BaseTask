def ConvertToDict(row):
    dict = {}

    for column in row.__table__.columns:
        dict[column.name] = getattr(row, column.name)

    return dict