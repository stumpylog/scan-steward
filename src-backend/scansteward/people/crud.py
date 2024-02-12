from ninja_crud import views
from ninja_crud import viewsets

from scansteward.models import Person
from scansteward.people.schemas import PersonCreate
from scansteward.people.schemas import PersonRead
from scansteward.people.schemas import PersonUpdate


class PersonViewSet(viewsets.ModelViewSet):
    model = Person
    default_input_schema = PersonCreate
    default_output_schema = PersonRead

    list_people = views.ListModelView()
    create_person = views.CreateModelView()
    get_person = views.RetrieveModelView()
    update_person = views.UpdateModelView(input_schema=PersonUpdate)
    delete_person = views.DeleteModelView()
