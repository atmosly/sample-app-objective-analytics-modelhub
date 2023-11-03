import bach
import pytest
from bach import SortColumn
from bach.testing import assert_equals_data

from modelhub import ModelHub


def _add_root_offset_sorting(objectiv_df: bach.DataFrame, asc: bool = True) -> bach.DataFrame:
    if '__root_step_offset' in objectiv_df.base_node.series_names:
        objectiv_df._order_by.append(
            SortColumn(
                expression=bach.expression.Expression.identifier('__root_step_offset'),
                asc=asc,
            )
        )

    return objectiv_df

def test_get_navigation_paths(objectiv_df):
    modelhub = ModelHub()
    funnel = modelhub.get_funnel_discovery()
    objectiv_df = objectiv_df.sort_values(by='moment')

    # this is the order of all nice names when aggregated
    agg_nice_names = (
        objectiv_df['location_stack'].ls.nice_name
        .sort_by_series(by=[objectiv_df['moment']]).to_json_array()
    )
    assert_equals_data(
        agg_nice_names,
        expected_columns=['location_stack'],
        expected_data=[[[
            'Link: cta-docs-taxonomy located at Web Document: #document => Section: main => Section: taxonomy',
            'Link: logo located at Web Document: #document => Section: navbar-top',
            'Link: notebook-product-analytics located at Web Document: #document',
            'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
            'Link: cta-repo-button located at Web Document: #document => Section: header',
            'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            'Link: Cookies located at Web Document: #document => Section: footer',
            'Link: About Us located at Web Document: #document => Section: navbar-top',
            'Link: Docs located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
        ]]],
        use_to_pandas=True,
    )

    bts = funnel.get_navigation_paths(data=objectiv_df, steps=4)
    bts = _add_root_offset_sorting(bts)
    assert_equals_data(
        bts,
        expected_columns=[
            'location_stack_step_1', 'location_stack_step_2', 'location_stack_step_3', 'location_stack_step_4',
        ],
        expected_data=[
            [
                'Link: cta-docs-taxonomy located at Web Document: #document => Section: main => Section: taxonomy',
                'Link: logo located at Web Document: #document => Section: navbar-top',
                'Link: notebook-product-analytics located at Web Document: #document',
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            ],
            [
                'Link: logo located at Web Document: #document => Section: navbar-top',
                'Link: notebook-product-analytics located at Web Document: #document',
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
            ],
            [
                'Link: notebook-product-analytics located at Web Document: #document',
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                'Link: cta-repo-button located at Web Document: #document => Section: header',
            ],
            [
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                'Link: cta-repo-button located at Web Document: #document => Section: header',
                'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            ],
            [
                'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                'Link: cta-repo-button located at Web Document: #document => Section: header',
                'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu'
            ],
            [
                'Link: cta-repo-button located at Web Document: #document => Section: header',
                'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu'
            ],
            [
                'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Cookies located at Web Document: #document => Section: footer'
            ],
            [
                'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Cookies located at Web Document: #document => Section: footer',
                'Link: About Us located at Web Document: #document => Section: navbar-top'
            ],
            [
                'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Cookies located at Web Document: #document => Section: footer',
                'Link: About Us located at Web Document: #document => Section: navbar-top',
                'Link: Docs located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu'
            ],
            [
                'Link: Cookies located at Web Document: #document => Section: footer',
                'Link: About Us located at Web Document: #document => Section: navbar-top',
                'Link: Docs located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                None
            ],
            [
                'Link: About Us located at Web Document: #document => Section: navbar-top',
                'Link: Docs located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                None, None
            ],
        ],
        use_to_pandas=True,
    )

    # test different location stack column by name and different type
    bts = funnel.get_navigation_paths(data=objectiv_df, steps=2, location_stack='session_hit_number')
    bts = _add_root_offset_sorting(bts)
    assert_equals_data(
        bts,
        expected_columns=[
            'session_hit_number_step_1', 'session_hit_number_step_2'
        ],
        expected_data=[
            [1, 2],
            [2, 1],
            [1, 1],
            [1, 2],
            [2, 3],
            [3, 1],
            [1, 2],
            [2, 1],
            [1, 2],
            [2, 1],
            [1, 1]
        ],
        use_to_pandas=True,
    )

    # test none-default sort_by
    bts = funnel.get_navigation_paths(data=objectiv_df.reset_index(), steps=2, sort_by='event_id')
    bts = _add_root_offset_sorting(bts)
    assert_equals_data(
        bts,
        expected_columns=[
            'location_stack_step_1', 'location_stack_step_2'
        ],
        expected_data=[
            ['Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu', 'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack'],
            ['Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack', 'Link: cta-repo-button located at Web Document: #document => Section: header'],
            ['Link: cta-repo-button located at Web Document: #document => Section: header', 'Link: notebook-product-analytics located at Web Document: #document'],
            ['Link: notebook-product-analytics located at Web Document: #document', 'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu'],
            ['Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu', 'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu'],
            ['Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu', 'Link: Cookies located at Web Document: #document => Section: footer'],
            ['Link: Cookies located at Web Document: #document => Section: footer', 'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu'],
            ['Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu', 'Link: About Us located at Web Document: #document => Section: navbar-top'],
            ['Link: About Us located at Web Document: #document => Section: navbar-top', 'Link: Docs located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu'],
            ['Link: Docs located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu', 'Link: cta-docs-taxonomy located at Web Document: #document => Section: main => Section: taxonomy'],
            ['Link: cta-docs-taxonomy located at Web Document: #document => Section: main => Section: taxonomy', 'Link: logo located at Web Document: #document => Section: navbar-top']
        ],
        use_to_pandas=True,
    )


def test_get_navigation_paths_grouped(objectiv_df) -> None:
    modelhub = ModelHub()
    funnel = modelhub.get_funnel_discovery()

    agg_nice_names_per_session = (
        objectiv_df['location_stack'].ls.nice_name
        .sort_by_series(by=[objectiv_df['moment']]).to_json_array(objectiv_df.groupby('session_id').group_by)
    )
    assert_equals_data(
        agg_nice_names_per_session,
        expected_columns=['session_id', 'location_stack'],
        expected_data=[
            [
                1,
                [
                    'Link: cta-docs-taxonomy located at Web Document: #document => Section: main => Section: taxonomy',
                    'Link: logo located at Web Document: #document => Section: navbar-top',
                ],
            ],
            [
                2, ['Link: notebook-product-analytics located at Web Document: #document'],
            ],
            [
                3,
                [
                    'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                    'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                    'Link: cta-repo-button located at Web Document: #document => Section: header'
                ],
            ],
            [
                4,
                [
                    'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                    'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                ],
            ],
            [
                5,
                [
                    'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                    'Link: Cookies located at Web Document: #document => Section: footer',
                ],
            ],
            [
                6, ['Link: About Us located at Web Document: #document => Section: navbar-top'],
            ],
            [
                7, ['Link: Docs located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu'],
            ],
        ],
        use_to_pandas=True,
    )

    bts = funnel.get_navigation_paths(data=objectiv_df, steps=3, by=['session_id'])
    bts = _add_root_offset_sorting(bts)
    assert_equals_data(
        bts,
        expected_columns=['session_id', 'location_stack_step_1', 'location_stack_step_2', 'location_stack_step_3'],
        expected_data=[
            [
                1,
                'Link: cta-docs-taxonomy located at Web Document: #document => Section: main => Section: taxonomy',
                'Link: logo located at Web Document: #document => Section: navbar-top',
                None,
            ],
            [
                2,
                'Link: notebook-product-analytics located at Web Document: #document',
                None,
                None,
            ],
            [
                3,
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                'Link: cta-repo-button located at Web Document: #document => Section: header',
            ],
            [
                3,
                'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                'Link: cta-repo-button located at Web Document: #document => Section: header',
                None,
            ],
            [
                4,
                'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                None,
            ],
            [
                5,
                'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Cookies located at Web Document: #document => Section: footer',
                None,
            ],
            [
                6,
                'Link: About Us located at Web Document: #document => Section: navbar-top',
                None,
                None,
            ],
            [
                7,
                'Link: Docs located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                None,
                None,
            ],
        ]
    )


def test_get_navigation_paths_filtered(objectiv_df) -> None:
    modelhub = ModelHub()
    funnel = modelhub.get_funnel_discovery()
    bts = funnel.get_navigation_paths(data=objectiv_df, steps=3).materialize()
    step = 'Link: logo located at Web Document: #document => Section: navbar-top'
    bts = bts[bts['location_stack_step_1'] == step]
    assert_equals_data(
        bts,
        expected_columns=[
            'location_stack_step_1', 'location_stack_step_2', 'location_stack_step_3',
        ],
        expected_data=[
            [
                'Link: logo located at Web Document: #document => Section: navbar-top',
                'Link: notebook-product-analytics located at Web Document: #document',
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            ],
        ]
    )


@pytest.mark.parametrize("objectiv_df", ([['application']]), indirect=True)
def test_filter_navigation_paths_conversion(objectiv_df) -> None:
    modelhub = ModelHub(global_contexts=['application'])
    funnel = modelhub.get_funnel_discovery()

    objectiv_df = objectiv_df[['moment', 'location_stack', 'application']]

    with pytest.raises(ValueError, match='The is_conversion_event column '
                                         'is missing in the dataframe.'):
        funnel.get_navigation_paths(data=objectiv_df, steps=3, only_converted_paths=True)

    objectiv_df['is_conversion_event'] = False
    # define which data to use as conversion events
    objectiv_df.loc[objectiv_df.application.context.id == 'objectiv-website', 'is_conversion_event'] = True

    # add_conversion_step_column
    bts = funnel.get_navigation_paths(objectiv_df, steps=3, add_conversion_step_column=True, n_examples=3)
    bts = _add_root_offset_sorting(bts)
    assert_equals_data(
        bts,
        expected_columns=[
            'location_stack_step_1', 'location_stack_step_2', 'location_stack_step_3',
            '_first_conversion_step_number'
        ],
        expected_data=[
            [
                'Link: cta-docs-taxonomy located at Web Document: #document => Section: main => Section: taxonomy',
                'Link: logo located at Web Document: #document => Section: navbar-top',
                'Link: notebook-product-analytics located at Web Document: #document',
                1
            ],
            [
                'Link: notebook-product-analytics located at Web Document: #document',
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                2
            ],
            [
                'Link: logo located at Web Document: #document => Section: navbar-top',
                'Link: notebook-product-analytics located at Web Document: #document',
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                3
            ],
        ],
        order_by=['_first_conversion_step_number'],
        use_to_pandas=True,
    )

    # only_converted_paths
    bts = funnel.get_navigation_paths(objectiv_df, steps=3, only_converted_paths=True, n_examples=3)
    bts = _add_root_offset_sorting(bts)
    assert_equals_data(
        bts,
        expected_columns=[
            'location_stack_step_1', 'location_stack_step_2', 'location_stack_step_3'
        ],
        expected_data=[
            [
                'Link: logo located at Web Document: #document => Section: navbar-top',
                'Link: notebook-product-analytics located at Web Document: #document',
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            ],
            [
                'Link: notebook-product-analytics located at Web Document: #document',
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                None
            ],
        ],
        order_by=['location_stack_step_1'],
        use_to_pandas=True,
    )


def test_get_navigation_paths_start_from_end(objectiv_df):

    modelhub = ModelHub()
    funnel = modelhub.get_funnel_discovery()

    bts = funnel.get_navigation_paths(data=objectiv_df, steps=4, start_from_end=True)
    bts = _add_root_offset_sorting(bts, asc=False)
    assert_equals_data(
        bts,
        expected_columns=[
            'location_stack_step_1', 'location_stack_step_2', 'location_stack_step_3', 'location_stack_step_4',
        ],
        expected_data=[
            [
                'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Cookies located at Web Document: #document => Section: footer',
                'Link: About Us located at Web Document: #document => Section: navbar-top',
                'Link: Docs located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            ],
            [
                'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Cookies located at Web Document: #document => Section: footer',
                'Link: About Us located at Web Document: #document => Section: navbar-top',
            ],
            [
                'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Cookies located at Web Document: #document => Section: footer',
            ],
            [
                'Link: cta-repo-button located at Web Document: #document => Section: header',
                'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Expandable Section: The Project located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            ],
            [
                'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                'Link: cta-repo-button located at Web Document: #document => Section: header',
                'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: Contact Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            ],
            [
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                'Link: cta-repo-button located at Web Document: #document => Section: header',
                'Link: About Us located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            ],
            [
                'Link: notebook-product-analytics located at Web Document: #document',
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                'Link: cta-repo-button located at Web Document: #document => Section: header',
            ],
            [
                'Link: logo located at Web Document: #document => Section: navbar-top',
                'Link: notebook-product-analytics located at Web Document: #document',
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
            ],
            [
                'Link: cta-docs-taxonomy located at Web Document: #document => Section: main => Section: taxonomy',
                'Link: logo located at Web Document: #document => Section: navbar-top',
                'Link: notebook-product-analytics located at Web Document: #document',
                'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
            ],
            [
                None,
                'Link: cta-docs-taxonomy located at Web Document: #document => Section: main => Section: taxonomy',
                'Link: logo located at Web Document: #document => Section: navbar-top',
                'Link: notebook-product-analytics located at Web Document: #document',
            ],
            [
                None, None,
                'Link: cta-docs-taxonomy located at Web Document: #document => Section: main => Section: taxonomy',
                'Link: logo located at Web Document: #document => Section: navbar-top'
            ],
        ],
        use_to_pandas=True,
    )


def test_construct_source_target_df(objectiv_df) -> None:
    modelhub = ModelHub()
    funnel = modelhub.get_funnel_discovery()

    steps_objectiv_df = funnel.get_navigation_paths(data=objectiv_df, steps=4, n_examples=3)
    bts = funnel._construct_source_target_df(steps_objectiv_df, n_top_examples=None)

    assert_equals_data(
            bts,
            expected_columns=['source', 'target', 'value'],
            expected_data=[
                [
                    'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                    'Link: cta-repo-button located at Web Document: #document => Section: header',
                    1
                ],
                [
                    'Link: cta-docs-taxonomy located at Web Document: #document => Section: main => Section: taxonomy',
                    'Link: logo located at Web Document: #document => Section: navbar-top',
                    1
                ],
                [
                    'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                    'Link: cta-docs-location-stack located at Web Document: #document => Section: main => Section: location-stack',
                    2
                ],
                [
                    'Link: logo located at Web Document: #document => Section: navbar-top',
                    'Link: notebook-product-analytics located at Web Document: #document',
                    2
                ],
                [
                    'Link: notebook-product-analytics located at Web Document: #document',
                    'Link: GitHub located at Web Document: #document => Section: navbar-top => Overlay: hamburger-menu',
                    3
                ],
            ],
            order_by=['value', 'source'],
            use_to_pandas=True
     )

    # with n_top_examples
    steps = 3
    steps_objectiv_df = funnel.get_navigation_paths(data=objectiv_df, steps=steps, n_examples=None)

    for i in range(1, steps + 1):
        steps_objectiv_df[f'location_stack_step_{i}'] = steps_objectiv_df[f'location_stack_step_{i}'].str[:4]

    bts = funnel._construct_source_target_df(steps_objectiv_df, n_top_examples=3)

    assert_equals_data(
        bts,
        expected_columns=['source', 'target', 'value'],
        expected_data=[
            ['Link', 'Expa', 1],
            ['Link', 'Link', 16]
        ],
        order_by=['value'],
        use_to_pandas=True
    )

    # test exceptions
    steps_objectiv_df['some_column'] = steps_objectiv_df['location_stack_step_1']
    with pytest.raises(ValueError, match='Couldn\'t find any navigation path.'):
        funnel._construct_source_target_df(steps_objectiv_df[['some_column']])

    steps_objectiv_df['some_step_1'] = steps_objectiv_df['location_stack_step_1']
    with pytest.raises(ValueError, match='Provided DataFrame contains navigation paths from multiple base series,'
                                         ' e.g. x_step_1, y_step_1, ... x_step_n, y_step_n'):
        funnel._construct_source_target_df(steps_objectiv_df)
