/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

export interface DeleteLocation$Params {
	location_id: number;
}

export function deleteLocation(
	http: HttpClient,
	rootUrl: string,
	params: DeleteLocation$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<void>> {
	const rb = new RequestBuilder(rootUrl, deleteLocation.PATH, "delete");
	if (params) {
		rb.path("location_id", params.location_id, {});
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

deleteLocation.PATH = "/api/location/{location_id}/";
