/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

export interface DownloadAlbum$Params {
	album_id: number;
	zip_originals?: boolean;
}

export function downloadAlbum(
	http: HttpClient,
	rootUrl: string,
	params: DownloadAlbum$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<Blob>> {
	const rb = new RequestBuilder(rootUrl, downloadAlbum.PATH, "get");
	if (params) {
		rb.path("album_id", params.album_id, {});
		rb.query("zip_originals", params.zip_originals, {});
	}

	return http
		.request(
			rb.build({ responseType: "blob", accept: "application/zip", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<Blob>;
			}),
		);
}

downloadAlbum.PATH = "/api/album/{album_id}/download/";
