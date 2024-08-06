/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { BaseService } from "../base-service";
import { ApiConfiguration } from "../api-configuration";
import { StrictHttpResponse } from "../strict-http-response";

import { deleteFacesInImage } from "../fn/images/delete-faces-in-image";
import { DeleteFacesInImage$Params } from "../fn/images/delete-faces-in-image";
import { deletePetsFromImage } from "../fn/images/delete-pets-from-image";
import { DeletePetsFromImage$Params } from "../fn/images/delete-pets-from-image";
import { getAllImages } from "../fn/images/get-all-images";
import { GetAllImages$Params } from "../fn/images/get-all-images";
import { getFacesInImages } from "../fn/images/get-faces-in-images";
import { GetFacesInImages$Params } from "../fn/images/get-faces-in-images";
import { getImageFullSize } from "../fn/images/get-image-full-size";
import { GetImageFullSize$Params } from "../fn/images/get-image-full-size";
import { getImageMetadata } from "../fn/images/get-image-metadata";
import { GetImageMetadata$Params } from "../fn/images/get-image-metadata";
import { getImageOriginal } from "../fn/images/get-image-original";
import { GetImageOriginal$Params } from "../fn/images/get-image-original";
import { getImageThumbnail } from "../fn/images/get-image-thumbnail";
import { GetImageThumbnail$Params } from "../fn/images/get-image-thumbnail";
import { getPetsInImages } from "../fn/images/get-pets-in-images";
import { GetPetsInImages$Params } from "../fn/images/get-pets-in-images";
import { ImageMetadataReadSchema } from "../models/image-metadata-read-schema";
import { Pagedint } from "../models/pagedint";
import { PersonWithBoxSchema } from "../models/person-with-box-schema";
import { PetWithBoxSchema } from "../models/pet-with-box-schema";
import { updateFacesInImage } from "../fn/images/update-faces-in-image";
import { UpdateFacesInImage$Params } from "../fn/images/update-faces-in-image";
import { updateImageMetadata } from "../fn/images/update-image-metadata";
import { UpdateImageMetadata$Params } from "../fn/images/update-image-metadata";
import { updatePetBoxesInImage } from "../fn/images/update-pet-boxes-in-image";
import { UpdatePetBoxesInImage$Params } from "../fn/images/update-pet-boxes-in-image";

@Injectable({ providedIn: "root" })
export class ImagesService extends BaseService {
	constructor(config: ApiConfiguration, http: HttpClient) {
		super(config, http);
	}

	/** Path part for operation `getAllImages()` */
	static readonly GetAllImagesPath = "/api/image/";

	/**
	 * Get All Images.
	 *
	 * Get all images, filtered as requested
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getAllImages()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getAllImages$Response(
		params?: GetAllImages$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Pagedint>> {
		return getAllImages(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get All Images.
	 *
	 * Get all images, filtered as requested
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getAllImages$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getAllImages(
		params?: GetAllImages$Params,
		context?: HttpContext,
	): Observable<Pagedint> {
		return this.getAllImages$Response(params, context).pipe(
			map((r: StrictHttpResponse<Pagedint>): Pagedint => r.body),
		);
	}

	/** Path part for operation `getImageThumbnail()` */
	static readonly GetImageThumbnailPath = "/api/image/{image_id}/thumbnail/";

	/**
	 * Get Image Thumbnail.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getImageThumbnail()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getImageThumbnail$Response(
		params: GetImageThumbnail$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Blob>> {
		return getImageThumbnail(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Image Thumbnail.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getImageThumbnail$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getImageThumbnail(
		params: GetImageThumbnail$Params,
		context?: HttpContext,
	): Observable<Blob> {
		return this.getImageThumbnail$Response(params, context).pipe(
			map((r: StrictHttpResponse<Blob>): Blob => r.body),
		);
	}

	/** Path part for operation `getImageFullSize()` */
	static readonly GetImageFullSizePath = "/api/image/{image_id}/full/";

	/**
	 * Get Image Full Size.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getImageFullSize()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getImageFullSize$Response(
		params: GetImageFullSize$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Blob>> {
		return getImageFullSize(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Image Full Size.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getImageFullSize$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getImageFullSize(
		params: GetImageFullSize$Params,
		context?: HttpContext,
	): Observable<Blob> {
		return this.getImageFullSize$Response(params, context).pipe(
			map((r: StrictHttpResponse<Blob>): Blob => r.body),
		);
	}

	/** Path part for operation `getImageOriginal()` */
	static readonly GetImageOriginalPath = "/api/image/{image_id}/original/";

	/**
	 * Get Image Original.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getImageOriginal()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getImageOriginal$Response(
		params: GetImageOriginal$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Blob>> {
		return getImageOriginal(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Image Original.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getImageOriginal$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getImageOriginal(
		params: GetImageOriginal$Params,
		context?: HttpContext,
	): Observable<Blob> {
		return this.getImageOriginal$Response(params, context).pipe(
			map((r: StrictHttpResponse<Blob>): Blob => r.body),
		);
	}

	/** Path part for operation `getFacesInImages()` */
	static readonly GetFacesInImagesPath = "/api/image/{image_id}/faces/";

	/**
	 * Get Faces In Images.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getFacesInImages()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getFacesInImages$Response(
		params: GetFacesInImages$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Array<PersonWithBoxSchema>>> {
		return getFacesInImages(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Faces In Images.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getFacesInImages$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getFacesInImages(
		params: GetFacesInImages$Params,
		context?: HttpContext,
	): Observable<Array<PersonWithBoxSchema>> {
		return this.getFacesInImages$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<Array<PersonWithBoxSchema>>,
				): Array<PersonWithBoxSchema> => r.body,
			),
		);
	}

	/** Path part for operation `deleteFacesInImage()` */
	static readonly DeleteFacesInImagePath = "/api/image/{image_id}/faces/";

