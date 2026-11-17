import json
import mimetypes
import os
import sys
from io import BytesIO
from urllib.parse import quote
from urllib.request import urlopen

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

SOURCE = "https://wodqhghltahymlqqmczn.supabase.co"
TARGET_ENDPOINT = "https://mftblumpgqsqwdkzjpda.storage.supabase.co/storage/v1/s3"
BUCKET = "notices-techniques"
REGION = "eu-west-3"
MANIFEST = os.path.join(os.path.dirname(__file__), "notices_manifest_ESI_DEVIS.json")

def main():
    access_id = os.environ.get("ESI_PRO_S3_ACCESS_KEY_ID")
    secret = os.environ.get("ESI_PRO_S3_SECRET_ACCESS_KEY")
    if not access_id or not secret:
        sys.exit("ERREUR : ajouter les 2 secrets S3 dans GitHub Actions.")

    with open(MANIFEST, encoding="utf-8") as f:
        paths = json.load(f)
    if not paths:
        sys.exit("ERREUR : manifeste vide.")

    s3 = boto3.client(
        "s3",
        endpoint_url=TARGET_ENDPOINT,
        region_name=REGION,
        aws_access_key_id=access_id,
        aws_secret_access_key=secret,
        config=Config(s3={"addressing_style": "path"}, retries={"max_attempts": 3}),
    )

    success, skipped, failed = 0, 0, []
    for path in paths:
        url = f"{SOURCE}/storage/v1/object/public/{BUCKET}/{quote(path, safe='/')}"
        try:
            with urlopen(url, timeout=40) as response:
                content = response.read()
            if path.lower().endswith(".pdf") and not content.startswith(b"%PDF-"):
                raise ValueError("Le fichier telecharge n'est pas un PDF valide")
            if path.lower().endswith(".png") and not content.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("Le fichier telecharge n'est pas un PNG valide")
            if not content:
                raise ValueError("Fichier vide")

            try:
                existing = s3.head_object(Bucket=BUCKET, Key=path)
            except ClientError as e:
                if e.response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 404:
                    raise
            else:
                if existing["ContentLength"] != len(content):
                    raise ValueError("Fichier deja present, taille differente : aucun ecrasement")
                print(f"DEJA PRESENT : {path} ({len(content)} octets)")
                skipped += 1
                continue

            content_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
            s3.put_object(Bucket=BUCKET, Key=path, Body=BytesIO(content),
                          ContentType=content_type)
            uploaded = s3.head_object(Bucket=BUCKET, Key=path)
            if uploaded["ContentLength"] != len(content):
                raise ValueError("Taille du fichier distant differente")
            print(f"OK : {path} ({len(content)} octets)")
            success += 1
        except Exception as exc:
            print(f"ERREUR : {path} : {type(exc).__name__} - {exc}")
            failed.append(path)

    print(f"\nBILAN : {success} copies, {skipped} deja presents, {len(failed)} erreurs, {len(paths)} attendus")
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    main()
