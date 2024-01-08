from collections.abc import Sequence
from typing import ClassVar

from litestar import Controller
from litestar import get
from litestar import post
from litestar import put
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.pagination import OffsetPagination
from litestar.repository.filters import LimitOffset

from app.core.providers import provide_limit_offset_pagination
from app.domain.subject.models import Subject as SubjectModel
from app.domain.subject.providers import provide_subjects_repo
from app.domain.subject.repository import SubjectRepository
from app.domain.subject.schema import SubjectCreateDTO
from app.domain.subject.schema import SubjectReadDTO
from app.domain.subject.schema import SubjectUpdateDTO


class SubjectController(Controller):
    path = "/subject/"

    tags: Sequence[str] = ["subject"]

    dependencies: ClassVar[dict[str, Provide]] = {
        "subjects_repo": Provide(provide_subjects_repo),
    }

    @get(
        dependencies={
            "limit_offset": Provide(provide_limit_offset_pagination),
        },
        summary="List all subjects",
    )
    async def get_subjects(
        self,
        subjects_repo: SubjectRepository,
        limit_offset: LimitOffset,
    ) -> OffsetPagination[SubjectModel]:
        """
        List subjects
        """
        results, total = await subjects_repo.list_and_count(limit_offset)
        return OffsetPagination[SubjectModel](
            items=results,
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @get("{subject_id:int}", summary="Get a single subject", raises=[NotFoundException])
    async def get_single_subject(
        self,
        subjects_repo: SubjectRepository,
        subject_id: int,
    ) -> SubjectModel:
        """
        Get single subjects
        """
        obj = await subjects_repo.get_one_or_none(id=subject_id)
        if obj is None:
            raise NotFoundException(detail=f"Subject with ID {subject_id} not found")
        return obj

    @post(dto=SubjectCreateDTO, return_dto=SubjectReadDTO, summary="Create new subject")
    async def create_subject(
        self,
        subjects_repo: SubjectRepository,
        data: SubjectModel,
    ) -> SubjectModel:
        """
        Creates a subject
        """
        obj = await subjects_repo.add(data)
        await subjects_repo.session.commit()
        return obj

    @put(
        "{subject_id:int}",
        dto=SubjectUpdateDTO,
        return_dto=SubjectReadDTO,
        summary="Updates single location",
        raises=[NotFoundException],
    )
    async def update_subject(
        self,
        subjects_repo: SubjectRepository,
        subject_id: int,
        data: SubjectModel,
    ) -> SubjectModel:
        obj = await subjects_repo.get_one_or_none(id=subject_id)
        if obj is None:
            raise NotFoundException(detail=f"Subject with ID {subject_id} not found")
        data.id = obj.id
        await subjects_repo.update(data, ["name"])
        await subjects_repo.session.commit()
        obj = await subjects_repo.get(subject_id)
        return obj
