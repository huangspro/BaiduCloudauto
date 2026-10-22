#include <iostream>
#include <string>
#include <cstdlib>
#include <filesystem>
#include <vector>
#include <fstream>

bool get_links(const std::string& to_extract_code)
{
    std::string cmd =
        R"(./curl -sS -X POST "http://127.0.0.1:5000/download" )"
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



bool download_file(std::string access_token, const std::string& dlink, std::string path)
{
    namespace fs = std::filesystem;
    std::string filename = "download";

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
        std::error_code ec;
        fs::remove(filename, ec);
        return false;
    }

    return true;
}


int main()
{
    std::cout<<"请输入提取码"<<std::endl;
    std::string to_extract_code;
    std::cin>>to_extract_code;
    if(!get_links(to_extract_code)){
        std::cout<<"无法获取提取码"<<std::endl;
        return 1;
    }
    
    int failed=0, success=0;
    
    std::vector<std::string> download_info = readFileLines(to_extract_code + ".txt");
    for(int i=1;i<=download_info.size();i+=2){
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
