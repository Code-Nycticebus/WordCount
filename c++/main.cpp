#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <unordered_map>
#include <vector>

int main(int argc, const char **argv) {
  std::unordered_map<std::string, int> occurences;
  std::vector<std::pair<std::string, int>> pairs;

  std::ifstream ifs(argc < 2 ? __FILE__ : argv[1]);
  std::string text = std::string((std::istreambuf_iterator<char>(ifs)),
                                 (std::istreambuf_iterator<char>()));

  std::istringstream iss(text);

  while (iss) {
    std::string sub;
    iss >> sub;
    int &idx = occurences[sub];
    if (idx == 0) {
      idx = pairs.size() + 1;
      pairs.push_back(std::pair(sub, 1));
    } else {
      pairs[idx - 1].second += 1;
    }
  }

  std::sort(pairs.begin(), pairs.end(),
            [](auto &a, auto &b) { return a.second > b.second; });

  for (int i = 0; i < 3; ++i) {
    const auto &p = pairs[i];
    std::cout << i + 1 << ": " << p.first << ": " << p.second << std::endl;
  }
}
