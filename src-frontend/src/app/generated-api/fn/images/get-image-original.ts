/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

export interface GetImageOriginal$Params {
	image_id: number;
}

export function getImageOriginal(
	http: HttpClient,
	rootUrl: string,
	params: GetImageOriginal$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<Blob>> {
	const rb = new RequestBuilder(rootUrl, getImageOriginal.PATH, "get");
	if (params) {
		rb.path("image_id", params.image_id, {});
	}

	return http
		.request(rb.build({ responseType: "blob", accept: "image/*", context }))
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<Blob>;
			}),
		);
}

getImageOriginal.PATH = "/api/image/{image_id}/original/";
