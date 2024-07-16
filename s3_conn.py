import os
import time
import boto3
from io import BytesIO
# from rag import settings
# from rag.settings import minio_logger
# from rag.utils import singleton


@singleton
class HuS3(object):
    def __init__(self):
        self.conn = None
        self.__open__()

    def __open__(self):
        try:
            if self.conn:
                self.__close__()
        except Exception as e:
            pass

        try:
            self.conn = boto3.client(
                            's3',
                            aws_access_key_id = settings.S3["access_key"],
                            aws_secret_access_key = settings.S3["secret_key"],
                            endpoint_url = settings.S3["host"]
                            )
        except Exception as e:
            minio_logger.error(
                "Fail to connect %s " % settings.S3["host"] + str(e))

    def __close__(self):
        del self.conn
        self.conn = None

    def put(self, bucket, fnm, binary):
        for _ in range(10):
            try:
                self.conn.upload_fileobj(BytesIO(binary), settings.S3["bucket"], bucket+"/"+ fnm)
                return "Upload successful"
            except Exception as e:
                minio_logger.error(f"Fail put {bucket}/{fnm}: " + str(e))
                self.__open__()
                time.sleep(1)

    def rm(self, bucket, fnm):
        try:
            self.conn.delete_object(Bucket=settings.S3["bucket"], Key=bucket+"/"+fnm)
        except Exception as e:
            minio_logger.error(f"Fail rm {bucket}/{fnm}: " + str(e))


    def get(self, bucket, fnm):
        for _ in range(1):
            try:
                response = self.conn.get_object(Bucket=settings.S3["bucket"], Key= bucket+"/"+ fnm)
                return response['Body'].read()
            except Exception as e:
                minio_logger.error(f"fail get {bucket}/{fnm}: " + str(e))
                self.__open__()
                time.sleep(1)
        return

    def obj_exist(self, bucket, fnm):
        try:
            self.conn.head_object(Bucket=settings.S3["bucket"], Key= bucket+"/"+ fnm)
            return True
        except Exception as e:
            minio_logger.error(f"Fail put {bucket}/{fnm}: " + str(e))
        return False


    def get_presigned_url(self, bucket, fnm, expires):
        for _ in range(10):
            try:
                url = self.conn.generate_presigned_url('get_object', Params={'Bucket': settings.S3["bucket"], 'Key':  bucket+"/"+ fnm},
                                                       ExpiresIn=expires)
                return url
            except Exception as e:
                minio_logger.error(f"fail get {bucket}/{fnm}: " + str(e))
                self.__open__()
                time.sleep(1)
        return

MINIO = HuS3()

if __name__ == "__main__":
    conn = HuS3()
    fnm = r"C:\Users\Administrator\Pictures\企业微信截图_17125441604851.png"
    ifExist = conn.obj_exist("", "S3.xml")
    print(ifExist)
    from PIL import Image
    img = Image.open(fnm).convert('RGB')
    buff = BytesIO()
    img.save(buff, format='JPEG')
    print(conn.put("test", "11-408.jpg", buff.getvalue()))
    bts = conn.get("test", "11-408.jpg")
    img = Image.open(BytesIO(bts))
    img.save("test.jpg")
