from django.urls import path
from .views import index,visit_photography_site
from .admin_views import custom_admin_index
from .photographer_views import custom_photographer_index,add_photographer_info,stat_add,add_gallery,add_team,add_service,add_package,view_photographer_info,view_stat,view_gallery,view_team,view_service,view_package,view_booking,export_booking_csv,export_booking_pdf,add_booking,delete_booking,delete_package,delete_service,delete_team,generate_invoice,get_invoice,download_invoice_pdf,edit_photographer_info,update_photographer_info

urlpatterns = [
    path('',index,name='index'),
    path('photographer/<int:id>/',visit_photography_site,name='visit_photography_site'),


    # customadmin views
    path('customadmin/',custom_admin_index,name='custom_admin_index'),



    # photographer views
    path('customadmin/photographer/',custom_photographer_index,name='custom_photographer_index'),
    
    path('customadmin/add/info/',add_photographer_info,name='add_photographer_info'),
    path('customadmin/view/info/',view_photographer_info,name='view_photographer_info'),
    path('photographer/edit/',edit_photographer_info,name='edit_photographer_info'),
    path('photographer/update/',update_photographer_info,name='update_photographer_info'),
    
    path('customadmin/add/stat/',stat_add,name='stat_add'),
    path('customadmin/view/stat/',view_stat,name='view_stat'),

    path('customadmin/add/gallery/',add_gallery,name='add_gallery'),
    path('customadmin/view/gallery/',view_gallery,name='view_gallery'),

    path('customadmin/add/team/',add_team,name='add_team'),
    path('customadmin/view/team/',view_team,name='view_team'),
    path('customadmin/delete/team/<int:id>/',delete_team,name='delete_team'),

    path('customadmin/add/service/',add_service,name='add_service'),
    path('customadmin/view/service/',view_service,name='view_service'),
    path('customadmin/delete/service/<int:id>/',delete_service,name='delete_service'),

    path('customadmin/add/package/',add_package,name='add_package'),
    path('customadmin/view/package/',view_package,name='view_package'),
    path('customadmin/delete/package/<int:id>/',delete_package,name='delete_package'),
    
    path('customadmin/view/bookings/',view_booking,name='view_booking'),
    path('customadmin/add/bookings/',add_booking,name='add_booking'),
    path('customadmin/delete/bookings/<int:id>/',delete_booking,name='delete_booking'),
    path('customadmin/bookings/export/csv/',export_booking_csv,name='export_booking_csv'),
    path('customadmin/bookings/export/pdf/',export_booking_pdf,name='export_booking_pdf'),
    
    
    path('customadmin/bookings/generate-invoice/<int:id>/',generate_invoice,name='generate_invoice'),
    path('customadmin/get/invoices/',get_invoice,name='get_invoice'),
    path('customadmin/download/invoice/<int:id>/',download_invoice_pdf,name='download_invoice_pdf'),
]