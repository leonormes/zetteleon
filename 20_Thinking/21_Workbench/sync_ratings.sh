#!/bin/bash

# sync_ratings.sh - Automates fetching ratings from Goodreads and updating Calibre custom columns

IDS=$@

if [ -z "$IDS" ]; then
    echo "Usage: $0 <book_id1> <book_id2> ..."
    exit 1
fi

for ID in $IDS; do
    echo "Processing Book ID: $ID"
    
    # Get Title and Author from Calibre
    METADATA=$(calibredb show_metadata $ID)
    TITLE=$(echo "$METADATA" | grep "^Title" | cut -d":" -f2- | xargs)
    AUTHOR=$(echo "$METADATA" | grep "^Author(s)" | cut -d":" -f2- | cut -d"[" -f1 | xargs)
    
    echo "  Title: $TITLE"
    echo "  Author: $AUTHOR"
    
    # Fetch metadata from Goodreads
    fetch-ebook-metadata --title "$TITLE" --authors "$AUTHOR" --allowed-plugin Goodreads --opf > /tmp/meta.opf 2>/dev/null
    
    # Extract rating (calibre:rating meta tag)
    RATING=$(grep "calibre:rating" /tmp/meta.opf | sed 's/.*content="\([^"]*\)".*/\1/')
    
    if [ ! -z "$RATING" ]; then
        echo "  Found Rating: $RATING"
        # Update Calibre
        calibredb set_custom prodos_rating $ID "$RATING"
    else
        echo "  No rating found on Goodreads."
    fi
    
    # Clean up
    rm -f /tmp/meta.opf
done
