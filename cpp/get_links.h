#include "httplib.h"
#include <string>
#include <vector>

// GET 请求，将响应文本按行分割
// 成功返回 true，失败返回 false
bool http_get_lines(
    const std::string& host,
    const std::string& path,
    std::vector<std::string>& lines)
{
    lines.clear();

    httplib::Client cli(host);
    cli.set_connection_timeout(5, 0);
    cli.set_read_timeout(10, 0);

    auto res = cli.Get(path);

    if (!res || res->status != 200) {
        return false;
    }

    const std::string& text = res->body;
    size_t start = 0;

    while (start < text.size()) {
        size_t end = text.find('\n', start);

        if (end == std::string::npos) {
            end = text.size();
        }

        size_t len = end - start;

        // 兼容 Windows 风格的 \r\n
        if (len > 0 && text[start + len - 1] == '\r') {
            --len;
        }

        lines.emplace_back(text.substr(start, len));

        if (end == text.size()) {
            break;
        }

        start = end + 1;
    }

    return true;
}