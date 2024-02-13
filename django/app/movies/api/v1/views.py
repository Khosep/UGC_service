from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, PersonFilmWork


class MoviesApiMixin(View):
    http_method_names = ("get",)

    @staticmethod
    def get_role_data(role) -> ArrayAgg:
        return ArrayAgg(
            "persons__full_name",
            distinct=True,
            filter=Q(personfilmwork__role=role),
        )

    def get_queryset(self):
        return (
            FilmWork.objects.prefetch_related("genres")
            .values(
                "id",
                "title",
                "description",
                "creation_date",
                "rating",
                "type",
            )
            .annotate(
                genres=ArrayAgg(
                    "genres__name",
                    distinct=True,
                    filter=Q(genres__name__isnull=False),
                ),
                actors=self.get_role_data(PersonFilmWork.Role.actor),
                directors=self.get_role_data(PersonFilmWork.Role.director),
                writers=self.get_role_data(PersonFilmWork.Role.writer),
            )
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    http_method_names = ("get",)
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        paginator, page, queryset, _ = self.paginate_queryset(
            self.get_queryset(), self.paginate_by
        )
        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number()
            if page.has_previous()
            else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }
        return self.render_to_response(context)


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return {**kwargs["object"]}
