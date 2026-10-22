#pragma once

#include <curl/curl.h>
#include <string>
#include <vector>

// libcurl 写入响应数据的回调函数
static size_t http_write_callback(
    char* ptr,
    size_t size,
    size_t nmemb,
    void* userdata)
{
    const size_t total = size * nmemb;
    auto* response = static_cast<std::string*>(userdata);

    response->append(ptr, total);
    return total;
}

// GET 请求，将响应文本按行分割
// 成功返回 true，失败返回 false
inline bool http_get_lines(
    const std::string& host,
    const std::string& path,
    std::vector<std::string>& lines)
{
    lines.clear();

    CURL* curl = curl_easy_init();
    if (!curl) {
        return false;
    }

    std::string response;

    // 拼接 URL
    std::string url = host + path;

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

    // 连接超时：5 秒
    curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, 5L);

    // 总请求超时：10 秒
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L);

    // 接收响应正文
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, http_write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

    // 跟随 HTTP 重定向（可按需删除）
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

    // 执行 GET 请求
    CURLcode res = curl_easy_perform(curl);

    long status_code = 0;
    if (res == CURLE_OK) {
        curl_easy_getinfo(
            curl,
            CURLINFO_RESPONSE_CODE,
            &status_code);
    }

    curl_easy_cleanup(curl);

    // 请求失败或 HTTP 状态码不是 200
    if (res != CURLE_OK || status_code != 200) {
        return false;
    }

    // 按行分割响应正文
    size_t start = 0;

    while (start < response.size()) {
        size_t end = response.find('\n', start);

        if (end == std::string::npos) {
            end = response.size();
        }

        size_t len = end - start;

        // 兼容 Windows 风格的 \r\n
        if (len > 0 && response[start + len - 1] == '\r') {
            --len;
        }

        lines.emplace_back(response.substr(start, len));

        if (end == response.size()) {
            break;
        }

        start = end + 1;
    }

    return true;
}
