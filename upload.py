from azure.storage.file import FileService

file_service = FileService(account_name='storage2ia', account_key='zYWmupNNK0F9RBZkrapMiiMuq9neJRcS44R3WTkJVeME45NTYxOoaENsN+Da5EUKd9Gcto9fG/Wh9zmzSyz0Ag==')
file_service.create_share('myshare')