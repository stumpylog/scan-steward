/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

export interface DeleteRoughDate$Params {
	date_id: number;
}

export function deleteRoughDate(
	http: HttpClient,
	rootUrl: string,
	params: DeleteRoughDate$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<void>> {
	const rb = new RequestBuilder(rootUrl, deleteRoughDate.PATH, "delete");
	if (params) {
		rb.path("date_id", params.date_id, {});
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

deleteRoughDate.PATH = "/api/date/{date_id}/";
