# Roadmap

## Near Term

- [ ] Initial CRUD Support For:
  - [ ] Image
  - [ ] Person
  - [ ] Location
  - [ ] Subject
  - [ ] Trip
- [ ] Sync SQLite database working
- [ ] Generation of thumbnails for each Image
- [ ] Configuration defined for:
  - [ ] Directories
  - [ ] SQLite
- [ ] Docker image
  - [ ] s6-overlay
  - [ ] Python/poetry
  - [ ] backend server
  - [ ] Task queue
- [ ] Task queue
  - [ ] Task for consuming images
- [ ] Basic web UI
- [ ] Basic filtering
  - [ ] Containing person, location or subject (only 1 at a time)
  - [ ] Not containing person, location or subject
- [ ] Image ingestion via upload
- [ ] Image indexing of existing folders
- [ ] Exact duplicate detection

## Medium Term

- [ ] Support for sync Postgres
- [ ] Text based Memory support
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
- [ ] Face boxes for People present in Image
- [ ] Advanced security

## Far Out Term

- [ ] Machine learning for face recognition
- [ ] Duplicate or near duplicate detection
