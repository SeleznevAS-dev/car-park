from models import Manager, ManagerEnterprise, User
from sqladmin import ModelView

from models.brand import Brand
from models.driver import Driver
from models.enterprise import Enterprise
from models.vehicle import Vehicle
from models.driver_vehicle import DriverVehicle


class VehicleView(ModelView, model=Vehicle):
    column_list = [k for k, v in Vehicle.__dict__.items() if hasattr(v, "prop")]
    form_excluded_columns = [Vehicle.created_at, Vehicle.updated_at]


class BrandView(ModelView, model=Brand):
    column_list = [k for k, v in Brand.__dict__.items() if hasattr(v, "prop")]
    form_excluded_columns = [Brand.created_at, Brand.updated_at]


class DriverView(ModelView, model=Driver):
    column_list = [k for k, v in Driver.__dict__.items() if hasattr(v, "prop")]
    form_excluded_columns = [Driver.created_at, Driver.updated_at]


class EnterpriseView(ModelView, model=Enterprise):
    column_list = [k for k, v in Enterprise.__dict__.items() if hasattr(v, "prop")]
    form_excluded_columns = [Enterprise.created_at, Enterprise.updated_at]


class DriverVehicleView(ModelView, model=DriverVehicle):
    column_list = [k for k, v in DriverVehicle.__dict__.items() if hasattr(v, "prop")]


class ManagerView(ModelView, model=Manager):
    column_list = [k for k, v in Manager.__dict__.items() if hasattr(v, "prop")]
    form_excluded_columns = [Manager.created_at, Manager.updated_at]


class ManagerEnterpriseView(ModelView, model=ManagerEnterprise):
    column_list = [k for k, v in ManagerEnterprise.__dict__.items() if hasattr(v, "prop")]


class UserView(ModelView, model=User):
    column_list = [k for k, v in User.__dict__.items() if hasattr(v, "prop")]
    form_excluded_columns = [User.created_at, User.updated_at]


def add_views_to_admin(admin):
    admin.add_view(VehicleView)
    admin.add_view(BrandView)
    admin.add_view(DriverView)
    admin.add_view(EnterpriseView)
    admin.add_view(DriverVehicleView)
    admin.add_view(ManagerView)
    admin.add_view(ManagerEnterpriseView)
    admin.add_view(UserView)
