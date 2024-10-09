import hashlib
import os
import glob
import argparse


def compute_checksum( file_path: str ):
    sha256_hash = hashlib.sha256()
    with open( file_path, "rb" ) as f:
        for byte_block in iter( lambda: f.read( 4096 ), b"" ):
            sha256_hash.update( byte_block )
    return sha256_hash.hexdigest()


def main( pattern: str, checksum_extension: str, subfolder: str, paths_ignore: list[str] ):
    for filepath in glob.glob( pattern, recursive=True ):
        parent_path, basename = os.path.split( filepath )
        file_extension        = os.path.splitext( filepath )[1]

        if ( os.path.isdir( filepath ) or # skip folders.
             file_extension == ".{checksum_extension}"  or # skip checksum files.
             filepath in paths_ignore
        ):
            continue

        checksum = compute_checksum( filepath )

        subfolder_path = os.path.join( parent_path, subfolder )
        if not os.path.exists( subfolder_path ):
             os.mkdir( subfolder_path )
        elif not os.path.isdir( subfolder_path ):
             raise Exception( "Subfolder already exist but is not a folder." )

        with open( os.path.join( subfolder_path, f"{basename}.{checksum_extension}" ), "w" ) as f:
            f.write( checksum )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate checksums for multiple files"
    )

    #### Same arguments must be also present on the "action.yaml" file.
    parser.add_argument(
        "--pattern",
        required=True,
        help="Pattern to search for files (glob)"
    )
    parser.add_argument(
        "--checksum_extension",
        default="checksum",
        help="Checksum extension"
    )
    parser.add_argument(
        "--subfolder",
        required=False,
        default="checksums__",
        help="Subfolder to put the checksum files"
    )
    parser.add_argument(
        "--paths_ignore",
        required=False,
        default=[],
        help="Paths to ignore"
    )

    args = parser.parse_args()
    main( pattern=args.pattern, checksum_extension=args.checksum_extension, subfolder=args.subfolder, paths_ignore=args.paths_ignore )
