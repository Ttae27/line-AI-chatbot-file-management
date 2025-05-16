from pymongo import MongoClient
from langchain_core.tools import tool
import gridfs
from google_drive import upload_file_drive

conn_string = "mongodb://localhost:27017/"

def mongo_conn():
    try:
        conn = MongoClient("mongodb://localhost:27017/")
        return conn.historyDB
    except Exception as err:
        print(f"Error in connection : {err}")

db = mongo_conn()

fs = gridfs.GridFS(db, collection='files')

def get_files_data(group_id):
    query = db.files.files.find({"groupid": group_id})
    files_data = []
    for file_data in query:
        files_data.append(file_data)
    return files_data

def get_file_data(filename):
    query = db.files.files.find_one({"filename": filename})

    return query


def upload_file(file: bytearray, file_name: str, metadata: dict, fs):
    fs.put(file, filename=file_name, **metadata)

@tool
def download_file(filename: str, group_id: str):
    """
        Upload just one file from user query 

        Args:
        filename: name of file
    """
    data = db.files.files.find_one({"filename": filename, "groupid": group_id})
    fs_id = data['_id']
    out_data = fs.get(fs_id).read()
    file_id = upload_file_drive(bytearray(out_data), filename, data['about'], data['groupid'], data['userid'])
    if file_id:
        return "เซฟไฟล์เรียบร้อย"
    return 'error'

# out_data, file_path = download_file('Security Law.docx', db, fs)
# a = get_file_data(db)
# print(a)
def download_file_test(filename: str, group_id: str):
    """
        Upload just one file from user query 

        Args:
        filename: name of file
    """
    data = db.files.files.find_one({"filename": filename, "groupid": group_id})
    fs_id = data['_id']
    out_data = fs.get(fs_id).read()
    file_id = upload_file_drive(bytearray(out_data), filename, data['about'], data['groupid'], data['userid'])
    if file_id:
        return file_id
    return 'error'


# print(download_file_test("Security Law.docx", "Cdb64c7273beeb53116ca68976a25209f"))