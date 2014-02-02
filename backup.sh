#!/bin/bash

## For backing up the database.

BACKUP_DIR=$HOME/backups
backup_file="$BACKUP_DIR/sqlite.db.`date +%Y-%m-%d-%H-%M-%S`.bak"

echo "Copying database to $backup_file..."
cp data/sqlite.db $backup_file
