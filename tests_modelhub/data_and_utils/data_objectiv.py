import json
import datetime
from typing import List, Dict
from uuid import UUID

from pandas import Timestamp

_BASE_TEST_DATA_OBJECTIVE = [
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac301','2021-11-30','2021-11-30 10:23:36.287','b2df75d2-d7ca-48ac-9747-af47d7a4a2b2','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://objectiv.io/", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "SectionContext", "id": "navbar-top", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "OverlayContext", "id": "hamburger-menu", "_types": ["AbstractContext", "AbstractLocationContext", "OverlayContext", "SectionContext"]}, {"_type": "LinkContext", "id": "GitHub", "text": "GitHub", "href": "https://github.com/objectiv", "_types": ["AbstractContext", "AbstractLocationContext", "ActionContext", "ItemContext", "LinkContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-website", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://objectiv.io/", "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b2", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b2", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "729c84f9-91d0-4f9f-be58-5cfb2d8130e4", "time": 1636476263115, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}'),
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac302','2021-11-30','2021-11-30 10:23:36.290','b2df75d2-d7ca-48ac-9747-af47d7a4a2b2','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://objectiv.io/", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "SectionContext", "id": "main", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "SectionContext", "id": "location-stack", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "LinkContext", "id": "cta-docs-location-stack", "text": "Docs - Location Stack", "href": "/docs/taxonomy", "_types": ["AbstractContext", "AbstractLocationContext", "ActionContext", "ItemContext", "LinkContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-website", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://objectiv.io/", "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b2", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b2", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "1049e11c-bb9c-4b84-9dac-b4125998999d", "time": 1636475896879, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}'),
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac303','2021-11-30','2021-11-30 10:23:36.291','b2df75d2-d7ca-48ac-9747-af47d7a4a2b2','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://objectiv.io/", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "SectionContext", "id": "header", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "LinkContext", "id": "cta-repo-button", "text": "Objectiv on GitHub", "href": "https://github.com/objectiv/objectiv-analytics", "_types": ["AbstractContext", "AbstractLocationContext", "ActionContext", "ItemContext", "LinkContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-website", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://objectiv.io/", "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b2", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b2", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "fd8239de-032f-499a-9849-8e97214ecdf1", "time": 1636475880112, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}'),
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac304','2021-11-30','2021-11-30 10:23:36.267','b2df75d2-d7ca-48ac-9747-af47d7a4a2b1','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://objectiv.io/docs/modeling/", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "LinkContext", "id": "notebook-product-analytics", "text": "sandboxed notebook", "href": "https://notebook.objectiv.io/", "_types": ["AbstractContext", "AbstractLocationContext", "ActionContext", "ItemContext", "LinkContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-docs", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://objectiv.io/", "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b1", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b1", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "a789d8fe-5cd9-4ff0-9780-a56cf094b62a", "time": 1636475922156, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}'),
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac305','2021-12-01','2021-12-01 10:23:36.276','b2df75d2-d7ca-48ac-9747-af47d7a4a2b1','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://objectiv.io/", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "SectionContext", "id": "navbar-top", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "OverlayContext", "id": "hamburger-menu", "_types": ["AbstractContext", "AbstractLocationContext", "OverlayContext", "SectionContext"]}, {"_type": "LinkContext", "id": "About Us", "text": "About Us", "href": "about", "_types": ["AbstractContext", "AbstractLocationContext", "ActionContext", "ItemContext", "LinkContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-website", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://objectiv.io/", "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b1", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b1", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "67cbfc73-b8bd-40f6-aa8e-88cb73857d09", "time": 1636475947689, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}'),
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac306','2021-12-01','2021-12-01 10:23:36.279','b2df75d2-d7ca-48ac-9747-af47d7a4a2b1','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://www.objectiv.io/", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "SectionContext", "id": "navbar-top", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "OverlayContext", "id": "hamburger-menu", "_types": ["AbstractContext", "AbstractLocationContext", "OverlayContext", "SectionContext"]}, {"_type": "LinkContext", "id": "Contact Us", "text": "Contact Us", "href": "mailto:hi@objectiv.io", "_types": ["AbstractContext", "AbstractLocationContext", "ActionContext", "ItemContext", "LinkContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-website", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://www.objectiv.io/", "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b1", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b1", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "899c18aa-a908-43f9-9827-d4b9072205ea", "time": 1636475983057, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}'),
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac307','2021-12-02','2021-12-02 10:23:36.281','b2df75d2-d7ca-48ac-9747-af47d7a4a2b3','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://www.objectiv.io/jobs", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "SectionContext", "id": "footer", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "LinkContext", "id": "Cookies", "text": "Cookies", "href": "/privacy/cookies", "_types": ["AbstractContext", "AbstractLocationContext", "ActionContext", "ItemContext", "LinkContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-website", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://www.objectiv.io/", "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b3", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b3", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "837ae9db-497c-4925-a4c9-b2183bd3056b", "time": 1636476007981, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}'),
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac308','2021-12-02','2021-12-02 10:23:36.281','b2df75d2-d7ca-48ac-9747-af47d7a4a2b3','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://objectiv.io/docs/", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "SectionContext", "id": "navbar-top", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "OverlayContext", "id": "hamburger-menu", "_types": ["AbstractContext", "AbstractLocationContext", "OverlayContext", "SectionContext"]}, {"_type": "ExpandableSectionContext", "id": "The Project", "_types": ["AbstractContext", "AbstractLocationContext", "ExpandableSectionContext", "SectionContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-docs", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://objectiv.io/", "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b3", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b3", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "5835d00e-4099-44cc-9191-8baccc2d32fa", "time": 1636476074003, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}'),
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac309','2021-12-02','2021-12-02 14:23:36.282','b2df75d2-d7ca-48ac-9747-af47d7a4a2b3','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://objectiv.io/", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "SectionContext", "id": "navbar-top", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "LinkContext", "id": "About Us", "text": "About Us", "href": "about", "_types": ["AbstractContext", "AbstractLocationContext", "ActionContext", "ItemContext", "LinkContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-website", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://objectiv.io/", "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b3", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b3", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "690ada97-c0fa-4378-9c04-bd1f7753505a", "time": 1636476111218, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}'),
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac310','2021-12-03','2021-12-03 10:23:36.283','b2df75d2-d7ca-48ac-9747-af47d7a4a2b4','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://objectiv.io/about", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "SectionContext", "id": "navbar-top", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "OverlayContext", "id": "hamburger-menu", "_types": ["AbstractContext", "AbstractLocationContext", "OverlayContext", "SectionContext"]}, {"_type": "LinkContext", "id": "Docs", "text": "Docs", "href": "https://objectiv.io/docs/", "_types": ["AbstractContext", "AbstractLocationContext", "ActionContext", "ItemContext", "LinkContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-website", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://objectiv.io/", "user_agent": "Mozilla/5.0 (Linux; Android 10; POCOPHONE F1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b4", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b4", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "089ff754-35d6-49da-bb32-dc9031b10289", "time": 1636476142139, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}'),
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac311','2021-11-29','2021-11-29 10:23:36.286','b2df75d2-d7ca-48ac-9747-af47d7a4a2b2','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://objectiv.io/", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "SectionContext", "id": "main", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "SectionContext", "id": "taxonomy", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "LinkContext", "id": "cta-docs-taxonomy", "text": "Docs - Taxonomy", "href": "/docs/taxonomy/", "_types": ["AbstractContext", "AbstractLocationContext", "ActionContext", "ItemContext", "LinkContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-website", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://objectiv.io/", "user_agent": "Mozilla/5.0 (Linux; Android 11; SM-G986B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b2", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b2", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "fd54aa9a-b8b8-4feb-968d-8fa9f736c596", "time": 1636476191693, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}'),
    ('12b55ed5-4295-4fc1-bf1f-88d64d1ac312','2021-11-29','2021-11-29 10:23:36.287','b2df75d2-d7ca-48ac-9747-af47d7a4a2b2','{"_type": "ClickEvent", "location_stack": [{"_type": "WebDocumentContext", "id": "#document", "url": "https://objectiv.io/docs/taxonomy/", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext", "WebDocumentContext"]}, {"_type": "SectionContext", "id": "navbar-top", "_types": ["AbstractContext", "AbstractLocationContext", "SectionContext"]}, {"_type": "LinkContext", "id": "logo", "text": "Objectiv Documentation Logo", "href": "/docs/", "_types": ["AbstractContext", "AbstractLocationContext", "ActionContext", "ItemContext", "LinkContext"]}], "global_contexts": [{"_type": "ApplicationContext", "id": "objectiv-docs", "_types": ["AbstractContext", "AbstractGlobalContext", "ApplicationContext"]}, {"id": "http_context", "referrer": "https://objectiv.io/", "user_agent": "Mozilla/5.0 (Linux; Android 11; SM-G986B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36", "_type": "HttpContext", "_types": ["AbstractContext", "AbstractGlobalContext", "HttpContext"]}, {"id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b2", "cookie_id": "b2df75d2-d7ca-48ac-9747-af47d7a4a2b2", "_type": "CookieIdContext", "_types": ["AbstractContext", "AbstractGlobalContext", "CookieIdContext"]}], "id": "e2445152-327a-466f-a2bf-116f0146ab7a", "time": 1636476196460, "_types": ["AbstractEvent", "ClickEvent", "InteractiveEvent"]}')
]

