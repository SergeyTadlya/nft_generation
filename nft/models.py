from django.db.models import *


def img_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatars/<id>/<filename>
    return "{0}/collection_{1}/img/{2}".format(instance.collection_type, instance.collection_id, filename)


def json_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatars/<id>/<filename>
    return "{0}/collection_{1}/json/{2}".format(instance.collection_type, instance.collection_id, filename)


class Image(Model):
    collection_id = IntegerField()
    collection_type = CharField(max_length=50)
    name = CharField(max_length=120)
    image = ImageField(null=True, blank=True, upload_to=img_path)
    json = FileField(null=True, blank=True, upload_to=json_path)
    description = TextField(verbose_name="Description", max_length=1200, blank=True, null=True)
    attributes = JSONField(blank=True, default=list)
    uploaded_on = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Collection(Model):
    name = CharField(max_length=120)
    folder_name = CharField(max_length=50, blank=True, null=True)
    type = CharField(max_length=50)
    images = ManyToManyField(Image)
    pinata_img_hash = CharField(max_length=120, blank=True, null=True)
    pinata_json_hash = CharField(max_length=120, blank=True, null=True)
    created_on = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name