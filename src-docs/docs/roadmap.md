# Roadmap

## Near Term

- [ ] Initial CRUD Support For
    - [ ] Person
    - [ ] Location (hierarchical)
    - [ ] Tag (hierarchical)
    - [ ] Album (hierarchical)
- [ ] SQLite database support
- [ ] Generation of thumbnails for each Image
- [ ] Reading existing face boxes
    - [ ] Creating or linking to existing Person
- [ ] Reading existing tags
    - [ ] Creating new tags or linking to existing tags as needed
- [ ] Configuration defined for:
    - [ ] Directories
    - [ ] SQLite
- [ ] Docker image
    - [ ] s6-overlay
    - [ ] Python/poetry
    - [ ] backend server
- [ ] Basic web UI
- [ ] Basic filtering
    - [ ] Containing person, location or subject (only 1 at a time)
    - [ ] Not containing person, location or subject
- [ ] Image indexing of existing folders
- [ ] Exact duplicate detection

## Medium Term

- [ ] Album support
    - [ ] Independent sorting of images per album
    - [ ] Download zip archive of images in album
        - [ ] Maintain sorting order in file naming
- [ ] Support for Postgres
- [ ] User support
- [ ] Combination filters
    - [ ] Containing one or more people locations, subjects
- [ ] Basic Image operations
    - [ ] Rotate
    - [ ] Flip
    - [ ] Mirror

## Long Term

- [ ] Audio Memory support
- [ ] Document Memory support
- [ ] Compressed static files
- [ ] Draw new face boxes for People present in Image
- [ ] Sync metadata back to image file using exiftool
- [ ] Advanced security

## Far Out Term

- [ ] Machine learning for face recognition
- [ ] Duplicate or near duplicate detection