IDENTITY_CONTEXTS_PER_EVENT = [
    # event: 301, user: a2b2
    [
        {'_type': 'IdentityContext', 'id': 'email', 'value': 'fake1@objectiv.io'},
        {'_type': 'IdentityContext', 'id': 'phone', 'value': '123456789'},
    ],
    # event: 302, user: a2b2
    [],
    # event: 303, user: a2b2
    [
        {'_type': 'IdentityContext', 'id': 'email', 'value': 'fake2@objectiv.io'},
    ],
    # event: 304, user: a2b1
    [],
    # event: 305, user: a2b1
    [{'_type': 'IdentityContext', 'id': 'phone', 'value': '123456789'}],
    # event: 306, user: a2b1
    [],
    # event: 307, user: a2b3
    [
        {'_type': 'IdentityContext', 'id': 'email', 'value': 'fake3@objectiv.io'},
        {'_type': 'IdentityContext', 'id': 'email', 'value': 'fake31@objectiv.io'},
    ],
    # event: 308, user: a2b3
    [],
    # event: 309, user: a2b3
    [],
    # event: 310, user: a2b4
    [],
    # event: 311, user: a2b2
    [{'_type': 'IdentityContext', 'id': 'email', 'value': 'fake4@objectiv.io'}],
    # event: 312, user: a2b2
    [],
]


