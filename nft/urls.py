from django.urls import path
from .views import *

urlpatterns = [
    path(route="", view=home, name="home"),
    path(route="get_contract_nft/", view=get_contract_nft, name="get_contract_nft"),
    path(route="collections/<str:type>/", view=collections, name="collections"),
    path(route="img/delete/<int:image_id>/", view=delete_image, name="delete_image"),
    path(route="collection/delete/<int:collection_id>/", view=delete_collection, name="delete_collection"),
    # avatars
    path(route="avatars/", view=GenerateView.as_view(), name="avatars_generate"),
    # nft
    # path(route="", view=nft_generate, name="nft_generate"),
    path(route="nft/", view=NFTGenerateView.as_view(), name="nft_generate"),
    path(route="pinata_pin_folder/", view=pinata_pin_folder, name="pinata_pin_folder"),
]
