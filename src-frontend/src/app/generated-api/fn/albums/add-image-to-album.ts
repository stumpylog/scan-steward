/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { AlbumAddImageSchema } from "../../models/album-add-image-schema";
import { AlbumWithImagesReadSchema } from "../../models/album-with-images-read-schema";

export interface AddImageToAlbum$Params {
	album_id: number;
	body: AlbumAddImageSchema;
}

export function addImageToAlbum(
	http: HttpClient,
	rootUrl: string,
	params: AddImageToAlbum$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<AlbumWithImagesReadSchema>> {
	const rb = new RequestBuilder(rootUrl, addImageToAlbum.PATH, "patch");
	if (params) {
		rb.path("album_id", params.album_id, {});
		rb.body(params.body, "application/json");
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<AlbumWithImagesReadSchema>;
			}),
		);
}

addImageToAlbum.PATH = "/api/album/{album_id}/add/";
