/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

import { PersonWithBoxSchema } from "../../models/person-with-box-schema";

export interface GetFacesInImages$Params {
	image_id: number;
}

export function getFacesInImages(
	http: HttpClient,
	rootUrl: string,
	params: GetFacesInImages$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<Array<PersonWithBoxSchema>>> {
	const rb = new RequestBuilder(rootUrl, getFacesInImages.PATH, "get");
	if (params) {
		rb.path("image_id", params.image_id, {});
	}

	return http
		.request(
			rb.build({ responseType: "json", accept: "application/json", context }),
		)
		.pipe(
			filter((r: any): r is HttpResponse<any> => r instanceof HttpResponse),
			map((r: HttpResponse<any>) => {
				return r as StrictHttpResponse<Array<PersonWithBoxSchema>>;
			}),
		);
}

getFacesInImages.PATH = "/api/image/{image_id}/faces/";
