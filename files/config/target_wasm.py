def run(proj_path, target_name, params):
    return {
        "project_name": "Sample",
        "build_types": ["Debug", "Release"],
        "archs": [
            {
                "arch": "wasm",
                "conan_arch": "wasm",
                "conan_profile": "ezored_wasm_profile",
            }
        ],
    }
