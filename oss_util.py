import oss2

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth('', '')

# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-beijing.aliyuncs.com。
endpoint = ''
bucket_name = ''

# 填写Bucket名称。
bucket = oss2.Bucket(auth, endpoint, bucket_name)


def upload(uuid, src_path) -> bool:
    resp = bucket.put_object_from_file(uuid, src_path).resp.status
    return resp == 200


if __name__ == '__main__':
    print(upload("test-o.png", "test-o.png"))
