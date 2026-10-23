# 工作原理

关于这个项目的产生想法具体可见 `README.md`。本文将讲述该项目的工作流程。

## 项目结构

关于项目的目录结构，可以查看 [Structure.md](./Structure.md)。本项目遵循 EDD (Event driven development) (事件驱动开发) 设计模式。

### 服务端
使用 python 开发，
* `utils/` 中包含所有百度网盘 API 的调用，完成授权，获取链接，下载等等。
* `transfer/` 中是别人的项目 (具体来源可见 [transfer/README.md](./src/transfer/README.md))，用于自动转存分享链接中的文件。
* `event_handler/` 中定义了各种事件 (event)，以及每种事件对应的事件处理器 (event_handler)，并且定义了一个事件巴士 (`event_bus`)，用于接受事件和将事件分配到对应的处理器。
* `api/` 中定义了一个 http 服务器，用于接受客户端中发送的分享链接，同时激发事件进行各种转存，提取链接操作。
* `token/` 中保存了各种所需的 `AppKey`, `access_token`, `cookie` 等等凭证。
* `user_links/` 中保存了每个用户提取码对应的 txt 文件，每个文件中保存了分享链接中的所有文件，文件路径以及一个 `access_token`。

### 客户端
由于 python 需要在一定环境中运行，不方便使用。此处使用 cpp 实现客户端。由于作者很懒，懒得写流式下载大文件等等逻辑，所以直接在可执行文件的工作目录中放一个 curl 软件 (Windows 里是 `curl.exe`)，直接调用 curl 来进行下载。

## 工作逻辑 (这不是使用文档，只关注大致过程)

假设 Alice 有一个 SVIP 账号需要共享。

1. 首先，Alice 需要自己在百度网盘开放平台中申请自己的应用并通过认证。
2. 然后，Alice 需要将应用的一些 `Appkey`, `Scretekey`, `AppID` 等等存入 `token/` 中。随后运行 `utils` 中的相关函数，这些函数会自动获取 `access_token` 并且保存在相应文件中。Alice 还需要浏览器登录百度网盘主页获取 `cookie`，并将其手动保存在相应文件中。
3. 随后，Alice 启动服务器 (也就是运行 `api/page.py`)，这时程序会启动一个服务器，并且能够在局域网内被其他计算机访问。
4. 这时候 Bob 恰好获得了一个分享链接，分享链接中有一堆文件夹和文件，还需要下载这些文件。
5. Bob 首先需要在自己的计算机里面存放 `cpp/` 里面的所有内容。
6. 于是 Bob 登录 Alice 的服务器提交分享链接和提取码，并且输入一个自定义用户提取码。然后 Alice 的服务器将会自动在 `apps/应用名/一个文件夹/` 中创建一个文件夹，名称为：自定义用户提取码。随后服务器转存链接中的所有文件夹和文件。
7. 随后，Alice 在 `user_links/` 中创建 `自定义用户提取码.txt`。并在里面写入 `access_token`，提取的 `dlinks`，以及文件在网盘中的实际路径。
8. 这些过程 Bob 是不知道的。等待一段时间后 (或者 Bob 收到页面通知知道转存已经完成)，Bob 启动可执行文件 `cpp/main` (Windows 上是 `cpp/main.exe`)。然后填写自定义用户提取码。随后，`main` (或者 `main.exe`) 会自动获取 `user_links/` 中的 `links`, 完成文件下载。
