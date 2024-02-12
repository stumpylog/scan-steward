# examples/views/department_views.py

from ninja_crud import views
from ninja_crud import viewsets

from image_metadata.models import Tag
from image_metadata.schemas import Location
from image_metadata.schemas import LocationIn
from image_metadata.schemas import LocationOut
from image_metadata.schemas import LocationUpdate
from image_metadata.schemas import TagIn
from image_metadata.schemas import TagOut
from image_metadata.schemas import TagUpdate


class TagViewSet(viewsets.ModelViewSet):
    model = Tag
    default_input_schema = TagIn
    default_output_schema = TagOut

    list_departments = views.ListModelView()
    create_department = views.CreateModelView()
    retrieve_department = views.RetrieveModelView()
    update_department = views.UpdateModelView(input_schema=TagUpdate)
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
