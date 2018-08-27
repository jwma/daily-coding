
# 聊聊缓存 分享一个Python缓存装饰器

## 什么是缓存，缓存作用
我可能会说：“把某个计算过程 P 的结果保存起来，如果下次需要知道计算过程 P 的结果，就直接从上次保存的数据中读取，这样就无需重复运行计算过程  P，节省获取结果的时间”。

表述很简单，或许是我认为这样理解缓存比较简单吧。虽然话很简单，但在实际使用缓存的时候，要考虑的事情并不是那么简单，或许看看下文，就会体会到我的意思了。

## 使用缓存
除了框架或者第三方库提供的缓存功能，相信大家大多数情况都是这样用缓存的：
```python
def get_articles():
    # 尝试获取缓存
    articles = cache.get('articles', None)
    if articles is None:
        # 如果没有缓存数据，就从数据库获取数据，然后把数据缓存起来并设置一个缓存有效期
        articles = Article.list()
        cache.set('articles', articles, 3600)  # 缓存articles数据一个小时
    return articles
```

或许有的童鞋会说，这样用缓存累不累呀？像 `Django` 这种框架，本身就提供了 `@cache_page` 这种方便的装饰器来对 `view` 进行缓存：
```python
@cache_page(3600)
def home(request):
    articles = services.article.get_articles()
    return JsonResponse({'articles': articles})
```

又或是 `drf-extensions` 提供的 `@cache_response`：
```python
class HomeView(views.APIView):

    @cache_response(3600)
    def get(self, request):
        articles = services.article.get_articles()
        return Response({'articles': articles})
```

的确，框架或者第三方库都有提供一些通用的缓存功能，但有时候我们需要对一些粒度比较小的结果进行缓存时，还是需要按照最开头的那个套路来做，但如果每个地方都要重复劳动，那的确比较麻烦，那造个轮子吧？什么样的轮子呢：
- 方便使用
- 函数级别的缓存

`Django` `cache_page` 也好， `drf-extensions` 的 `cache_response` 也好，都是针对 `view` 的，而我觉得，更通用的缓存还是针对函数来做比较合适。

在项目中，我们都会用分层思想来组织我们的代码，在业务逻辑层中，无论我们是直接在模块写函数还是通过封装类，我们的重点都是要实现业务逻辑，而函数，几乎是所有编写业务逻辑的场所，无论是纯函数，还是类的实例函数又或是类的静态函数，这些都是函数，我们如果能方便的针对函数进行缓存，那么我们就可以轻松控制缓存的粒度，再结合具体业务场景分析，更是可以提高缓存的命中率。

## 动手写一个
```python
import functools
import hashlib
import json
import inspect
import redis

connection = redis.StrictRedis(decode_responses=True)

def get_cache(key):
    return connection.get(key)

def set_cache(key, data, expires):
    connection.set(key, data, expires)

def default_key_func(method, *args, **kwargs):
    arg_dict = inspect.getcallargs(method, *args, **kwargs)
    arg_dict.update({
        '__qualname__': method.__qualname__,
        '__module__': method.__module__,
    })
    arg_dict.pop('self', None)
    arg_dict.pop('cls', None)
    return hashlib.md5(json.dumps(arg_dict, sort_keys=True).encode('utf-8')).hexdigest()

def func_cache(key_func=None, key_prefix=None, update_result_func=None, expires=30):
    """ 
    方法的cache 
    :param key_func: 生成cache_key的方法 
    :param key_prefix: 缓存的key前缀 
    :param update_result_func: 获取到缓存之后回调更新不需要缓存的字段 :param expires: 缓存过期时间，单位秒 
    :return: 
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = ''
  if callable(key_func):
                key = key_func(func, *args, **kwargs)
            if not key:
                key = default_key_func(func, *args, **kwargs)
            if key_prefix is not None:
                key = f'{key_prefix(func, *args, **kwargs)}:{key}' if callable(key_prefix) else f'{key_prefix}:{key}'
  cache_data = get_cache(key)
            if cache_data is not None:
                return cache_data if not callable(update_result_func) else update_result_func(cache_data)
            result = func(*args, **kwargs)
            set_cache(key, result, expires)
            return result

        return wrapper

    return decorator

if __name__ == '__main__':

    @func_cache()
    def get_article(limit):
        result = []
        for x in range(limit):
            result.append({'title': x})
        return result

    rs1 = get_article(10)
    print(rs1)

    rs1 = get_article(20)
    print(rs1)
```

