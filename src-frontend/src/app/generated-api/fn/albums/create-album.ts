/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { AlbumBasicReadSchema } from "../../models/album-basic-read-schema";
import { AlbumCreateSchema } from "../../models/album-create-schema";

export interface CreateAlbum$Params {
	body: AlbumCreateSchema;
}

export function createAlbum(
	http: HttpClient,
	rootUrl: string,
	params: CreateAlbum$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<AlbumBasicReadSchema>> {
	const rb = new RequestBuilder(rootUrl, createAlbum.PATH, "post");
	if (params) {
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

createAlbum.PATH = "/api/album/";
