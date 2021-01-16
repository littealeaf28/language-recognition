import tarfile

raw_data_path = 'ja.tar'

# print('zh-CN.tar', tarfile.is_tarfile('zh-CN.tar'))

t = tarfile.open(raw_data_path, 'r')
t.extractall()