大致浏览代码，会发现好像没什么特别，的确，整体的实现都不复杂，但我还是想说说其中的 `default_key_func` 的作用及实现。

众所周知，我们要获取某个缓存，都是通过 `key` 去获取的，而这个 `key` 的值具体是什么呢？试想一下，如果我们使用同一个 `key` 对某个函数进行缓存会发生什么问题：
- 如果函数逻辑不需要使用任何外界参数，则不存在任何问题；
- 如果函数逻辑的运行依赖外界的输入参数，而 `key` 永远都不变的话，就会发生返回结果与输入参数不匹配的问题。

也就是说，`key` 的值是依赖了函数的参数的，如果要做到自动计算 `key` 还需要确定函数的唯一性，如，不能把 A 模块的 `get_articles` 和 B 模块的 `get_articles` 当成同一个函数。

在自动计算 `key` 值时，需要根据函数及函数必要参数进行计算。在 `default_key_func` 中，使用了 `inspect` 模块，对需要缓存结果的函数进行了分析，传入函数，参数和关键字参数，生成了一个参数列表的字典，然后再加入函数本身的所在模块和限定名，这样就能确定 `key` 是依据具有特定参数的某个函数的调用而生成的。

`default_key_func` 中，还把函数的 `self` 和 `cls` 给排除了，我们已经可以通过上述的方式确定 `key` 和函数的关系了，这二者存在可以说是没意义的，如果我们不把这两个可能存在的参数从字典排除，还会影响 `key` 的唯一性（元凶是 `self`），因为 `self` 属于引用类型，是一个类实例的地址，虽然不同类实例可以调用同一个实例方法，但不同类实例所在的地址是不一样的，而这个地址会影响 `self` 字符串形式的值，所以如果不把其排除，则即使是同一个实例函数（输入参数一样）进行缓存，但 `key` 的值也会不一样，这就会造成重复缓存的生成。

`default_key_func` 是有缺陷的，如果要使用这个装饰器，就务必要知道这个缺陷，避免踩坑。缺陷就是缓存的函数不能存在有未重写 `__repr__` 的类的实例，且实现的 `__repr__` 必须返回不变的值。虽然说是坑，但其实理解了上面说的之后，会发现也不算是一个坑。

上文给出的代码，我是把缓存保存到 Redis 中去了，而你在使用时，可以自行实现 `get_cache` 和 `set_cache`。

## 多说一点点
需要使用缓存的地方，一般都有一些共同点：
- 热点数据；
- 被缓存的数据实时性一般要求不高；
- 产生需要被缓存的数据一般耗时较长，无论是计算导致的耗时还是网络IO导致的耗时。

缓存用不好可能更糟糕：
- 为命中率不高的数据设置缓存，单次请求后几乎不可能被再次访问到的数据，不但浪费首次查询、计算和设置缓存的时间，还占用缓存服务空间；
- 为原本就可以快速查询、计算的数据设置缓存，若缓存的数据本身可以快速得到，甚至比从缓存读取的速度还快，那无疑就是浪费；
- 缓存粒度没控制好，很容易造成命中率降低，一旦命中率降低，那么缓存的数据无疑就是无用的。

使用缓存时，一定要结合业务场景，分析出哪些是热点数据，什么样的粒度比较合适，缓存多久合适，总之不要盲目的使用缓存。

