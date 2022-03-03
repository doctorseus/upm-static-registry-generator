import os
import json
import tarfile
import hashlib
import mmap
import argparse


def sha1sum(file):
    func = hashlib.sha1()
    with open(file, 'rb') as f:
        with mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ) as mm:
            func.update(mm)
    return func.hexdigest()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--packages', '-p', metavar='DIR', help='specify packages input directory', required=True)
    parser.add_argument('--url', '-u', help='specify tar archive address', required=True)
    parser.add_argument('--output', '-d', metavar='DIR', default='output/', help='specify output directory (default: output/)')
    args = parser.parse_args()

    packages_path = args.packages
    output_path = args.output

    # create output path
    os.makedirs(output_path, exist_ok=True)

    # find all packages
    package_files = [os.path.join(packages_path, f)
                     for f in os.listdir(packages_path)
                     if os.path.isfile(os.path.join(packages_path, f)) and os.path.splitext(f)[1] == '.tgz']

    print('Packages found: ')

    packages = []
    for package_file in package_files:
        print(package_file)

        package_archive = tarfile.open(package_file, "r:gz")
        for archive_member in package_archive.getmembers():
            if archive_member.isfile() and os.path.basename(archive_member.name) == 'package.json':
                package_json_file = package_archive.extractfile(archive_member)
                if package_json_file:
                    package_json_content = package_json_file.read()
                    package_json = json.loads(package_json_content)

                    packages.append((package_file, package_json))

    search_objects = []

    print('Generate:')

    for (package_file, package_json) in packages:
        # print(package_json)
        package_name = package_json['name']
        package_version = package_json['version']

        search_object = {
            "package": {
                "name": package_name,
                "displayName": package_json['displayName'],
                "description": package_json['description'],
                "dist-tags": {
                    "latest": package_version
                },
                "maintainers": [
                ],
                "author": package_json['author'],
                "readmeFilename": "README.md",
                "time": {
                    "modified": "2022-02-17T22:08:13.584Z"
                },
                "versions": {
                    package_version: "latest"
                }
            },
            "flags": {},
            "local": True,
            "score": {
                "final": 1,
                "detail": {
                    "quality": 1,
                    "popularity": 1,
                    "maintenance": 0
                }
            },
            "searchScore": 100000
        }

        search_objects.append(search_object)

        # generate package json
        tar_url = args.url\
            .replace('{package_name}', package_name)\
            .replace('{package_version}', package_version)

        package_content = {
            "name": package_name,
            "versions": {
                package_version: {
                    "name": package_name,
                    "displayName": package_json['displayName'],
                    "description": package_json['description'],
                    "version": package_version,
                    "unity": package_json['unity'],
                    "author": package_json['author'],
                    "dependencies": {
                    },
                    "publishConfig": {
                        "registry": "https://example.com"
                    },
                    "readmeFilename": "README.md",
                    "maintainers": [
                    ],
                    "dist": {
                        "integrity": None,  # ignore
                        "shasum": sha1sum(package_file),
                        "tarball": "https://dl.google.com/games/registry/unity/" + package_name + "/" + package_name + "-" + package_version + ".tgz"
                    },
                    "contributors": []
                }
            },
            "time": {
                "modified": "2022-02-17T21:43:58.917Z",
                "created": "2021-08-11T23:12:38.284Z",
                package_version: "2022-02-17T21:43:58.917Z"
            },
            "users": {},
            "dist-tags": {
                "latest": package_version,
            },
            "readme": "Empty",
        }

        print('- %s' % package_name)
        print('  > sha1=%s' % sha1sum(package_file))
        print('  > url=%s' % tar_url)
        with open(output_path + '/' + package_name, 'w') as f:
            json.dump(package_content, f)

    # generate /-/v1/search file
    os.makedirs(output_path + '/-/v1/', exist_ok=True)
    search_content = {
        "objects": search_objects,
        "total": len(search_objects),
        "time": "Thu, 03 Mar 2022 19:54:18 GMT"
    }
    with open(output_path + '/-/v1/' + 'search', 'w') as f:
        json.dump(search_content, f)
