# examples/views/department_views.py

from ninja_crud import views
from ninja_crud import viewsets

from image_metadata.models import Subject
from image_metadata.schemas import Location
from image_metadata.schemas import LocationIn
from image_metadata.schemas import LocationOut
from image_metadata.schemas import LocationUpdate
from image_metadata.schemas import SubjectIn
from image_metadata.schemas import SubjectOut
from image_metadata.schemas import SubjectUpdate


class SubjectViewSet(viewsets.ModelViewSet):
    model = Subject
    default_input_schema = SubjectIn
    default_output_schema = SubjectOut

    list_departments = views.ListModelView()
    create_department = views.CreateModelView()
    retrieve_department = views.RetrieveModelView()
    update_department = views.UpdateModelView(input_schema=SubjectUpdate)
    delete_department = views.DeleteModelView()


class LocationViewSet(viewsets.ModelViewSet):
    model = Location
    default_input_schema = LocationIn
    default_output_schema = LocationOut

    list_departments = views.ListModelView()
    create_department = views.CreateModelView()
    retrieve_department = views.RetrieveModelView()
    update_department = views.UpdateModelView(input_schema=LocationUpdate)
    delete_department = views.DeleteModelView()
