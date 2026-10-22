#pragma once

#include <curl/curl.h>

#include <iostream>
#include <string>

// 将响应数据直接写入文件
static size_t download_write_callback(
    char* data,
    size_t size,
    size_t nmemb,
    void* userdata)
{
    FILE* fp = static_cast<FILE*>(userdata);

    if (size != 0 && nmemb > static_cast<size_t>(-1) / size) {
        return 0;
    }

    const size_t len = size * nmemb;
    return fwrite(data, 1, len, fp);
}

// GET 下载文件
// 成功返回 true，失败返回 false
inline bool download_file(
    std::string token,
    const std::string& dlink)
{
    // 简单检查 HTTPS 协议
    if (dlink.compare(0, 8, "https://") != 0) {
        return false;
    }
std::cout<<"ok"<<std::endl;
    // 分离 URL 中的 fragment，fragment 不会发送给服务器
    std::string url = dlink;
    const size_t fragment_pos = url.find('#');

    if (fragment_pos != std::string::npos) {
        url.resize(fragment_pos);
    }

    // 追加 access_token
    url += (url.find('?') == std::string::npos ? "?" : "&");
    url += "access_token=" + token;

    const std::string filename = "download";

    FILE* fp = fopen(filename.c_str(), "wb");
    if (!fp) {
        return false;
    }

    CURL* curl = curl_easy_init();
    if (!curl) {
        fclose(fp);
        return false;
    }
    
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

    // 请求头
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "User-Agent: pan.baidu.com");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    // 连接超时与总请求超时：300 秒
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, 300L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 300L);

    // 跟随重定向
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_MAXREDIRS, 10L);

    // 限制协议为 HTTPS，防止重定向到非 HTTPS 地址
    curl_easy_setopt(curl, CURLOPT_PROTOCOLS_STR, "https");
    curl_easy_setopt(curl, CURLOPT_REDIR_PROTOCOLS_STR, "https");

    // 流式写入文件
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, download_write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);

    // 执行请求
    CURLcode result = curl_easy_perform(curl);

    long status_code = 0;
    if (result == CURLE_OK) {
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &status_code);
    }

    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
    fclose(fp);

    return result == CURLE_OK && status_code == 200;
}
