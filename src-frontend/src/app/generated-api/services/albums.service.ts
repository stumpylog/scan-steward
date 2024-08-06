/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { BaseService } from "../base-service";
import { ApiConfiguration } from "../api-configuration";
import { StrictHttpResponse } from "../strict-http-response";

import { addImageToAlbum } from "../fn/albums/add-image-to-album";
import { AddImageToAlbum$Params } from "../fn/albums/add-image-to-album";
import { AlbumBasicReadSchema } from "../models/album-basic-read-schema";
import { AlbumWithImagesReadSchema } from "../models/album-with-images-read-schema";
import { createAlbum } from "../fn/albums/create-album";
import { CreateAlbum$Params } from "../fn/albums/create-album";
import { deleteAlbum } from "../fn/albums/delete-album";
import { DeleteAlbum$Params } from "../fn/albums/delete-album";
import { deleteImageFromAlbum } from "../fn/albums/delete-image-from-album";
import { DeleteImageFromAlbum$Params } from "../fn/albums/delete-image-from-album";
import { downloadAlbum } from "../fn/albums/download-album";
import { DownloadAlbum$Params } from "../fn/albums/download-album";
import { getAlbums } from "../fn/albums/get-albums";
import { GetAlbums$Params } from "../fn/albums/get-albums";
import { getSingleAlbumInfo } from "../fn/albums/get-single-album-info";
import { GetSingleAlbumInfo$Params } from "../fn/albums/get-single-album-info";
import { PagedAlbumBasicReadSchema } from "../models/paged-album-basic-read-schema";
import { updateAlbumInfo } from "../fn/albums/update-album-info";
import { UpdateAlbumInfo$Params } from "../fn/albums/update-album-info";
import { updateAlbumSorting } from "../fn/albums/update-album-sorting";
import { UpdateAlbumSorting$Params } from "../fn/albums/update-album-sorting";

@Injectable({ providedIn: "root" })
export class AlbumsService extends BaseService {
	constructor(config: ApiConfiguration, http: HttpClient) {
		super(config, http);
	}

	/** Path part for operation `getAlbums()` */
	static readonly GetAlbumsPath = "/api/album/";

	/**
	 * Get Albums.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getAlbums()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getAlbums$Response(
		params?: GetAlbums$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PagedAlbumBasicReadSchema>> {
		return getAlbums(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Albums.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getAlbums$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getAlbums(
		params?: GetAlbums$Params,
		context?: HttpContext,
	): Observable<PagedAlbumBasicReadSchema> {
		return this.getAlbums$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<PagedAlbumBasicReadSchema>,
				): PagedAlbumBasicReadSchema => r.body,
			),
		);
	}

	/** Path part for operation `createAlbum()` */
	static readonly CreateAlbumPath = "/api/album/";

	/**
	 * Create Album.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `createAlbum()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createAlbum$Response(
		params: CreateAlbum$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<AlbumBasicReadSchema>> {
		return createAlbum(this.http, this.rootUrl, params, context);
	}

	/**
	 * Create Album.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `createAlbum$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createAlbum(
		params: CreateAlbum$Params,
		context?: HttpContext,
	): Observable<AlbumBasicReadSchema> {
		return this.createAlbum$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<AlbumBasicReadSchema>): AlbumBasicReadSchema =>
					r.body,
			),
		);
	}

	/** Path part for operation `getSingleAlbumInfo()` */
	static readonly GetSingleAlbumInfoPath = "/api/album/{album_id}/";

	/**
	 * Get Album.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getSingleAlbumInfo()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getSingleAlbumInfo$Response(
		params: GetSingleAlbumInfo$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<AlbumWithImagesReadSchema>> {
		return getSingleAlbumInfo(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Album.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getSingleAlbumInfo$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getSingleAlbumInfo(
		params: GetSingleAlbumInfo$Params,
		context?: HttpContext,
	): Observable<AlbumWithImagesReadSchema> {
		return this.getSingleAlbumInfo$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<AlbumWithImagesReadSchema>,
				): AlbumWithImagesReadSchema => r.body,
			),
		);
	}

	/** Path part for operation `deleteAlbum()` */
	static readonly DeleteAlbumPath = "/api/album/{album_id}/";