def _add_identity_contexts_to_value_json(
    value: str, identity_contexts: List[Dict[str, str]]
) -> str:
    value_json = json.loads(value)
    value_json['global_contexts'].extend(identity_contexts)
    return json.dumps(value_json)


TEST_DATA_OBJECTIV = [
    (
        base_data[0],  # event_id
        base_data[1],  # day
        base_data[2],  # moment
        base_data[3],  # cookie_id
        _add_identity_contexts_to_value_json(base_data[4], identity_data),  # value

    )
    for base_data, identity_data in zip(_BASE_TEST_DATA_OBJECTIVE, IDENTITY_CONTEXTS_PER_EVENT)
]

TEST_SESSIONIZED_DATA = [
    {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac301'),
        'day': datetime.date(2021, 11, 30),
        'moment': Timestamp('2021-11-30 10:23:36.287000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b2'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://objectiv.io/', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'SectionContext', 'id': 'navbar-top', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'OverlayContext', 'id': 'hamburger-menu', '_types': ['AbstractContext', 'AbstractLocationContext', 'OverlayContext', 'SectionContext']}, {'_type': 'LinkContext', 'id': 'GitHub', 'text': 'GitHub', 'href': 'https://github.com/objectiv', '_types': ['AbstractContext', 'AbstractLocationContext', 'ActionContext', 'ItemContext', 'LinkContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-website'}],
        'http': [{'id': 'http_context', 'referrer': 'https://objectiv.io/', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b2', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b2'}], 'identity': [{'id': 'email', 'value': 'fake1@objectiv.io'}, {'id': 'phone', 'value': '123456789'}],
        'session_id': 3,
        'session_hit_number': 1,
    }, {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac302'),
        'day': datetime.date(2021, 11, 30),
        'moment': Timestamp('2021-11-30 10:23:36.290000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b2'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://objectiv.io/', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'SectionContext', 'id': 'main', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'SectionContext', 'id': 'location-stack', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'LinkContext', 'id': 'cta-docs-location-stack', 'text': 'Docs - Location Stack', 'href': '/docs/taxonomy', '_types': ['AbstractContext', 'AbstractLocationContext', 'ActionContext', 'ItemContext', 'LinkContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-website'}],
        'http': [{'id': 'http_context', 'referrer': 'https://objectiv.io/', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b2', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b2'}],
        'identity': [],
        'session_id': 3,
        'session_hit_number': 2,
    }, {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac303'),
        'day': datetime.date(2021, 11, 30),
        'moment': Timestamp('2021-11-30 10:23:36.291000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b2'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://objectiv.io/', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'SectionContext', 'id': 'header', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'LinkContext', 'id': 'cta-repo-button', 'text': 'Objectiv on GitHub', 'href': 'https://github.com/objectiv/objectiv-analytics', '_types': ['AbstractContext', 'AbstractLocationContext', 'ActionContext', 'ItemContext', 'LinkContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-website'}],
        'http': [{'id': 'http_context', 'referrer': 'https://objectiv.io/', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b2', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b2'}],
        'identity': [{'id': 'email', 'value': 'fake2@objectiv.io'}],
        'session_id': 3,
        'session_hit_number': 3,
    }, {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac304'),
        'day': datetime.date(2021, 11, 30),
        'moment': Timestamp('2021-11-30 10:23:36.267000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b1'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://objectiv.io/docs/modeling/', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'LinkContext', 'id': 'notebook-product-analytics', 'text': 'sandboxed notebook', 'href': 'https://notebook.objectiv.io/', '_types': ['AbstractContext', 'AbstractLocationContext', 'ActionContext', 'ItemContext', 'LinkContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-docs'}],
        'http': [{'id': 'http_context', 'referrer': 'https://objectiv.io/', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b1', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b1'}],
        'identity': [],
        'session_id': 2,
        'session_hit_number': 1,
    }, {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac305'),
        'day': datetime.date(2021, 12, 1),
        'moment': Timestamp('2021-12-01 10:23:36.276000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b1'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://objectiv.io/', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'SectionContext', 'id': 'navbar-top', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'OverlayContext', 'id': 'hamburger-menu', '_types': ['AbstractContext', 'AbstractLocationContext', 'OverlayContext', 'SectionContext']}, {'_type': 'LinkContext', 'id': 'About Us', 'text': 'About Us', 'href': 'about', '_types': ['AbstractContext', 'AbstractLocationContext', 'ActionContext', 'ItemContext', 'LinkContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-website'}],
        'http': [{'id': 'http_context', 'referrer': 'https://objectiv.io/', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b1', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b1'}],
        'identity': [{'id': 'phone', 'value': '123456789'}],
        'session_id': 4,
        'session_hit_number': 1,
    }, {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac306'),
        'day': datetime.date(2021, 12, 1),
        'moment': Timestamp('2021-12-01 10:23:36.279000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b1'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://www.objectiv.io/', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'SectionContext', 'id': 'navbar-top', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'OverlayContext', 'id': 'hamburger-menu', '_types': ['AbstractContext', 'AbstractLocationContext', 'OverlayContext', 'SectionContext']}, {'_type': 'LinkContext', 'id': 'Contact Us', 'text': 'Contact Us', 'href': 'mailto:hi@objectiv.io', '_types': ['AbstractContext', 'AbstractLocationContext', 'ActionContext', 'ItemContext', 'LinkContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-website'}],
        'http': [{'id': 'http_context', 'referrer': 'https://www.objectiv.io/', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b1', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b1'}],
        'identity': [],
        'session_id': 4,
        'session_hit_number': 2,
    }, {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac307'),
        'day': datetime.date(2021, 12, 2),
        'moment': Timestamp('2021-12-02 10:23:36.281000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b3'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://www.objectiv.io/jobs', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'SectionContext', 'id': 'footer', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'LinkContext', 'id': 'Cookies', 'text': 'Cookies', 'href': '/privacy/cookies', '_types': ['AbstractContext', 'AbstractLocationContext', 'ActionContext', 'ItemContext', 'LinkContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-website'}],
        'http': [{'id': 'http_context', 'referrer': 'https://www.objectiv.io/', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b3', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b3'}],
        'identity': [{'id': 'email', 'value': 'fake3@objectiv.io'}, {'id': 'email', 'value': 'fake31@objectiv.io'}],
        'session_id': 5,
        'session_hit_number': 1,
    }, {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac308'),
        'day': datetime.date(2021, 12, 2),
        'moment': Timestamp('2021-12-02 10:23:36.281000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b3'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://objectiv.io/docs/', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'SectionContext', 'id': 'navbar-top', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'OverlayContext', 'id': 'hamburger-menu', '_types': ['AbstractContext', 'AbstractLocationContext', 'OverlayContext', 'SectionContext']}, {'_type': 'ExpandableSectionContext', 'id': 'The Project', '_types': ['AbstractContext', 'AbstractLocationContext', 'ExpandableSectionContext', 'SectionContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-docs'}],
        'http': [{'id': 'http_context', 'referrer': 'https://objectiv.io/', 'user_agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b3', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b3'}],
        'identity': [],
        'session_id': 5,
        'session_hit_number': 2,
    }, {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac309'),
        'day': datetime.date(2021, 12, 2),
        'moment': Timestamp('2021-12-02 14:23:36.282000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b3'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://objectiv.io/', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'SectionContext', 'id': 'navbar-top', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'LinkContext', 'id': 'About Us', 'text': 'About Us', 'href': 'about', '_types': ['AbstractContext', 'AbstractLocationContext', 'ActionContext', 'ItemContext', 'LinkContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-website'}],
        'http': [{'id': 'http_context', 'referrer': 'https://objectiv.io/', 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b3', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b3'}],
        'identity': [],
        'session_id': 6,
        'session_hit_number': 1,
    }, {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac310'),
        'day': datetime.date(2021, 12, 3),
        'moment': Timestamp('2021-12-03 10:23:36.283000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b4'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://objectiv.io/about', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'SectionContext', 'id': 'navbar-top', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'OverlayContext', 'id': 'hamburger-menu', '_types': ['AbstractContext', 'AbstractLocationContext', 'OverlayContext', 'SectionContext']}, {'_type': 'LinkContext', 'id': 'Docs', 'text': 'Docs', 'href': 'https://objectiv.io/docs/', '_types': ['AbstractContext', 'AbstractLocationContext', 'ActionContext', 'ItemContext', 'LinkContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-website'}],
        'http': [{'id': 'http_context', 'referrer': 'https://objectiv.io/', 'user_agent': 'Mozilla/5.0 (Linux; Android 10; POCOPHONE F1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b4', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b4'}],
        'identity': [],
        'session_id': 7,
        'session_hit_number': 1,
    }, {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac311'),
        'day': datetime.date(2021, 11, 29),
        'moment': Timestamp('2021-11-29 10:23:36.286000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b2'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://objectiv.io/', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'SectionContext', 'id': 'main', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'SectionContext', 'id': 'taxonomy', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'LinkContext', 'id': 'cta-docs-taxonomy', 'text': 'Docs - Taxonomy', 'href': '/docs/taxonomy/', '_types': ['AbstractContext', 'AbstractLocationContext', 'ActionContext', 'ItemContext', 'LinkContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-website'}],
        'http': [{'id': 'http_context', 'referrer': 'https://objectiv.io/', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; SM-G986B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b2', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b2'}],
        'identity': [{'id': 'email', 'value': 'fake4@objectiv.io'}],
        'session_id': 1,
        'session_hit_number': 1,
    }, {
        'event_id': UUID('12b55ed5-4295-4fc1-bf1f-88d64d1ac312'),
        'day': datetime.date(2021, 11, 29),
        'moment': Timestamp('2021-11-29 10:23:36.287000'),
        'user_id': UUID('b2df75d2-d7ca-48ac-9747-af47d7a4a2b2'),
        'location_stack': [{'_type': 'WebDocumentContext', 'id': '#document', 'url': 'https://objectiv.io/docs/taxonomy/', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext', 'WebDocumentContext']}, {'_type': 'SectionContext', 'id': 'navbar-top', '_types': ['AbstractContext', 'AbstractLocationContext', 'SectionContext']}, {'_type': 'LinkContext', 'id': 'logo', 'text': 'Objectiv Documentation Logo', 'href': '/docs/', '_types': ['AbstractContext', 'AbstractLocationContext', 'ActionContext', 'ItemContext', 'LinkContext']}],
        'event_type': 'ClickEvent',
        'stack_event_types': ['AbstractEvent', 'ClickEvent', 'InteractiveEvent'],
        'application': [{'id': 'objectiv-docs'}],
        'http': [{'id': 'http_context', 'referrer': 'https://objectiv.io/', 'user_agent': 'Mozilla/5.0 (Linux; Android 11; SM-G986B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36', 'remote_address': None}],
        'cookie_id': [{'id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b2', 'cookie_id': 'b2df75d2-d7ca-48ac-9747-af47d7a4a2b2'}],
        'identity': [],
        'session_id': 1,
        'session_hit_number': 2,
    },
]
GLOBAL_CONTEXTS_IN_CURRENT_TEST_DATA = (
    'application', 'http', 'cookie_id', 'identity'
)
