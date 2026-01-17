""" Vista para la pagina de inicio """


from django.views.generic import TemplateView
# Create your views here.


class HomePageView(TemplateView):
    """ Vista para la pagina de inicio """

    template_name = "home/index.html"


