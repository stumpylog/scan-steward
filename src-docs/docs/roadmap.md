# Roadmap

## Near Term

### Backend

- [x] SQLite database support
- [x] Generation of thumbnails for each Image
- [x] Reading existing MWG region info boxes
    - [x] Creating or linking to existing Person
    - [x] Creating or linking to existing Pet
- [x] Reading the following metadata:
    - [x] Tags, including hierarchy
    - [x] Rough location, including hierarchy, from MWG location
    - [x] Rough location, based on keywords
    - [x] Rough dating, based on keywords
    - [x] Creating new tags or linking to existing tags as needed
    - [x] Reading image description
- [ ] Syncing metadata back to image
    - [ ] Tags
    - [ ] MWG location
    - [ ] Tag based dating structure
    - [ ] Image description
- [ ] Configuration for:
    - [ ] Directories
    - [ ] SQLite
- [ ] Basic filtering
    - [ ] Containing given person
    - [ ] In given country
    - [ ] In given country, state
    - [ ] In given country, city
    - [ ] In given city
    - [ ] In given year
    - [ ] In given year, month
    - [ ] In given year, month, day
- [x] Image indexing of existing folders
- [x] Exact duplicate detection
- [x] Album support
    - [x] Independent sorting of images per album
    - [x] Download zip archive of images in album
        - [x] Maintain sorting order in file naming

### Docker

- [ ] Docker image
    - [ ] Alpine based image
    - [ ] s6-overlay
    - [ ] backend server
    - [ ] frontend via nginx

### Frontend

- [ ] Paginated image wall of all images
- [ ] View single image full size
- [ ] Add image to album
- [ ] View album images (sorted)
- [ ] Update album sorting

## Medium Term

### Backend

- [ ] Support for Postgres
- [ ] User support
    - [ ] Role based access control
- [ ] Combination filters
    - [ ] Containing ALL given people
    - [ ] Container all people but not others
- [ ] Basic Image operations
    - [ ] Rotate
    - [ ] Flip
    - [ ] Mirror
    - [ ] Soft delete (aka trash)
    - [ ] Scheduled trash cleanup

### Frontend

- [ ] Draw new face boxes for People present in Image
- [ ] Draw new boxes for Pets present in Image

## Long Term

- [ ] Audio Memory support
- [ ] Document Memory support
- [ ] Compressed static files
- [ ] Advanced security

## Far Out Term

- [ ] Machine learning for face recognition
- [ ] Near duplicate detection
