from rest_framework.viewsets import ReadOnlyModelViewSet

from regions.models import Region
from regions.serializers import RegionSerializer


class RegionViewSet(ReadOnlyModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
