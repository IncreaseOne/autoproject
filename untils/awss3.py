# -*- coding: utf-8 -*-
# author：王勇
import json

import boto3
import logging
logger = logging.getLogger(__name__)
class S3():


    def __init__(self):
        self.BUCKET_NAME = "increaseone-webserver"  # 存储桶名称
        self.AWS_ACCESS_KEY_ID = 'AKIAWMVHTMA6UDTPJZ73'
        self.AWS_SECRET_ACCESS_KEY = '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'
        self.CN_REGION_NAME = 'us-west-2'  # 区域
        self.AWS_URL = "https://cloud.dealsgot.com"
        self.s3 = boto3.client('s3', region_name=self.CN_REGION_NAME,aws_access_key_id=self.AWS_ACCESS_KEY_ID, aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY)

    def upload_single_file(self, image, file_name):
        """
        上传单个文件
        :param src_local_path:
        :param file_name:
        :return:
        """
        try:
            self.s3.put_object(Body=image, Bucket=self.BUCKET_NAME, Key=file_name, ACL='public-read', ContentType="binary/image")
            logger.info(f"{self.AWS_URL}/{file_name}上传图片完成")
        except Exception as e:
            logger.info(f"{self.AWS_URL}/{file_name}上传图片失败")
            logger.error("{}: {}".format(file_name, e))
            return None
        return f"{self.AWS_URL}/{file_name}"
















