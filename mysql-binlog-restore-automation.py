#!/usr/bin/env python3

import subprocess
import argparse
import os
import sys

def restore_binlog(
    mysql_host,
    mysql_user,
    mysql_password,
    mysql_port,
    binlog_dir,
    start_time,
    stop_time=None
):
    try:
        # Get all binlog files sorted
        binlogs = sorted([
            os.path.join(binlog_dir, f)
            for f in os.listdir(binlog_dir)
            if f.startswith("mysql-bin.")
        ])

        if not binlogs:
            print("No binlog files found.")
            sys.exit(1)

        print(f"Found {len(binlogs)} binlog files.")

        # Build mysqlbinlog command
        cmd = [
            "mysqlbinlog",
            f"--start-datetime={start_time}"
        ]

        if stop_time:
            cmd.append(f"--stop-datetime={stop_time}")

        cmd.extend(binlogs)

        # Pipe into mysql client
        mysql_cmd = [
            "mysql",
            f"-h{mysql_host}",
            f"-P{mysql_port}",
            f"-u{mysql_user}",
            f"-p{mysql_password}"
        ]

        print("Starting binlog restore...")

        p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(mysql_cmd, stdin=p1.stdout)

        p1.stdout.close()
        p2.communicate()

        if p2.returncode == 0:
            print("Binlog restore completed successfully.")
        else:
            print("Restore failed.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restore MySQL binlog from timestamp")

    parser.add_argument("--host", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--port", default="3306")
    parser.add_argument("--binlog-dir", required=True)
    parser.add_argument("--start-time", required=True, help="Format: 'YYYY-MM-DD HH:MM:SS'")
    parser.add_argument("--stop-time", help="Optional stop time")

    args = parser.parse_args()

    restore_binlog(
        args.host,
        args.user,
        args.password,
        args.port,
        args.binlog_dir,
        args.start_time,
        args.stop_time
    )
