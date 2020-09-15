from . import views
from .models import Category

def categories(request):
    cat = Category.objects.all()
    return {
        'categories': cat
    }