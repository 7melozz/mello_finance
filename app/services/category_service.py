from app.exceptions import BadRequestError, NotFoundError
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    @staticmethod
    def list_categories():
        return CategoryRepository.list_categories()

    @staticmethod
    def create_category(name: str):
        if not name.strip():
            raise BadRequestError("name não pode estar vazio")
        return CategoryRepository.create_category(name=name.strip())

    @staticmethod
    def update_category(category_id: int, name: str):
        category = CategoryRepository.get_category(category_id)
        if not category:
            raise NotFoundError("Categoria não encontrada")
        if not name.strip():
            raise BadRequestError("name não pode estar vazio")
        return CategoryRepository.update_category(category_id=category_id, name=name.strip())

    @staticmethod
    def delete_category(category_id: int):
        category = CategoryRepository.get_category(category_id)
        if not category:
            raise NotFoundError("Categoria não encontrada")
        if CategoryRepository.count_category_transactions(category_id):
            raise BadRequestError("Não é possível excluir categoria vinculada a transações")
        CategoryRepository.delete_category(category_id)
