import { Component, type OnDestroy, type OnInit } from "@angular/core";
import { NgbPaginationConfig } from "@ng-bootstrap/ng-bootstrap";
import { type Subscription, combineLatest } from "rxjs";
import { map, tap } from "rxjs/operators";
import { ImagesService } from "../../generated-api/services";

@Component({
	selector: "app-photo-wall",
	templateUrl: "./photo-wall.component.html",
	styleUrl: "./photo-wall.component.css",
})
export class PhotoWallComponent implements OnInit, OnDestroy {
	imageIds: number[] = [];
	thumbnailUrls: { [key: number]: string } = {};
	currentPage = 1;
	pageSize = 50;
	totalPhotos = 0;
	maxPageSize = 10;

	private subscriptions: Subscription[] = [];

	constructor(
		private imagesService: ImagesService,
		private paginationConfig: NgbPaginationConfig,
	) {
		this.paginationConfig.maxSize = this.maxPageSize;
		this.paginationConfig.boundaryLinks = true;
	}

	ngOnInit() {
		this.loadPhotos();
	}

	ngOnDestroy() {
		for (const sub of this.subscriptions) {
			sub.unsubscribe();
		}
	}

	loadPhotos() {
		this.subscriptions.push(
			this.imagesService
				.getAllImages({ page: this.currentPage })
				.pipe(
					tap((response) => {
						this.totalPhotos = response.count;
						this.maxPageSize = Math.min(
							this.maxPageSize,
							Math.ceil(this.totalPhotos / this.pageSize),
						);
					}),
					map((response) => response.items),
				)
				.subscribe((imageIds) => {
					this.imageIds = imageIds;
					this.loadThumbnails();
				}),
		);
	}

	loadThumbnails() {
		this.subscriptions.push(
			combineLatest(
				this.imageIds.map((id) =>
					this.imagesService.getImageThumbnail({ image_id: id }),
				),
			).subscribe((thumbnailBlobs) => {
				this.imageIds.forEach((id, index) => {
					this.thumbnailUrls[id] = this.createObjectURL(thumbnailBlobs[index]);
				});
			}),
		);
	}

	private createObjectURL(blob: Blob): string {
		return URL.createObjectURL(blob);
	}
}
