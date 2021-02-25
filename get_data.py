from azure.storage.blob import ContainerClient
from tqdm import tqdm
import os


account_url = 'https://osdg0public.blob.core.windows.net/'
sas = '?sv=2019-12-12&si=public-osdg-tool-policy&sr=c&sig=NubHWWDuafJc39VBbzJAfmyM2mseTXceN2bzTW%2Bbvmg%3D'
container_name = 'osdg-tool'

container = ContainerClient(account_url=account_url,
                            container_name=container_name,
                            credential=sas)

blob_names = []
blob_list = container.list_blobs()
for blob in blob_list:
    blob_names.append(blob.name)
print(blob_names[0:5])

directory = "./data/"
if not os.path.exists(directory):
    os.makedirs(directory)

for blob_name in tqdm(blob_names):
    blob = container.get_blob_client(blob_name)
    with open(directory + blob_name, "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)

