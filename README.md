# A static UMP Scoped Registry generator (Unity Package manager)

Google ended support for their hosted scoped registry for the Unity Firebase packages. Currently, they only provide links to their `.tgz` files (https://developers.google.com/unity/archive) to be downloaded locally and added manually to your Unity Project.

This script generates a UMP repository with just static files which can easily be hosted on a CDN and require no dynamic application server (npm). Aimed to be used with the Firebase packages but this script would work also with any other Unity packages.

Tested with Unity 2021.1.2f1f.

## Limitations
 - Only support one version per package (support could easily be added, but I did not need it).
 - Files are actually NOT copied into the output. Just the JSON metafiles. The actual `.tgz` are assumed to be hosted somewhere else (but this could also be added).
 - Dependencies are not support (so if a package has them they must be installed manually).

## Usage
1. Download the `.tgz` packages in the version you need and place them in `./packages`.
2. Run 
   ```
   $ ./generate.py -p ./packages -u "https://dl.google.com/games/registry/unity/{package_name}/{package_name}-{package_version}.tgz"` -d output/
   ```
3. All files will be written to `./output`
4. Copy them to a CDN. They need to be served with `Content-Type: application/json`.


## Upload to public Google Storage bucket
```
$ gsutil mb -p <gcp_project> gs://<your-bucket-name>
$ gsutil defacl set public-read gs://<your-bucket-name>
$ gsutil -m -h "Content-Type:application/json" -h "Cache-Control: no-cache" rsync -r ./output gs://<your-bucket-name>/packages
```

Finally, you can use the bucket public url as Unity registry URL for your own Scoped Registry:
```
https://storage.googleapis.com/<your-bucket-name>/packages
```
