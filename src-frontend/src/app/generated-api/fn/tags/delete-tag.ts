/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { filter, map } from "rxjs/operators";
import { StrictHttpResponse } from "../../strict-http-response";
import { RequestBuilder } from "../../request-builder";

export interface DeleteTag$Params {
	tag_id: number;
}

export function deleteTag(
	http: HttpClient,
	rootUrl: string,
	params: DeleteTag$Params,
	context?: HttpContext,
): Observable<StrictHttpResponse<void>> {
	const rb = new RequestBuilder(rootUrl, deleteTag.PATH, "delete");
	if (params) {
		rb.path("tag_id", params.tag_id, {});
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

deleteTag.PATH = "/api/tag/{tag_id}/";
