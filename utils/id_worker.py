# 导入包
# https://github.com/yitter/IdGenerator
from id_generator import options, generator

# 声明id生成器参数，需要自己构建一个worker_id
options = options.IdGeneratorOptions(worker_id=23)
# 参数中，worker_id_bit_length 默认值6，支持的 worker_id 最大值为2^6-1，若 worker_id 超过64，可设置更大的 worker_id_bit_length
idgen = generator.DefaultIdGenerator()
# 保存参数
idgen.set_id_generator(options)
# 生成id
# uid = idgen.next_id()
# 打印出来查看
# print("%d, %x" % (uid, uid))
# print(f'{uid}')
