# Crawl_instagram_img

首先抱歉一开始在官方文档阅读时没有仔细，没有看到examples里的instagram，
于是自己先通过python进行尝试，查阅了一些相关的文档后，结合自己在ins上的观察发现
以前通过动态传输的windowsData里的displayurl经过了处理，而且需要登录才能进行图片继续加载，所以就想到了用selenum模拟浏览器操作进行爬取
首先是python是基于requests模块，采用的proxy也是socks5,需要在proxies设置一下本地的地址和ssr的本地端口号，然后Chromedriver插件，我的是7.6版本的，需要和自己的Chrome版本对应
将Chromedriver.exe和crawl_ins_byPython.py放在同一目录下，运行crawl_ins_byPython.py即可，首先是ins登录，然后在浏览器输入博主对应的insAccount地址，
之后会自动滑动窗口请求图片地址，项目介于测试，设置了大于500停止，注释掉就可以爬取完主页面所有图片，会在跟目下生成imgp文件夹，图片存入里面

然后在昨天重新看gocolly框架时，在github发现了instagram的案例，但是在测试中，首先是源码在定义结构体mainPageData中有一个`json::node"`语法错误，
问题不大，修改为`json:"node"`即可，然后也需要加proxy代理，同样采用ssr，需要导入"github.com/gocolly/colly/proxy"，同时在main中收集器创建好后加入
if p,err := proxy.RoundRobinProxySwitcher(
		"socks5://127.0.0.1:1080",
	);err == nil {
        c.SetProxyFunc(p)
    }
和python中socks5的设置类似
在运行中会报一个错，在正则匹配的一行中，index超出范围，后来打印出看，并没有匹配到内容，卡在这一步，这一步应该是访问首页后，调用OnHTML后，以OnResponse处理，
会匹配一个二进制数据，存放的应该是query_hash下一页时需要的id，但具体在二进制中的位置因为能力不足并不清楚，所以未能用该框架获取到数据
   
