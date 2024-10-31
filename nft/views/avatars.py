from nft.helpers.generate_avatar import generate_avatars
from django.views.generic import TemplateView
from nft.forms import ImageForm


class GenerateView(TemplateView):
    template_name = "create_nft.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ImageForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context = generate_avatars(self.request, context)
        context["form"] = ImageForm()

        return self.render_to_response(context)



