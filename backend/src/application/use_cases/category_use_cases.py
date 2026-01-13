from typing import Optional
from uuid import UUID

from src.application.dtos import CategoryCreateDTO, CategoryResponseDTO, CategoryUpdateDTO
from src.domain.entities import Category
from src.domain.repositories import CategoryRepository


class CreateCategoryUseCase:
    """Caso de uso para criação de categoria."""

    def __init__(self, category_repository: CategoryRepository):
        self._category_repository = category_repository

    async def execute(self, user_id: UUID, dto: CategoryCreateDTO) -> CategoryResponseDTO:
        category = Category(
            name=dto.name,
            color=dto.color,
            icon=dto.icon,
            user_id=user_id,
        )

        created_category = await self._category_repository.create(category)
        return CategoryResponseDTO.model_validate(created_category)


class GetCategoriesUseCase:
    """Caso de uso para listar categorias."""

    def __init__(self, category_repository: CategoryRepository):
        self._category_repository = category_repository

    async def execute(self, user_id: UUID) -> list[CategoryResponseDTO]:
        categories = await self._category_repository.get_all_by_user(user_id)
        return [CategoryResponseDTO.model_validate(c) for c in categories]


class UpdateCategoryUseCase:
    """Caso de uso para atualizar categoria."""

    def __init__(self, category_repository: CategoryRepository):
        self._category_repository = category_repository

    async def execute(
        self, category_id: UUID, user_id: UUID, dto: CategoryUpdateDTO
    ) -> Optional[CategoryResponseDTO]:
        category = await self._category_repository.get_by_id(category_id)

        if not category or category.user_id != user_id:
            return None

        category.update(name=dto.name, color=dto.color, icon=dto.icon)
        updated_category = await self._category_repository.update(category)
        return CategoryResponseDTO.model_validate(updated_category)


class DeleteCategoryUseCase:
    """Caso de uso para deletar categoria."""

    def __init__(self, category_repository: CategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_id: UUID, user_id: UUID) -> bool:
        category = await self._category_repository.get_by_id(category_id)

        if not category or category.user_id != user_id:
            return False

        return await self._category_repository.delete(category_id)
