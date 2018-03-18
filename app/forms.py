from wtforms import Form, StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.upload import BS3FileUploadFieldWidget, FileUploadField
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder import SimpleFormView
from flask_babel import lazy_gettext as _
from app import appbuilder


class MyForm(DynamicForm):
    sequence = StringField(('sequence'),
                         description=('Your field number one!'),
                         widget=TextArea())
    analysis = StringField(('analysis'),
                         description=('Your field number one!'),
                         widget=TextArea())
    security = StringField(('security'),
                         description=('Your field number one!'),
                         widget=TextArea())

    bpipe = StringField(('bpipe'),
                         description=('Your field number one!'),
                         widget=TextArea())
    pdump = StringField(('pdump'),
                         description=('Your field number one!'),
                         widget=TextArea())
    extra = StringField(('extra'),
                         description=('Your field number one!'),
                         widget=TextArea())