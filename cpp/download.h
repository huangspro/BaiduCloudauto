#include "httplib.h"
#include <cstdio>
#include <string>

bool download_file(std::string token, const std::string& dlink) {
    // 假设 dlink 是完整的 HTTP URL
    auto url = httplib::detail::parse_url(dlink);
    if (!url) return false;

    httplib::Client cli(url->scheme + "://" + url->authority);
    cli.set_connection_timeout(300, 0);
    cli.set_read_timeout(300, 0);

    std::string path = url->path.empty() ? "/" : url->path;
    if (!url->query.empty()) path += "?" + url->query;
    path += (path.find('?') == std::string::npos ? "?" : "&");
    path += "access_token=" + httplib::detail::encode_query_param(token);

    std::string filename = path.substr(path.find_last_of('/') + 1);
    filename = filename.substr(0, filename.find('?'));
    if (filename.empty()) filename = "download";

    FILE* fp = fopen(filename.c_str(), "wb");
    if (!fp) return false;

    auto res = cli.Get(path, {{"User-Agent", "pan.baidu.com"}},
        [&](const char* data, size_t len) {
            return fwrite(data, 1, len, fp) == len;
        });

    fclose(fp);
    return res && res->status == 200;
}