	/**
	 * Delete Faces In Image.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `deleteFacesInImage()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	deleteFacesInImage$Response(
		params: DeleteFacesInImage$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Array<PersonWithBoxSchema>>> {
		return deleteFacesInImage(this.http, this.rootUrl, params, context);
	}

	/**
	 * Delete Faces In Image.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `deleteFacesInImage$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	deleteFacesInImage(
		params: DeleteFacesInImage$Params,
		context?: HttpContext,
	): Observable<Array<PersonWithBoxSchema>> {
		return this.deleteFacesInImage$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<Array<PersonWithBoxSchema>>,
				): Array<PersonWithBoxSchema> => r.body,
			),
		);
	}

	/** Path part for operation `updateFacesInImage()` */
	static readonly UpdateFacesInImagePath = "/api/image/{image_id}/faces/";

	/**
	 * Update Faces In Image.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `updateFacesInImage()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateFacesInImage$Response(
		params: UpdateFacesInImage$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Array<PersonWithBoxSchema>>> {
		return updateFacesInImage(this.http, this.rootUrl, params, context);
	}

	/**
	 * Update Faces In Image.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `updateFacesInImage$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateFacesInImage(
		params: UpdateFacesInImage$Params,
		context?: HttpContext,
	): Observable<Array<PersonWithBoxSchema>> {
		return this.updateFacesInImage$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<Array<PersonWithBoxSchema>>,
				): Array<PersonWithBoxSchema> => r.body,
			),
		);
	}

	/** Path part for operation `getPetsInImages()` */
	static readonly GetPetsInImagesPath = "/api/image/{image_id}/pets/";

	/**
	 * Get Pets In Images.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getPetsInImages()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getPetsInImages$Response(
		params: GetPetsInImages$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Array<PetWithBoxSchema>>> {
		return getPetsInImages(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Pets In Images.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getPetsInImages$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getPetsInImages(
		params: GetPetsInImages$Params,
		context?: HttpContext,
	): Observable<Array<PetWithBoxSchema>> {
		return this.getPetsInImages$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<Array<PetWithBoxSchema>>,
				): Array<PetWithBoxSchema> => r.body,
			),
		);
	}

	/** Path part for operation `deletePetsFromImage()` */
	static readonly DeletePetsFromImagePath = "/api/image/{image_id}/pets/";

	/**
	 * Delete Pets From Image.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `deletePetsFromImage()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	deletePetsFromImage$Response(
		params: DeletePetsFromImage$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Array<PetWithBoxSchema>>> {
		return deletePetsFromImage(this.http, this.rootUrl, params, context);
	}

	/**
	 * Delete Pets From Image.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `deletePetsFromImage$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	deletePetsFromImage(
		params: DeletePetsFromImage$Params,
		context?: HttpContext,
	): Observable<Array<PetWithBoxSchema>> {
		return this.deletePetsFromImage$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<Array<PetWithBoxSchema>>,
				): Array<PetWithBoxSchema> => r.body,
			),
		);
	}

	/** Path part for operation `updatePetBoxesInImage()` */
	static readonly UpdatePetBoxesInImagePath = "/api/image/{image_id}/pets/";

	/**
	 * Update Pet Boxes In Image.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `updatePetBoxesInImage()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updatePetBoxesInImage$Response(
		params: UpdatePetBoxesInImage$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<Array<PetWithBoxSchema>>> {
		return updatePetBoxesInImage(this.http, this.rootUrl, params, context);
	}

	/**
	 * Update Pet Boxes In Image.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `updatePetBoxesInImage$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updatePetBoxesInImage(
		params: UpdatePetBoxesInImage$Params,
		context?: HttpContext,
	): Observable<Array<PetWithBoxSchema>> {
		return this.updatePetBoxesInImage$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<Array<PetWithBoxSchema>>,
				): Array<PetWithBoxSchema> => r.body,
			),
		);
	}

	/** Path part for operation `getImageMetadata()` */
	static readonly GetImageMetadataPath = "/api/image/{image_id}/metadata/";

	/**
	 * Get Image Metadata.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getImageMetadata()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getImageMetadata$Response(
		params: GetImageMetadata$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<ImageMetadataReadSchema>> {
		return getImageMetadata(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Image Metadata.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getImageMetadata$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getImageMetadata(
		params: GetImageMetadata$Params,
		context?: HttpContext,
	): Observable<ImageMetadataReadSchema> {
		return this.getImageMetadata$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<ImageMetadataReadSchema>,
				): ImageMetadataReadSchema => r.body,
			),
		);
	}

	/** Path part for operation `updateImageMetadata()` */
	static readonly UpdateImageMetadataPath = "/api/image/{image_id}/metadata/";

	/**
	 * Update Image Metadata.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `updateImageMetadata()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateImageMetadata$Response(
		params: UpdateImageMetadata$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<ImageMetadataReadSchema>> {
		return updateImageMetadata(this.http, this.rootUrl, params, context);
	}

	/**
	 * Update Image Metadata.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `updateImageMetadata$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateImageMetadata(
		params: UpdateImageMetadata$Params,
		context?: HttpContext,
	): Observable<ImageMetadataReadSchema> {
		return this.updateImageMetadata$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<ImageMetadataReadSchema>,
				): ImageMetadataReadSchema => r.body,
			),
		);
	}
}
