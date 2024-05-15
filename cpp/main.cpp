#include <algorithm>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <vector>

int main(int argc, const char **argv) {
  std::unordered_map<std::string, int> occurences;
  std::vector<std::pair<std::string, int>> pairs;

  const char *file = argc < 2 ? __FILE__ : argv[1];
  std::ifstream ifs(file);
  if (!ifs) {
    std::cerr << "Failed to open file: " << file << std::endl;
    return 1;
  }

  std::string word;
  while (ifs >> word) {
    int &idx = occurences[word];
    if (idx == 0) {
      pairs.emplace_back(std::pair(word, 1));
      idx = pairs.size();
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