	/**
	 * Delete Album.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `deleteAlbum()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deleteAlbum$Response(
		params: DeleteAlbum$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<void>> {
		return deleteAlbum(this.http, this.rootUrl, params, context);
	}

	/**
	 * Delete Album.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `deleteAlbum$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deleteAlbum(
		params: DeleteAlbum$Params,
		context?: HttpContext,
	): Observable<void> {
		return this.deleteAlbum$Response(params, context).pipe(
			map((r: StrictHttpResponse<void>): void => r.body),
		);
	}

	/** Path part for operation `updateAlbumInfo()` */
	static readonly UpdateAlbumInfoPath = "/api/album/{album_id}/";

	/**
	 * Update Album.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `updateAlbumInfo()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateAlbumInfo$Response(
		params: UpdateAlbumInfo$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<AlbumBasicReadSchema>> {
		return updateAlbumInfo(this.http, this.rootUrl, params, context);
	}

	/**
	 * Update Album.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `updateAlbumInfo$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateAlbumInfo(
		params: UpdateAlbumInfo$Params,
		context?: HttpContext,
	): Observable<AlbumBasicReadSchema> {
		return this.updateAlbumInfo$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<AlbumBasicReadSchema>): AlbumBasicReadSchema =>
					r.body,
			),
		);
	}

	/** Path part for operation `addImageToAlbum()` */
	static readonly AddImageToAlbumPath = "/api/album/{album_id}/add/";

	/**
	 * Add Image To Album.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `addImageToAlbum()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	addImageToAlbum$Response(
		params: AddImageToAlbum$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<AlbumWithImagesReadSchema>> {
		return addImageToAlbum(this.http, this.rootUrl, params, context);
	}

	/**
	 * Add Image To Album.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `addImageToAlbum$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	addImageToAlbum(
		params: AddImageToAlbum$Params,
		context?: HttpContext,
	): Observable<AlbumWithImagesReadSchema> {
		return this.addImageToAlbum$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<AlbumWithImagesReadSchema>,
				): AlbumWithImagesReadSchema => r.body,
			),
		);
	}

	/** Path part for operation `deleteImageFromAlbum()` */
	static readonly DeleteImageFromAlbumPath = "/api/album/{album_id}/remove/";

	/**
	 * Remove Image From Album.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `deleteImageFromAlbum()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	deleteImageFromAlbum$Response(
		params: DeleteImageFromAlbum$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<AlbumWithImagesReadSchema>> {
		return deleteImageFromAlbum(this.http, this.rootUrl, params, context);
	}

	/**
	 * Remove Image From Album.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `deleteImageFromAlbum$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	deleteImageFromAlbum(
		params: DeleteImageFromAlbum$Params,
		context?: HttpContext,
	): Observable<AlbumWithImagesReadSchema> {
		return this.deleteImageFromAlbum$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<AlbumWithImagesReadSchema>,
				): AlbumWithImagesReadSchema => r.body,
			),
		);
	}

	/** Path part for operation `updateAlbumSorting()` */
	static readonly UpdateAlbumSortingPath = "/api/album/{album_id}/sort/";

	/**
	 * Update Album Sorting.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `updateAlbumSorting()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateAlbumSorting$Response(
		params: UpdateAlbumSorting$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<AlbumWithImagesReadSchema>> {
		return updateAlbumSorting(this.http, this.rootUrl, params, context);
	}

	/**
	 * Update Album Sorting.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `updateAlbumSorting$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateAlbumSorting(
		params: UpdateAlbumSorting$Params,
		context?: HttpContext,
	): Observable<AlbumWithImagesReadSchema> {
		return this.updateAlbumSorting$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<AlbumWithImagesReadSchema>,
				): AlbumWithImagesReadSchema => r.body,
			),
		);
	}

	/** Path part for operation `downloadAlbum()` */
	static readonly DownloadAlbumPath = "/api/album/{album_id}/download/";

	/**
	 * Download Album.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `downloadAlbum()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	downloadAlbum$Response(
		params: DownloadAlbum$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Blob>> {
		return downloadAlbum(this.http, this.rootUrl, params, context);
	}

	/**
	 * Download Album.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `downloadAlbum$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	downloadAlbum(
		params: DownloadAlbum$Params,
		context?: HttpContext,
	): Observable<Blob> {
		return this.downloadAlbum$Response(params, context).pipe(
			map((r: StrictHttpResponse<Blob>): Blob => r.body),
		);
	}
}
