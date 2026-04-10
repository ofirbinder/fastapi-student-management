from app.core.DomainError import InvalidAPIFeaturesParamsError
from app.models.student_schema import StudentSchema


class APIFeatures:
    def __init__(self, data: list, query_params: dict):
        self.data = data
        self.query_params = query_params

    def sort(self):
        sort_by = self.query_params.get("sort_by")
        if not sort_by:
            return self
        if "," in sort_by:
            raise InvalidAPIFeaturesParamsError(
                f"Multi-field (sort_by={sort_by}) sorting is not supported."
            )
        reverse = sort_by.startswith("-")
        field = sort_by.lstrip("-")
        if field not in StudentSchema.model_fields:
            raise InvalidAPIFeaturesParamsError(
                f"Field '{field}' does not exist on student schema!"
            )
        try:
            self.data.sort(key=lambda x: x.get(field, ""), reverse=reverse)
        except TypeError as err:
            raise InvalidAPIFeaturesParamsError(
                f"Field '{field}' contains inconsistent or complex data types that cannot be sorted."
            ) from err
        return self

    def paginate(self):
        page = int(self.query_params.get("page", 1))
        limit = int(self.query_params.get("limit", 10))
        skip = (page - 1) * limit
        self.data = self.data[skip : skip + limit]
        return self

    @property
    def results(self):
        return self.data
