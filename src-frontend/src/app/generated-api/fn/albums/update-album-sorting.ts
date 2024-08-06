/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { AlbumSortUpdate } from "../../models/album-sort-update";
import { AlbumWithImagesReadSchema } from "../../models/album-with-images-read-schema";

export interface UpdateAlbumSorting$Params {
	album_id: number;
	body: AlbumSortUpdate;
}

export function updateAlbumSorting(
	http: HttpClient,
	rootUrl: string,
	params: UpdateAlbumSorting$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<AlbumWithImagesReadSchema>> {
	const rb = new RequestBuilder(rootUrl, updateAlbumSorting.PATH, "patch");
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

updateAlbumSorting.PATH = "/api/album/{album_id}/sort/";
