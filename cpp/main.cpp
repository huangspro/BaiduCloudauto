#include <iostream>
#include <string>

#include "download.h"
#include "get_links.h"


int main(){
  std::cout << download_file("https://d.pcs.baidu.com/file/6cb06943bl9042fb4e1affebf994a738?fid=1103781937522-250528-901185618239706&rt=pr&sign=FDtAERK-DCb740ccc5511e5e8fedcff06b081203-jYGOfnPGsyQj1mIwG5VY4F8Oeyo%3D&expires=8h&chkbd=0&chkv=0&dp-logid=115302435783167661&dp-callid=0&dstime=1792119201&r=527080331&vuk=1103781937522&origin_appid=124475457&file_type=0", "121.945c5aca809f27d1c5fb4cfeb091e776.Y_vxwfyjACAUfiT8l9cR9fwPup4HQKcZEq6qruY.NPoV_A");
}
