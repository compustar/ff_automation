import browser_extentions
from inspect import getmembers, isfunction

def extend_driver(driver_class):
    for method_name, method in [o for o in getmembers(browser_extentions) if isfunction(o[1])]:
        setattr(driver_class, method_name, method)
