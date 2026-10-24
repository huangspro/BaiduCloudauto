#include <iostream>
#include <string>
#include <cstdlib>
#include <filesystem>
#include <vector>
#include <fstream>
#include <system_error>



bool get_links(const std::string& host, const std::string& to_extract_code)
{
    std::string cmd =
        "./curl -sS -X POST \"" + host + "/download\" "
        + std::string(R"(-d "to_extract_code=)")
        + to_extract_code
        + R"(" -H "Content-Type: application/x-www-form-urlencoded" )"
        + R"(-o ")"
        + to_extract_code
        + R"(.txt")";

    int ret = std::system(cmd.c_str());

    return ret == 0;
}

// The format of the file
/*
* access_token (1 line)
* dlink (1 line)
* file path (1 line)
* dlink (1 line)
* file path (1 line)
* dlink (1 line)
* file path (1 line)
* ...
*/
std::vector<std::string> readFileLines(const std::string& filename)
{
    std::vector<std::string> lines;
    std::ifstream file(filename);
    std::string line;

    if (!file.is_open()) {
        std::cerr << "文件打开失败: " << filename << std::endl;
        return lines;
    }

    while (std::getline(file, line)) {
        lines.push_back(line);
    }

    return lines;
}

bool download_file(const std::string& access_token,
                   const std::string& dlink,
                   const std::string& path)
{
    namespace fs = std::filesystem;

    // Create parent directories if needed.
    std::error_code ec;
    fs::path output_path(path);

    if (output_path.has_parent_path())
    {
        fs::create_directories(output_path.parent_path(), ec);
        if (ec)
            return false;
    }

    std::string cmd =
        "./curl"
        " -L"
        " -f"
        " --max-time 60"
        " -G"
        " --data-urlencode \"access_token=" + access_token + "\""
        " -H \"User-Agent: pan.baidu.com\""
        " -o \"" + path + "\""
        " \"" + dlink + "\"";

    int ret = std::system(cmd.c_str());

    if (ret != 0)
    {
        fs::remove(output_path, ec);
        return false;
    }

    return true;
}



int main()
{
    std::string host;
    std::cout<<"请输入服务器host（例如 http://127.0.0.1:5000）"<<std::endl;
    std::getline(std::cin, host);
    while (!host.empty() && host.back() == '/') host.pop_back();
    std::cout<<"请浏览器访问: "<<host<<"/apply "<<"，提交分享链接和自定义提取码，等待分享链接处理完成后，再进行下一步"<<std::endl;
    
    std::cout<<"请输入提取码，注意如果分享链接还没有处理完成，下一步将失败"<<std::endl;
    std::string to_extract_code;
    std::cin>>to_extract_code;


    if(!get_links(host, to_extract_code)){
        std::cout<<"无法获取提取码"<<std::endl;
        return 1;
    }
    
    int failed=0, success=0;
    
    std::vector<std::string> download_info = readFileLines(to_extract_code + ".txt");
    if(download_info.size()%2 == 1 || download_info.size()==0){
        std::cout<<"无法获取提取码"<<std::endl;
        return 1;
    }
    for(int i=1;i<=download_info.size()-2;i+=2){
      if(download_file(download_info[0], download_info[i], download_info[i+1])){
          std::cout<<download_info[i+1] + "下载完成"<<std::endl;
          success++;
      }
      else {
          failed++;
          std::cout<<download_info[i+1] + "下载失败"<<std::endl;
      }
    }
    int total = failed + success;
    std::cout<<"总共：" + std::to_string(total) + "| 成功下载：" + std::to_string(success) + "| 下载失败：" + std::to_string(failed) <<std::endl;
}
