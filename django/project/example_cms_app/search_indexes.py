from haystack.indexes import *
from haystack import site
from models import AnotherExampleModel

class AnotherExampleModelIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr='title')
    author = CharField(model_attr='author')
    region = MultiValueField()
    sector = MultiValueField()
    equity_focus = MultiValueField()
    status = CharField(null=True)
    type = CharField(null=True)

    def prepare_region(self, obj):
        return [region.name for region in obj.region.all()]

    def prepare_sector(self, obj):
        return [sector.name for sector in obj.sector.all()]

    def prepare_equity_focus(self, obj):
        return [equity.name for equity in obj.equity_focus.all()]

    def prepare_type(self, obj):
        if obj.review_type:
            return obj.review_type.type
        return ""

    def prepare_status(self, obj):
        if obj.status:
            return obj.status.status
        return ""

    def index_queryset(self):
        return AnotherExampleModel.objects.filter(published=True) # Only add already published


site.register(AnotherExampleModel, AnotherExampleModelIndex)
