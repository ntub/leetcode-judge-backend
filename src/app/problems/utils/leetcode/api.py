from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

import humps

from django.conf import settings
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from graphql import DocumentNode


class GraphAPIMethod(str, Enum):
    QUERY = "query"


class LeetCodeGraphAPI:
    QUESTION_LIST_QUERY_FILE = "QuestionList.graphql"
    QUESTION_QUERY_FILE = "Question.graphql"

    def __init__(self) -> None:
        self.transport = RequestsHTTPTransport(
            url="https://leetcode.com/graphql",
            verify=True,
            retries=3,
        )
        self.graphql_dir: Path = settings.BASE_DIR / "graphql"

    def _read_graphql(self, method: GraphAPIMethod, file: str) -> str:
        file_path = self.graphql_dir / str(method.value) / file
        with open(file_path, "r") as f:
            return f.read()

    @cached_property
    def question_list_query(self) -> DocumentNode:
        query_str = self._read_graphql(
            GraphAPIMethod.QUERY,
            self.QUESTION_LIST_QUERY_FILE,
        )
        return gql(query_str)

    @cached_property
    def question_query(self) -> DocumentNode:
        query_str = self._read_graphql(GraphAPIMethod.QUERY, self.QUESTION_QUERY_FILE)
        return gql(query_str)

    @property
    def client(self) -> Client:
        return Client(
            transport=self.transport,
            fetch_schema_from_transport=False,
        )

    def _execute(
        self,
        gql_doc: DocumentNode,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        data = self.client.execute(
            gql_doc,
            variable_values=params,
        )
        return humps.decamelize(data)  # type: ignore

    def question_list(
        self,
        skip: int = 0,
        limit: int = 50,
        category_slug: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = {
            "categorySlug": category_slug or "",
            "skip": skip,
            "limit": limit,
            "filters": {},
        }
        data = self._execute(self.question_list_query, params)
        return data.get("problemset_question_list", {})

    def question(self, title_slug: str) -> Dict[str, Any]:
        params = {
            "titleSlug": title_slug,
        }
        data = self._execute(self.question_query, params)
        return data.get("question", {})

    def question_list_iterator(
        self,
        limit: int = 50,
        category_slug: Optional[str] = None,
    ) -> Iterator[List[Dict[str, Any]]]:
        offset = 0
        response = self.question_list(offset, limit, category_slug)
        total = response.get("total", 0)
        data = response.get("questions", [])
        while total >= offset and data:
            offset += len(data)
            yield data
            response = self.question_list(offset, limit, category_slug)
            data = response.get("questions", [])
