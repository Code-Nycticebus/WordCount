#include <algorithm>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <vector>
#include <string_view>

int main(int argc, const char **argv) {
    std::unordered_map<std::string_view, int> occurences;
    std::vector<std::pair<std::string_view, int>> pairs;

    const char *path = argc < 2 ? __FILE__ : argv[1];
    std::ifstream file(path, std::ios::in | std::ios::binary);
    if (!file) throw std::runtime_error("Failed to open file");

    file.seekg(0, std::ios::end);
    size_t size = file.tellg();
    std::string c(size, '\0');
    file.seekg(0);
    file.read(c.data(), size);

    std::string_view content = c;
    size_t begin = 0;
    while (begin < content.size()) {
        while (begin < content.size() && std::isspace(static_cast<unsigned char>(content[begin]))) {
            ++begin;
        }

        size_t end = begin;
        while (end < content.size() && !std::isspace(static_cast<unsigned char>(content[end]))) {
            ++end;
        }

        if (begin < end) {
            std::string_view word = content.substr(begin, end - begin);
            int &idx = occurences[word];
            if (idx == 0) {
                pairs.emplace_back(std::pair(word, 1));
                idx = pairs.size();
            } else {
                pairs[idx - 1].second += 1;
            }
        }

        begin = end;
    }

    std::sort(pairs.begin(), pairs.end(), [](auto &a, auto &b) { return a.second > b.second; });

    for (int i = 0; i < 3; ++i) {
        const auto &p = pairs[i];
        std::cout << i + 1 << ": " << p.first << ": " << p.second << std::endl;
    }
}
