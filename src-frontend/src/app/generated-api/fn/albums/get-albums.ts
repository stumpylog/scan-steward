/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PagedAlbumBasicReadSchema } from "../../models/paged-album-basic-read-schema";

export interface GetAlbums$Params {
	name_like?: string | null;
	page?: number;
}

export function getAlbums(
	http: HttpClient,
	rootUrl: string,
	params?: GetAlbums$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<PagedAlbumBasicReadSchema>> {
	const rb = new RequestBuilder(rootUrl, getAlbums.PATH, "get");
	if (params) {
		rb.query("name_like", params.name_like, {});
		rb.query("page", params.page, {});
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<PagedAlbumBasicReadSchema>;
			}),
		);
}

getAlbums.PATH = "/api/album/";
