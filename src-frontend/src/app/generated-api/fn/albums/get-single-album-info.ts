/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { AlbumWithImagesReadSchema } from "../../models/album-with-images-read-schema";

export interface GetSingleAlbumInfo$Params {
	album_id: number;
}

export function getSingleAlbumInfo(
	http: HttpClient,
	rootUrl: string,
	params: GetSingleAlbumInfo$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<AlbumWithImagesReadSchema>> {
	const rb = new RequestBuilder(rootUrl, getSingleAlbumInfo.PATH, "get");
	if (params) {
		rb.path("album_id", params.album_id, {});
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

getSingleAlbumInfo.PATH = "/api/album/{album_id}/";
