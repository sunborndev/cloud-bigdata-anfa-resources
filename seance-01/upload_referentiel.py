from pathlib import Path
import sys
import tempfile

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError


ENDPOINT_URL = "http://localhost:9000"
ACCESS_KEY = "anfa-app-key"
SECRET_KEY = "anfa-app-secret-2026"
BUCKET_NAME = "anfa-raw"

BASE_DIR = Path(__file__).resolve().parent
REFERENTIEL_DIR = BASE_DIR.parent / "data" / "referentiel"


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )


def check_bucket_access(s3_client):
    print(f"Verification de l'acces au bucket {BUCKET_NAME}...")
    s3_client.head_bucket(Bucket=BUCKET_NAME)
    print("Bucket accessible.")


def upload_csv_files(s3_client):
    csv_files = sorted(REFERENTIEL_DIR.glob("*.csv"))

    if not csv_files:
        print(f"Aucun fichier CSV trouve dans {REFERENTIEL_DIR}")
        sys.exit(1)

    print(f"Upload des fichiers depuis {REFERENTIEL_DIR}...")

    for csv_file in csv_files:
        line_count = count_lines(csv_file)
        object_key = f"referentiel/{csv_file.name}"
        s3_client.upload_file(
            str(csv_file),
            BUCKET_NAME,
            object_key,
            ExtraArgs={"ContentType": "text/csv"},
        )
        print(
            f"OK - {csv_file.name} ({line_count} lignes) "
            f"-> s3://{BUCKET_NAME}/{object_key}"
        )


def count_lines(csv_file):
    with csv_file.open("r", encoding="utf-8", errors="replace") as file:
        return sum(1 for _ in file)


def list_bucket_content(s3_client):
    print("\nContenu du bucket apres upload :")
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix="referentiel/")

    objects = response.get("Contents", [])
    if not objects:
        print("Aucun objet trouve.")
        return

    for obj in objects:
        print(f"- {obj['Key']} ({obj['Size']} octets)")


def download_and_show_sample(s3_client):
    object_key = "referentiel/lignes.csv"

    with tempfile.TemporaryDirectory() as temp_dir:
        local_file = Path(temp_dir) / "lignes.csv"
        s3_client.download_file(BUCKET_NAME, object_key, str(local_file))

        print(f"\nFichier telecharge depuis MinIO : s3://{BUCKET_NAME}/{object_key}")
        print("Contenu de lignes.csv :")
        print(local_file.read_text(encoding="utf-8", errors="replace").strip())


def main():
    s3_client = get_s3_client()

    try:
        check_bucket_access(s3_client)
        upload_csv_files(s3_client)
        list_bucket_content(s3_client)
        download_and_show_sample(s3_client)
    except ClientError as error:
        code = error.response.get("Error", {}).get("Code", "Unknown")
        message = error.response.get("Error", {}).get("Message", str(error))
        print(f"Erreur MinIO/S3 : {code} - {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
