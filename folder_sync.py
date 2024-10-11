import os
import shutil
import time
import argparse
import logging
import hashlib

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def compute_file_hash(file_path):
    """Compute MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(source, replica):
    """Synchronize source folder to replica folder."""
    for dirpath, _, filenames in os.walk(source):
        # Compute the relative path for the replica
        relative_path = os.path.relpath(dirpath, source)
        replica_dir = os.path.join(replica, relative_path)

        # Create directories in the replica if they don't exist
        if not os.path.exists(replica_dir):
            os.makedirs(replica_dir)

        for filename in filenames:
            source_file_path = os.path.join(dirpath, filename)
            replica_file_path = os.path.join(replica_dir, filename)

            # Copy new and updated files from source to replica
            if not os.path.exists(replica_file_path) or \
               compute_file_hash(source_file_path) != compute_file_hash(replica_file_path):
                shutil.copy2(source_file_path, replica_file_path)
                logging.info(f"Copied: {source_file_path} to {replica_file_path}")
                print(f"Copied: {source_file_path} to {replica_file_path}")

    # Remove files that are no longer in the source
    for dirpath, _, filenames in os.walk(replica):
        for filename in filenames:
            replica_file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(dirpath, replica)
            source_file_path = os.path.join(source, relative_path, filename)

            if not os.path.exists(source_file_path):
                os.remove(replica_file_path)
                logging.info(f"Removed: {replica_file_path}")
                print(f"Removed: {replica_file_path}")

def main(source, replica, interval, log_file):
    setup_logging(log_file)
    while True:
        sync_folders(source, replica)
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Path to the source folder.")
    parser.add_argument("replica", help="Path to the replica folder.")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds.")
    parser.add_argument("log_file", help="Path to the log file.")

    args = parser.parse_args()

    # Validate paths
    if not os.path.isdir(args.source):
        print(f"Source folder does not exist: {args.source}")
        exit(1)
    if not os.path.isdir(args.replica):
        print(f"Replica folder does not exist: {args.replica}")
        exit(1)

    main(args.source, args.replica, args.interval, args.log_file)