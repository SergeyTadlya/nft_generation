from django.shortcuts import render, redirect
from nft.models import Collection, Image
from config.settings import MEDIA_ROOT, env
import os


def home(request):
    return render(request=request, template_name="home.html")


def get_contract_nft(request):
    res = {
        'api_key': env.str('CONTACT_API_KEY'),
        'contract_address': env.str('CONTACT_ADDRESS'),
        'token_id': env.str('TOKEN_ID'),
    }
    return render(request=request, template_name="get_contract_nft.html", context=res)


def collections(request, type: str):
    res = []
    for collection in Collection.objects.filter(type=type):
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


def delete_image(request, image_id: int):
    avatar = Image.objects.filter(id=image_id).first()
    if avatar:
        local_file_path = os.path.join(MEDIA_ROOT, str(avatar.image))
        if os.path.exists(local_file_path):
            os.remove(local_file_path)
        avatar.delete()
    return redirect(to="/collections/?deleted=true")


def delete_collection(request, collection_id: int):
    collection = Collection.objects.filter(id=collection_id).first()
    if collection:
        images_to_delete = collection.images.all()
        for image in images_to_delete:
            if image.image:
                local_file_path = os.path.join(MEDIA_ROOT, str(image.image))
                if os.path.exists(local_file_path):
                    os.remove(local_file_path)
                image.delete()
                local_folder_path = os.path.join(MEDIA_ROOT, 'avatars', f'collection_{image.collection_name}')
                if os.path.exists(local_folder_path):
                    os.rmdir(local_folder_path)
        collection.delete()
    return redirect(to="/collections/?deleted=true")