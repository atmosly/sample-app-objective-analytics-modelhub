"""
Copyright 2022 Objectiv B.V.
"""
import pandas as pd
import pytest

from bach import DataFrame

from modelhub.pipelines.extracted_contexts import get_extracted_context_pipeline
from tests_modelhub.data_and_utils.data_parsers import get_extracted_contexts_data_from_parsed_objectiv_data
from tests_modelhub.data_and_utils.utils import create_engine_from_db_params, \
    DBParams


@pytest.fixture()
def patch_extracted_contexts_validations(monkeypatch, db_params):
    if db_params.format == DBParams.Format.OBJECTIV:
        patch_db_dtypes = {
            'value': 'json'
        }
    elif db_params.format == DBParams.Format.SNOWPLOW:
        patch_db_dtypes = {
            'contexts': 'string'
        }
    elif db_params.format == DBParams.Format.FLATTENED_SNOWPLOW:
        patch_db_dtypes = {
            'contexts_io_objectiv_location_stack_1_0_0': [{'location_stack': 'string'}]
        }

    monkeypatch.setattr(
        'modelhub.pipelines.extracted_contexts.bach.from_database.get_dtypes_from_table',
        lambda *args, **kwargs: patch_db_dtypes
    )

    monkeypatch.setattr(
        'modelhub.pipelines.extracted_contexts.BaseExtractedContextsPipeline._validate_data_dtypes',
        lambda *args, **kwargs: None,
    )


def test_get_base_dtypes(db_params, patch_extracted_contexts_validations) -> None:
    engine = create_engine_from_db_params(db_params)
    pipeline = get_extracted_context_pipeline(engine, db_params.table_name, global_contexts=[])
    result = pipeline._base_dtypes

    if db_params.format == DBParams.Format.OBJECTIV:
        expected = {
            'value': 'json',
            'event_id': 'uuid',
            'day': 'date',
            'moment': 'timestamp',
            'cookie_id': 'uuid'
        }
        assert expected == result
        return

    if db_params.format in (DBParams.Format.FLATTENED_SNOWPLOW, DBParams.Format.SNOWPLOW):
        if db_params.format == DBParams.Format.FLATTENED_SNOWPLOW:
            extra_dtypes = {
                'contexts_io_objectiv_location_stack_1_0_0': [{'location_stack': 'string'}]
            }
        else:
            extra_dtypes = {'contexts': 'string'}

        expected = {
            'collector_tstamp': 'timestamp',
            **extra_dtypes,
            'domain_sessionid': 'string',
            'event_id': 'string',
            'network_userid': 'string',
            'se_action': 'string',
            'se_category': 'string',
            'true_tstamp': 'timestamp',
        }
    else:
        raise Exception()

    assert expected == result


def test_convert_dtypes(db_params, patch_extracted_contexts_validations) -> None:
    engine = create_engine_from_db_params(db_params)

    pipeline = get_extracted_context_pipeline(engine, db_params.table_name, global_contexts=[])

    event = get_extracted_contexts_data_from_parsed_objectiv_data(db_params.format)[0]
    pdf = pd.DataFrame(
        [
            {
                'event_id': str(event['event_id']),
                'day': str(event['day']),
                'moment': str(event['moment']),
                'user_id': str(event['user_id']),
            }
        ]
    )
    df = DataFrame.from_pandas(
        engine=engine,
        df=pdf,
        convert_objects=True,
    ).reset_index(drop=True)

    result = pipeline._convert_dtypes(df)
    assert result['event_id'].dtype == 'uuid'
    assert result['day'].dtype == 'date'
    assert result['moment'].dtype == 'timestamp'
    assert result['user_id'].dtype == 'uuid'


def test_get_base_dtypes(db_params, monkeypatch) -> None:
    monkeypatch.setattr(
        'modelhub.pipelines.extracted_contexts.bach.from_database.get_dtypes_from_table',
        lambda *args, **kwargs: {}   # empty result
    )

    engine = create_engine_from_db_params(db_params)
    with pytest.raises(Exception, match='Table is missing'):
        pipeline = get_extracted_context_pipeline(engine, db_params.table_name, global_contexts=[])
