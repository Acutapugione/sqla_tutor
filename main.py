# %%
from sqlalchemy import (
    create_engine,
    select,
)
from sqlalchemy.orm import (
    sessionmaker, 
    DeclarativeBase,
    Mapped,
    mapped_column
)


# %%
engine = create_engine("sqlite:///my_db.db", echo=True) # для бази даних в ОЗУ "sqlite://"
Session = sessionmaker(bind=engine)

# %%
class Base(DeclarativeBase):
    ...


# %%
from datetime import date


class Student(Base):
    __tablename__  = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    second_name: Mapped[str]
    dob: Mapped[date]

# %%
Base.metadata.drop_all(bind=engine)


# %%
Base.metadata.create_all(bind=engine)

# %%
from datetime import date, timedelta
aider = Student(
    first_name="Айдер",
    second_name="Ісматов",
    dob=date(2009, 4, 29, ),
)


students = [
    Student(
        first_name=f"first_name{i}",
        second_name=f"second_name{i}",
        dob=date(2000, 1, 1, ) + timedelta(days=i),
    )

    for i in range(10**2)
]


# %%
# Приклади додавання великого обсягу даних в таблицю(Необхідне розкоментувати)
with Session.begin() as session:
    # №1
    session.bulk_save_objects(students) # Швидке зберігання в таблицю BULK INSERT 
    # №2
    session.add_all(students) # Повільне зберігання колекції об'єктів в таблицю INSERT MANY
    # №3
    for student in students: # !!! Не рекомендується !!! Жахливий вибір, для тих хто бажає довго чекати 
        session.add(student)
    



