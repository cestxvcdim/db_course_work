from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    __allow_unmapped__ = True
    pass


class Company(Base):
    """
    Represents a company in the database.

    Attributes:
        id: The primary key of the company.
        name: The unique name of the company.
        vacancies: The list of vacancies associated with the company.
    """
    __tablename__ = 'companies'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, nullable=False)
    vacancies: list['Vacancy'] = relationship('Vacancy', back_populates='company')


class Vacancy(Base):
    """
    Represents a vacancy in the database.

    Attributes:
        id: The primary key of the vacancy.
        name: The name of the vacancy.
        salary_from: The starting salary for the vacancy.
        salary_to: The maximum salary for the vacancy.
        currency: The currency of the salary.
        gross: Indicates whether the salary is gross or net.
        url: The URL of the vacancy posting.
        company_id: The foreign key referencing the company.
        company: The company associated with the vacancy.
    """
    __tablename__ = 'vacancies'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    salary_from: int = Column(Integer)
    salary_to: int = Column(Integer)
    currency: str = Column(String, nullable=False)
    gross: bool = Column(Boolean)
    url: str = Column(String, nullable=False)
    company_id: int = Column(Integer, ForeignKey('companies.id'))
    company: Company = relationship('Company', back_populates='vacancies')
