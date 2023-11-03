"""
Copyright 2022 Objectiv B.V.
"""
import datetime
import glob
import os
import re
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, validator
from pydantic.fields import Field

from checklock_holmes.utils.constants import NOTEBOOK_EXTENSION
from checklock_holmes.utils.helpers import create_dir_if_not_exists
from checklock_holmes.utils.supported_db_engines import SupportedDBEngine


class CellError(BaseModel):
    number: int
    exc: str


class CellTiming(BaseModel):
    number: int
    time: float


class NoteBookCheckSettings(BaseModel):
    engines_to_check: List[SupportedDBEngine]
    notebooks_to_check: List[str]
    github_issues_dir: str
    compared_outputs_dir: str
    dump_nb_scripts_dir: Optional[str] = None
    display_cell_timing: bool = False
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    compare_notebook_outputs: bool = False
    update_history: bool = False

    @validator('engines_to_check')
    def _process_engines_to_check(cls, engines_to_check: List[str]) -> List[SupportedDBEngine]:
        """
        Verifies if engines are supported, parses string values to SupportedEngine instance
        """
        return SupportedDBEngine.get_supported_engines(engines_to_check)

    @validator('notebooks_to_check')
    def _process_notebooks_to_check(cls, nb_to_check: List[str]) -> List[str]:
        """
        Verifies notebooks extensions, will retrieve all notebooks if filepath suggests.
        """
        processed_nb_to_check = []
        for nb_file in nb_to_check:
            if NOTEBOOK_EXTENSION not in nb_file:
                raise ValueError(f'{nb_file} must be .{NOTEBOOK_EXTENSION} extension.')

            if nb_file.endswith(f'*.{NOTEBOOK_EXTENSION}'):
                processed_nb_to_check.extend(glob.glob(nb_file))
            else:
                processed_nb_to_check.append(nb_file)

        return processed_nb_to_check

    @validator('github_issues_dir')
    def _check_gh_dir(cls, dir: str) -> str:
        """
        Creates issue directory if provided dir does not exist
        """
        create_dir_if_not_exists(dir)
        return dir

    @validator('compared_outputs_dir')
    def _check_cout_dir(cls, dir: str) -> str:
        """
        Creates issue directory if provided dir does not exist
        """
        create_dir_if_not_exists(dir)
        return dir

    @validator('dump_nb_scripts_dir')
    def _check_nb_scripts_dir(cls, dir: str) -> str:
        """
        Creates scripts directory if provided dir does not exist
        """
        create_dir_if_not_exists(dir)
        return dir


class NoteBookMetadata(BaseModel):
    path: str
    name: str = ''
    check_id: UUID = Field(default_factory=uuid4)
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None

    @validator('name', always=True)
    def _process_name(cls, val: Optional[str], values: Dict[str, str]) -> str:
        """
        Extracts notebook name from notebook filepath.
        """
        path = values['path']
        match = re.compile(rf'(.*/)?(?P<nb_name>.+)(\.{NOTEBOOK_EXTENSION})').match(path)
        if not match:
            raise Exception(f'Cannot get notebook name from {path} path.')
        return match.group('nb_name')


class NoteBookCheck(BaseModel):
    metadata: NoteBookMetadata
    engine: str
    completed: bool = False
    skipped: bool = False
    error: Optional[CellError] = None
    failing_block: Optional[str] = None
    elapsed_time: Optional[float] = None
    elapsed_time_per_cell: Optional[List[CellTiming]] = None
    update_history: bool = False
