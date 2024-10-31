from config.settings import MEDIA_ROOT, BASE_DIR
from nft.models import Collection
from django.core.files import File
import os, requests, json
from config.settings import env


class Metadata:
    __slots__: tuple[str] = ("pinata_secret_access_token", "pinata_api_url")

    def __init__(self) -> None:
        # pinata api data
        self.pinata_secret_access_token = env.str('PINATA_ACCEESS_TOKEN')
        self.pinata_api_url = env.str('PINATA_API_URL')

    @staticmethod
    def create_payload(folder_collection_name: str, folder_type_name: str):
        files = []
        folder_path = os.path.join(MEDIA_ROOT, f'nft/{folder_collection_name}/{folder_type_name}/')
        folder_name = f'{folder_collection_name}_{folder_type_name}'
        files.append(('pinataMetadata', (None, '{"name":"' + folder_name + '"}')))
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                path = f'{folder_name}/{file_name}'
                files.append(('file', (path, open(file_path, 'rb'))))
        return files

    def pin_folder(self, folder_collection_name: str, folder_type_name: str) -> dict:
        """ Pin folder with nft in pinata to get the IpfsHash """

        url = f"{self.pinata_api_url}pinning/pinFileToIPFS"
        headers = {
            'Authorization': f'Bearer {self.pinata_secret_access_token}',
        }
        files = self.create_payload(folder_collection_name, folder_type_name)
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            res = {'status': response.status_code, 'hash': response.json()['IpfsHash']}
        else:
            res = {'status': response.status_code, 'error': response.json()['error']}

        return res

    def set_nft_metadata(self, collection: Collection) -> None or dict:
        """ Set metadata for nft collection and save it in json"""

        # pin in pinata images from collection
        img_ipfs_hash = self.pin_folder(collection.folder_name, 'img')
        if img_ipfs_hash['status'] == 200:
            json_files = []
            for image in collection.images.all():
                # create json with metadata
                base_json = {
                    "name": image.name,
                    "description": image.description,
                    "image": f"ipfs://{img_ipfs_hash['hash']}/{image.name}.png",
                    "attributes": [image.attributes]
                }
                # save json
                json_filename = f"{image.name}.json"
                json_file_path = os.path.join(BASE_DIR, json_filename)
                with open(json_file_path, "w") as json_file:
                    json.dump(base_json, json_file, indent=4)
                if os.path.exists(json_file_path):
                    image.json.save(json_filename, File(open(json_filename, 'rb')), save=True)
                    image.save()
                    os.remove(json_filename)

            # pin in pinata json files from collection
            json_ipfs_hash = self.pin_folder(collection.folder_name, 'json')
            if json_ipfs_hash['status'] == 200:
                collection.pinata_img_hash = img_ipfs_hash['hash']
                collection.pinata_json_hash = json_ipfs_hash['hash']
                collection.save()

            else:
                return {'error': json_ipfs_hash['error']}
        else:
            return {'error': img_ipfs_hash['error']}

