# 对知识星球中的文章进行下载

需要准备几个库

```
pip install re
pip install requests
pip install json
pip install BeautifulSoup
```

三个参数，例如

 ```
 group_id = '288881224841'
 user_id = '4158415242588'
 access_token = '4FE0F424-8AED-4F04-A8C8-FC58D5804C2A_33DEA2472F68523D'
 ```

若干个url，例如

```
https://api.zsxq.com/v2/groups/288881224841/topics?scope=all&count=20
https://api.zsxq.com/v2/groups/288881224841/topics?scope=all&count=20&end_time=2024-12-13T19%3A01%3A40.900%2B0800
https://api.zsxq.com/v2/groups/288881224841/topics?scope=all&count=20&end_time=2024-12-17T14%3A54%3A21.852%2B0800
```



参数从F12中获取，group_id为纯数字。如果出现空白，则按下键盘的F5按钮刷新页面。

![image-20250511210330964](C:/Users/90674/AppData/Roaming/Typora/typora-user-images/image-20250511210330964.png)



同理，url获取也是如此

但需要注意的是，这里的url由于知识星球的限制，一个url只能获取到部分的文章内容。需要将所有url都集齐，才能下载完成所有文章。

url可以通过

1.先打开F12，然后在左侧知识星球页面下滑直到底部

2.可看见新的网络请求包，此时将其url全部复制，如果右侧预览如2中一样，则就是此项为应该复制的url，格式为如下两种

```
https://api.zsxq.com/v2/groups/28888122422841/topics?scope=all&count=20
```

```
https://api.zsxq.com/v2/groups/28888122422841/topics?scope=all&count=20&end_time=2024-12-17T14%3A54%3A21.852%2B0800
```

![image-20250511210825166](C:/Users/90674/AppData/Roaming/Typora/typora-user-images/image-20250511210825166.png)

分批次复制到py文件中，修改api_url的值，运行即可。这里可以直接改一下后面的end_time的值

![image-20250511211108736](C:/Users/90674/AppData/Roaming/Typora/typora-user-images/image-20250511211108736.png)

然后直接运行就行