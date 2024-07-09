from typing import List, Tuple, Optional

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from models import Base, Company, Vacancy


class DBManager:
    def __init__(self, db_url: str):
        """
        Initializes the DBManager with the given database URL.

        Args:
            db_url: The database URL.
        """
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        session_local = sessionmaker(bind=self.engine)
        self.session: Session = session_local()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Retrieves the count of vacancies for each company.

        Returns:
            A list of tuples containing company names and their respective vacancies count.
        """
        result = self.session.query(
            Company.name,
            func.count(Vacancy.id).label('vacancies_count')
        ).join(Vacancy, isouter=True).group_by(Company.id).order_by(func.count(Vacancy.id).desc()).all()
        return result

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Retrieves all vacancies with their details.

        Returns:
            A list of tuples containing company name, job title,
            salary range, and URL.
        """
        result = self.session.query(
            Company.name.label('company_name'),
            Vacancy.name.label('job_title'),
            Vacancy.salary_from,
            Vacancy.salary_to,
            Vacancy.url
        ).join(Company).all()
        return result

    def get_avg_salary(self) -> Optional[float]:
        """
        Calculates the average salary of all vacancies.

        Returns:
            The average salary or None if no salaries are available.
        """
        result = self.session.query(
            func.avg((Vacancy.salary_from + Vacancy.salary_to) / 2)
        ).filter(Vacancy.salary_from.isnot(None), Vacancy.salary_to.isnot(None)).scalar()
        return result

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Retrieves vacancies with a higher salary than the average.

        Returns:
            A list of tuples containing company name, job title,
            salary range, and URL of vacancies with higher than average salary.
        """
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []

        result = self.session.query(
            Company.name.label('company_name'),
            Vacancy.name.label('job_title'),
            Vacancy.salary_from,
            Vacancy.salary_to,
            Vacancy.url
        ).join(Company).filter(((Vacancy.salary_from + Vacancy.salary_to) / 2) > avg_salary).all()
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Retrieves vacancies that contain a specific keyword in the job title.

        Args:
            keyword: The keyword to search for in the job titles.

        Returns:
            A list of tuples containing company name, job title,
            salary range, and URL of vacancies containing the keyword.
        """
        result = self.session.query(
            Company.name.label('company_name'),
            Vacancy.name.label('job_title'),
            Vacancy.salary_from,
            Vacancy.salary_to,
            Vacancy.url
        ).join(Company).filter(
            Vacancy.name.ilike(f'%{keyword}%')
        ).all()
        return result

    def close_connection(self) -> None:
        self.session.close()


# Пример использования класса
if __name__ == "__main__":
    db_manager = DBManager('postgresql://postgres:postgres@localhost/postgres')

    print("Companies and vacancies count:")
    print(db_manager.get_companies_and_vacancies_count())

    print("\nAll vacancies:")
    print(db_manager.get_all_vacancies())

    print("\nAverage salary:")
    print(db_manager.get_avg_salary())

    print("\nVacancies with higher salary than average:")
    print(db_manager.get_vacancies_with_higher_salary())

    print("\nVacancies with keyword 'программист':")
    print(db_manager.get_vacancies_with_keyword('программист'))

    db_manager.close_connection()
