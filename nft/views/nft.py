from django.views.generic import TemplateView

from config.settings import MEDIA_ROOT
from nft.helpers.nft_options import GenerateNFT
from django.shortcuts import HttpResponse, render, redirect
from nft.forms import ImageForm
from nft.models import Collection, Image
from pinata import Pinata
import requests, os
from config.settings import env


# def nft_generate(request):
#     amount = 2
#     for number in range(amount):
#         slime_num = number + 1
#         nft = GenerateNFT()
#         res = nft.create_image(slime_num)
#         print(">>>>>>>>>>>>>>>>>>>>> res", res)
#
#     return HttpResponse('ok')


class NFTGenerateView(TemplateView):
    template_name = "create_nft.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ImageForm()
        return context

    def post(self, request, *args, **kwargs):
        nft = GenerateNFT()
        context = self.get_context_data(**kwargs)
        context = nft.generate_collection(self.request, context)
        context["form"] = ImageForm()
        # return self.render_to_response(context)
        return render(request, self.template_name, context)


def nft_collections(request):
    res = []
    for collection in Collection.objects.filter(type='nft'):
        res.append({
            'id': collection.id,
            'name': collection.name,
            'images': collection.images.all(),
            'date_created': collection.created_on,
        })

    context: dict = {
        'collections': res
    }
    return render(request=request, template_name="collections.html", context=context)


def create_payload(folder_name):
    files = []
    folder_path = os.path.join(MEDIA_ROOT, f'nft/{folder_name}/')
    files.append(('pinataMetadata', (None, '{"name":"' + folder_name + '"}')))
    for file_name in os.listdir(folder_path):
        path = f'{folder_name}/{file_name}'
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(('file', (path, open(file_path, 'rb'))))
    return files


def pinata_pin_folder(request):
    # secret_access_token = env.str('PINATA_ACCEESS_TOKEN')
    # url = env.str('PINATA_PIN_FOLDER_URL')
    # headers = {
    #     'Authorization': f'Bearer {secret_access_token}',
    # }
    #
    # response = requests.post(url, headers=headers, files=files)
    # print(response.status_code)
    # print(response.json())

    return HttpResponse('ok')
