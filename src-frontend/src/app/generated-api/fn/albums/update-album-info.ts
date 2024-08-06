/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { AlbumBasicReadSchema } from "../../models/album-basic-read-schema";
import { AlbumUpdateSchema } from "../../models/album-update-schema";

export interface UpdateAlbumInfo$Params {
	album_id: number;
	body: AlbumUpdateSchema;
}

export function updateAlbumInfo(
	http: HttpClient,
	rootUrl: string,
	params: UpdateAlbumInfo$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<AlbumBasicReadSchema>> {
	const rb = new RequestBuilder(rootUrl, updateAlbumInfo.PATH, "patch");
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
				return r as StrictHttpResponse<AlbumBasicReadSchema>;
			}),
		);
}

updateAlbumInfo.PATH = "/api/album/{album_id}/";
