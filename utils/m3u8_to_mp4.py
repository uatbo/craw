import m3u8
import requests
import datetime
import os
from Crypto.Cipher import AES
from Crypto import Random
import glob

# Request header, not necessary, see website change
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}


def download(base_ts_url, ts_urls, download_path, keys=[]):
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    for i in range(len(ts_urls)):
        ts_url = base_ts_url + ts_urls[i].uri

        # 下载ts文件
        print("Start download %s" % ts_url)
        start_time = datetime.datetime.now().replace(microsecond=0)
        try:
            response = requests.get(ts_url, stream=True, verify=False)
        except Exception as e:
            print(e)
            return

        # ts文件的存储路径
        ts_path = download_path + "/{0}.ts".format(i)

        # 判断是否需要解密
        decrypt = True
        if len(keys) == 0 or keys[0] is None:  # m3u8 will get [None] if not key or []
            decrypt = False
        if decrypt:
            key = keys[i]
            iv = Random.new().read(AES.block_size)
            cryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC)

        with open(ts_path, "wb+") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    if decrypt:
                        file.write(cryptor.decrypt(chunk))
                    else:
                        file.write(chunk)

        end_time = datetime.datetime.now().replace(microsecond=0)
        print("Total time：%s" % (end_time - start_time))


def merge_to_mp4(dest_file, source_path, delete=False):
    with open(dest_file, 'wb') as fw:
        files = glob.glob(source_path + '/*.ts')
        for file in files:
            with open(file, 'rb') as fr:
                fw.write(fr.read())
                print(f'\r{file} Merged! Total:{len(files)}', end="     ")
            if delete:
                os.remove(file)

def m3u8_to_mp4(url, path_m3u8, path_mp4):
    video = m3u8.load(url)
    base_ts_url = url.rsplit("/", 1)
    download(base_ts_url, video.segments, path_m3u8, video.keys)
    merge_to_mp4('result.mp4', path_mp4)
    print("OK!")

if __name__ == "__main__":
    url = "https://r1-ndr.ykt.cbern.com.cn/edu_product/65/video/545602ec59b24cb9ab26f2266921e53d/ce0386e11f65e5eed429a8167255f835.852.480.false/ce0386e11f65e5eed429a8167255f835.852.480.m3u8"
    base_path = "../results/video"
    path_m3u8 = base_path + "/m3u8"
    path_mp4 = base_path + "/mp4"
    m3u8_to_mp4(url, path_m3u8=path_m3u8, path_mp4=path_mp4)