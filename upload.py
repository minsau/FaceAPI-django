from azure.storage.blob import BlockBlobService, PublicAccess

block_blob_service = BlockBlobService(account_name='storage2ia', account_key='zYWmupNNK0F9RBZkrapMiiMuq9neJRcS44R3WTkJVeME45NTYxOoaENsN+Da5EUKd9Gcto9fG/Wh9zmzSyz0Ag==')
block_blob_service.create_container('verify', public_access=PublicAccess.Container)
