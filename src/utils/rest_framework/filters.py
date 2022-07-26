import typing

from rest_framework import filters, request, views

__all__ = ["SearchFilter"]


class SearchFilter(filters.SearchFilter):
    def get_search_fields(
        self,
        view: views.APIView,
        request: typing.Optional[request.Request] = None,
    ) -> typing.Iterable[str]:
        """get_search_fields is same as super, but make request optional."""
        return typing.cast(typing.Iterable[str], getattr(view, "search_fields", None))

    def get_search_description_with_fields(
        self,
        search_fields: typing.Iterable[str],
    ) -> str:
        search_fields_str = ", ".join(search_fields)
        return f"{self.search_description} ({search_fields_str})"

    def get_schema_fields(self, view: views.APIView) -> typing.List[typing.Any]:
        search_fields = self.get_search_fields(view)
        if not search_fields:
            return []

        self.search_description = self.get_search_description_with_fields(search_fields)
        return super().get_schema_fields(view)

    def get_schema_operation_parameters(self, view: views.APIView) -> typing.Any:
        search_fields = self.get_search_fields(view)
        if not search_fields:
            return []

        self.search_description = self.get_search_description_with_fields(search_fields)
        return super().get_schema_operation_parameters(view)
