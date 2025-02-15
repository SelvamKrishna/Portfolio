#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;
#define ROOT ".versions"

bool CheckInit() {
  return fs::exists(ROOT) && fs::is_directory(ROOT);
}

int Initialize() {
  if (CheckInit()) {
    std::cout << '<' << ROOT << "> directory already exists." << std::endl;
    return EXIT_FAILURE;
  }

  if (!fs::create_directory(ROOT)) {
    std::cout << "Unable to create directory <" << ROOT << ">" << std::endl;
    return EXIT_FAILURE;
  } 
  
  std::cout << "Created Directory <" << ROOT << ">" << std::endl;
  return EXIT_SUCCESS;
}

int Commit(std::string commitName) {
  if (!CheckInit()) {
    std::cout << "Project is not initialized yet <./lily init>" << std::endl;
    return EXIT_FAILURE;
  }

  fs::path source = fs::current_path();
  fs::path dest = source / ROOT / commitName;
    
  if (fs::exists(dest)) {
    std::cout << "Commit already exist. Won't overwrite commit." << std::endl;
    return EXIT_FAILURE;
  }

  try {
    fs::create_directory(dest);
    for (const auto& entry : fs::directory_iterator(source)) {
      const auto& path = entry.path();
      if (path != source / ROOT) {
        if (path.filename() == "lily.exe") continue;
        fs::copy(path, dest / path.filename(), fs::copy_options::recursive | fs::copy_options::overwrite_existing);
        std::cout << "Copied <" << path.filename() << ">\n";
      }
    }
  } catch (const fs::filesystem_error &e) {
    std::cout << "Err: " << e.what() << std::endl;
    return EXIT_FAILURE;
  }
  
  std::cout << "Created Commit <" << commitName << ">" << std::endl;
  return EXIT_SUCCESS;
}

int main(int argc, char const *argv[]) {
  if (argc < 2) {
    std::cout << "Not enough arguments provided" << std::endl;
    return EXIT_FAILURE;
  }

  const std::string command = argv[1];

  if (command == "init") return Initialize();
  if (command == "commit") {
    if (argc < 3) {
      std::cout << "Requires a commit message <./lily commit sample-name>" << std::endl;
      return EXIT_FAILURE;
    }

    return Commit(std::string(argv[2]));
  }

  return EXIT_SUCCESS;
}