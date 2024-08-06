/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

export interface DeleteAlbum$Params {
	album_id: number;
}

export function deleteAlbum(
	http: HttpClient,
	rootUrl: string,
	params: DeleteAlbum$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<void>> {
	const rb = new RequestBuilder(rootUrl, deleteAlbum.PATH, "delete");
	if (params) {
		rb.path("album_id", params.album_id, {});
	}

	return http
		.request(rb.build({ responseType: "text", accept: "*/*", context }))
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return (r as HttpResponse<any>).clone({
					body: undefined,
				}) as StrictHttpResponse<void>;
			}),
		);
}

deleteAlbum.PATH = "/api/album/{album_id}/";
