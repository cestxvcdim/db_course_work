import json
import requests
from typing import List, Dict, Any, Optional


class VacancyFormatter:
    @staticmethod
    def format_vacancy(vacancy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formats a single vacancy.

        Args:
            vacancy: The raw vacancy data.

        Returns:
            The formatted vacancy data.
        """
        return {
            'name': vacancy.get('name', 'Не указано'),
            'salary': vacancy.get('salary', 'Не указано'),
            'url': vacancy.get('alternate_url', 'Не указано'),
            'company_name': vacancy.get('employer', {}).get('name', 'Не указано')
        }

    @staticmethod
    def format_data(vacancies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Formats a list of vacancies and groups them by company.

        Args:
            vacancies: The raw vacancies data.

        Returns:
            The formatted data grouped by company.
        """
        company_dict: Dict[str, Dict[str, Any]] = {}

        for vacancy in vacancies:
            salary = vacancy.get('salary')
            if salary and salary.get('currency') == 'RUR':
                formatted_vacancy = VacancyFormatter.format_vacancy(vacancy)
                company_name = formatted_vacancy['company_name']

                if company_name not in company_dict:
                    company_dict[company_name] = {
                        'company_name': company_name,
                        'vacancies': []
                    }
                company_dict[company_name]['vacancies'].append(formatted_vacancy)

        return list(company_dict.values())


class HHApi:
    @staticmethod
    def api_get(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sends a GET request to the specified endpoint with optional parameters.

        Args:
            endpoint: The API endpoint to send the GET request to.
            params: The query parameters for the GET request.

        Returns:
            The JSON response from the API.
        """
        url = f'https://api.hh.ru/{endpoint}'
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_companies_and_vacancies(cls, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieves companies and their vacancies from the API.

        Args:
            params: The query parameters for the request.

        Returns:
            The list of companies and their vacancies.
        """
        endpoint = 'vacancies'
        data = cls.api_get(endpoint, params)
        return VacancyFormatter.format_data(data['items'])


if __name__ == "__main__":
    hh_api = HHApi()
    companies = hh_api.get_companies_and_vacancies({'per_page': 100})

    with open('../data/companies.json', 'w', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False, indent=4)
