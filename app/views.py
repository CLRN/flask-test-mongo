import calendar
from flask_appbuilder import expose, has_access
from flask import url_for, make_response, Response, g
from flask_appbuilder import ModelView
from flask_appbuilder.models.mongoengine.interface import MongoEngineInterface
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.widgets import FormWidget
from flask_appbuilder._compat import as_unicode
from flask_babel import lazy_gettext as _
from app import appbuilder
from .models import Analysis, Tick, Security
from .forms import MyForm


def get_user():
    return g.user.id


class MySearchWidget(FormWidget):
    template = 'appbuilder/general/widgets/search.html'
    filters = None

    def __init__(self, **kwargs):
        self.filters = kwargs.get('filters')
        return super(MySearchWidget, self).__init__(**kwargs)

    def __call__(self, **kwargs):
        label_columns = {}
        form_fields = {}
        search_filters = {}
        dict_filters = self.filters.get_search_filters()
        dict_filters.append('extra')
        for col in self.template_args['include_cols']:
            label_columns[col] = as_unicode(self.template_args['form'][col].label.text)
            form_fields[col] = self.template_args['form'][col]()
            if col in dict_filters:
                search_filters[col] = [as_unicode(flt.name) for flt in dict_filters[col]]

        '''
        form = MyForm()

        label_columns['extra'] = u'extra'
        form_fields['extra'] = form['extra']()
        search_filters['extra'] = search_filters['sequence']
        '''

        kwargs['label_columns'] = label_columns
        kwargs['form_fields'] = form_fields
        kwargs['search_filters'] = search_filters
        kwargs['active_filters'] = self.filters.get_filters_values_tojson()
        return super(MySearchWidget, self).__call__(**kwargs)


class TickModelView(ModelView):
    datamodel = MongoEngineInterface(Tick)
    list_columns = ['sequence', 'pdump', 'bpipe']
    add_columns = ['sequence', 'analysis', 'security']
    search_columns = ['sequence', 'analysis', 'security', 'extra']
    search_widget = MySearchWidget
    search_form = MyForm


class SecurityModelView(ModelView):
    datamodel = MongoEngineInterface(Security)
    related_views = [TickModelView]
    search_columns = ['object_id', 'ticker']


class AnalysisModelView(ModelView):
    datamodel = MongoEngineInterface(Analysis)
    related_views = [TickModelView]
    search_columns = ['name']
    list_columns = ['name']
    add_columns = ['name', 'input']


class TickChartView(GroupByChartView):
    datamodel = MongoEngineInterface(Tick)
    chart_title = 'Grouped ticks'
    label_columns = TickModelView.label_columns
    chart_type = 'PieChart'

    definitions = [
        {
            'group': 'analysis',
            'series': [(aggregate_count, 'analysis.name')]
        },
        {
            'group': 'security',
            'series': [(aggregate_count, 'security.object_id')]
        }
    ]


appbuilder.add_view(AnalysisModelView, "List Analysis", icon="fa-folder-open-o", category="Analysis", category_icon='fa-envelope')
appbuilder.add_view(SecurityModelView, "List Securities", icon="fa-folder-open-o", category="Analysis", category_icon='fa-envelope')
appbuilder.add_separator("Analysis")
appbuilder.add_view(TickModelView, "List Ticks", icon="fa-folder-open-o", category="Ticks", category_icon='fa-envelope')
appbuilder.add_view(TickChartView, "Ticks Chart", icon="fa-dashboard", category="Ticks")

appbuilder.security_cleanup()
