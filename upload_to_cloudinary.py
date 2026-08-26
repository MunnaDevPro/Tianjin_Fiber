"""
Upload all local media files to Cloudinary.
Run this ONCE from your project root:
    python upload_to_cloudinary.py
"""

import os
import sys
import cloudinary
import cloudinary.uploader

# --- Configure Cloudinary directly ---
cloudinary.config(
    cloud_name="dr6jg7a8z",
    api_key="667893846918177",
    api_secret="6QUDWNLmopkDLanNs03pVSTZFqI",
    secure=True,
)

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "media")

def upload_all():
    if not os.path.exists(MEDIA_ROOT):
        print(f"[ERROR] media/ folder not found at: {MEDIA_ROOT}")
        sys.exit(1)

    total = 0
    skipped = 0
    failed = 0

    for dirpath, dirnames, filenames in os.walk(MEDIA_ROOT):
        for filename in filenames:
            local_path = os.path.join(dirpath, filename)
            # Build the relative path to use as public_id in Cloudinary
            relative_path = os.path.relpath(local_path, MEDIA_ROOT)
            # Convert Windows backslashes to forward slashes
            public_id = relative_path.replace("\\", "/")
            # Remove file extension from public_id (Cloudinary adds it automatically)
            public_id_no_ext, ext = os.path.splitext(public_id)

            print(f"Uploading: {public_id} ...", end=" ", flush=True)
            try:
                result = cloudinary.uploader.upload(
                    local_path,
                    public_id=public_id_no_ext,
                    overwrite=False,          # skip if already exists
                    resource_type="auto",     # handles images and videos
                    use_filename=True,
                    unique_filename=False,
                )
                print(f"OK -> {result['secure_url']}")
                total += 1
            except cloudinary.exceptions.Error as e:
                err_str = str(e)
                if "already exists" in err_str.lower() or "public id" in err_str.lower():
                    print("SKIPPED (already exists)")
                    skipped += 1
                else:
                    print(f"FAILED: {e}")
                    failed += 1
            except Exception as e:
                print(f"FAILED: {e}")
                failed += 1

    print(f"\n--- Done ---")
    print(f"Uploaded : {total}")
    print(f"Skipped  : {skipped}")
    print(f"Failed   : {failed}")

if __name__ == "__main__":
    upload_all()
