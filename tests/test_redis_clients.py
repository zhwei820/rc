from rc.redis_cluster import RedisCluster


def test_redis_cluster_client_basic_operations(redis_hosts):
    cluster = RedisCluster(redis_hosts)
    client = cluster.get_client()

    keys = []
    for i in range(10):
        key = 'test key: %s' % i
        keys.append(key)
        client.set(key, i)
    for i, key in enumerate(keys):
        assert client.get(key) == bytes(str(i), encoding='utf-8')
    assert client.mget(keys) == [bytes(str(ii), encoding='utf-8') for ii in  range(10)]

    keys = []
    for i in range(10, 20):
        key = 'test key: %s' % i
        keys.append(key)
        client.setex(key, 100, i)
    for i, key in enumerate(keys, 10):
        assert client.get(key) == bytes(str(i), encoding='utf-8')
    assert client.mget(keys) == [bytes(str(ii), encoding='utf-8') for ii in  range(10, 20)]

    keys = []
    deleted_keys = []
    for i in range(20, 30):
        key = 'test key: %s' % i
        keys.append(key)
        client.setex(key, 100, i)
    for i in range(20, 25):
        key = 'test key: %s' % i
        deleted_keys.append(key)
        client.delete(key)
    for i, key in enumerate(keys[5:], 25):
        assert client.get(key) == bytes(str(i), encoding='utf-8')

    for key in deleted_keys:
        assert client.get(key) is None
    # assert client.mget(keys) == [None] * 5 + map(str, range(25, 30))
    res = [None for i in range(5)]
    res.extend([bytes(str(ii), encoding='utf-8') for ii in  range(25, 30)])

    assert client.mget(keys) == res

    keys = []
    mapping = {}
    deleted_keys = []
    for i in range(30, 40):
        key = 'test key: %s' % i
        mapping[key] = i
        keys.append(key)
    assert client.msetex(mapping, 100)
    for i, key in enumerate(keys, 30):
        assert client.get(key) == bytes(str(i), encoding='utf-8')

    assert client.mget(keys) == [bytes(str(ii), encoding='utf-8') for ii in  range(30, 40)]

    for i in range(30, 35):
        key = 'test key: %s' % i
        deleted_keys.append(key)
    assert client.mdelete(*deleted_keys)
    for i, key in enumerate(keys[5:], 35):
        assert client.get(key) == bytes(str(i), encoding='utf-8')

    for key in deleted_keys:
        assert client.get(key) is None
        res = [None for i in range(5)]
        res.extend([bytes(str(ii), encoding='utf-8') for ii in  range(35, 40)])

        assert client.mget(keys) == res
